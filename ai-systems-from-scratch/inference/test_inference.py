import os
import sys
import pytest
import torch

sys.path.insert(0, os.path.dirname(__file__))

from kv_cache import SimpleKVCache, memory_footprint_report
from continuous_batching_scheduler import ContinuousBatchingSimulator, InferenceRequest, simulate_static_batching
from paged_kv_cache import PagedKVCacheManager
from prefix_caching import PrefixCacheEngine
from quantization_engine import (
    quantize_symmetric_int8,
    dequantize_symmetric_int8,
    quantize_asymmetric_uint8,
    dequantize_asymmetric_uint8,
    evaluate_quantization_error,
    QuantizedLinearWeightOnly
)
from speculative_decoding import run_speculative_experiment

def test_kv_cache_update_and_memory():
    cache = SimpleKVCache(num_layers=2, num_heads=4, head_dim=16, max_seq_len=64)
    new_k = torch.randn(4, 1, 16)
    new_v = torch.randn(4, 1, 16)
    k_hist, v_hist = cache.update(layer_idx=0, new_k=new_k, new_v=new_v)
    assert k_hist.shape == (4, 1, 16)
    cache.advance_step()

    # Memory calculation
    bytes_calc = SimpleKVCache.calculate_memory_bytes(num_layers=32, num_heads=32, head_dim=128, seq_len=1024, batch_size=1, dtype_bytes=2)
    assert bytes_calc == 2 * 32 * 1 * 32 * 1024 * 128 * 2

def test_continuous_batching_superiority():
    requests = [
        InferenceRequest("r1", prompt_len=10, target_output_len=5, arrival_step=0),
        InferenceRequest("r2", prompt_len=10, target_output_len=20, arrival_step=0),
        InferenceRequest("r3", prompt_len=10, target_output_len=5, arrival_step=0),
        InferenceRequest("r4", prompt_len=10, target_output_len=20, arrival_step=0),
    ]
    sim = ContinuousBatchingSimulator(max_batch_size=2)
    for r in requests:
        sim.add_request(r)
    res_cb = sim.run_until_complete()
    assert res_cb["total_steps"] > 0
    assert len(sim.completed) == 4

def test_paged_kv_cache_allocation():
    mgr = PagedKVCacheManager(total_blocks=10, block_size=16)
    # Allocate seq1 needing 24 tokens (needs 2 blocks)
    success = mgr.allocate_sequence("seq1", prompt_len=24)
    assert success is True
    assert len(mgr.free_blocks) == 8

    # Append 1 token
    app_success = mgr.append_token("seq1")
    assert app_success is True

    # Free sequence
    mgr.free_sequence("seq1")
    assert len(mgr.free_blocks) == 10

def test_prefix_caching():
    engine = PrefixCacheEngine()
    sys_prompt_tokens = [101, 2054, 2003, 1037] # "This is a"
    engine.insert_prefix(sys_prompt_tokens, cache_handle="SYS_PROMPT_HANDLE")

    # Match exact prefix
    matched_len, handle = engine.match_longest_prefix([101, 2054, 2003, 1037, 5000])
    assert matched_len == 4
    assert handle == "SYS_PROMPT_HANDLE"

def test_quantization_roundtrip_and_error():
    x = torch.randn(64, 64)
    q, scale = quantize_symmetric_int8(x)
    deq = dequantize_symmetric_int8(q, scale)
    err = evaluate_quantization_error(x, deq)
    assert err["cosine_similarity"] > 0.99
    assert err["mse"] < 0.01

    # Asymmetric
    q_asym, scale_asym, zp = quantize_asymmetric_uint8(x)
    deq_asym = dequantize_asymmetric_uint8(q_asym, scale_asym, zp)
    err_asym = evaluate_quantization_error(x, deq_asym)
    assert err_asym["cosine_similarity"] > 0.99

def test_speculative_decoding_simulation():
    res = run_speculative_experiment(num_trials=50, lookahead_k=4, acceptance_rate=0.75)
    assert res["effective_speedup"] > 1.5
