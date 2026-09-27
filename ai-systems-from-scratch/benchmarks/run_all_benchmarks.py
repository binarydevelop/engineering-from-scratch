#!/usr/bin/env python3
"""
Master Benchmark Suite Runner (20+ Experiments).
Executes and logs quantitative metrics across all subsystems.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

from benchmarks_collection import *

BENCHMARKS = [
    ("Bench 01: Eager vs Compiled Matmul", run_bench01_eager_vs_compiled),
    ("Bench 02: Operator Fusion Memory Traffic", run_bench02_operator_fusion_traffic),
    ("Bench 03: CPU Cache Tiling Hit Rate", run_bench03_cpu_tiling),
    ("Bench 04: Prefill vs Decode Arithmetic Intensity", run_bench04_prefill_vs_decode),
    ("Bench 05: KV Cache Compute Reduction", run_bench05_kv_cache_impact),
    ("Bench 06: Static vs Continuous Batching", run_bench06_batching),
    ("Bench 07: Paged vs Contiguous KV Fragmentation", run_bench07_paged_kv_cache),
    ("Bench 08: Prefix Caching Speedup", run_bench08_prefix_caching),
    ("Bench 09: Quantization Memory Compression", run_bench09_quant_memory),
    ("Bench 10: INT8 Quantization Numerical Error", run_bench10_quant_error),
    ("Bench 11: Speculative Decoding Throughput Gain", run_bench11_speculative_decoding),
    ("Bench 12: Training Loop Step Latency", run_bench12_training_latency),
    ("Bench 13: Gradient Accumulation Peak Memory", run_bench13_gradient_accumulation),
    ("Bench 14: Full Fine-Tuning vs LoRA State Memory", run_bench14_lora_memory),
    ("Bench 15: Sample Packing Saturation", run_bench15_sample_packing),
    ("Bench 16: Exact Match vs Judge Eval Latency", run_bench16_eval_latency),
    ("Bench 17: LLM-as-Judge Position Bias Rate", run_bench17_judge_position_bias),
    ("Bench 18: BM25 vs Dense Search Latency", run_bench18_retrieval_latency),
    ("Bench 19: Agent Turn Cost & Latency Growth", run_bench19_agent_turn_growth),
    ("Bench 20: Jittered Retry Collision Mitigation", run_bench20_backoff_jitter),
]

def main():
    print("=" * 65)
    print(" AI Systems From Scratch: Master Benchmark Suite (20 Experiments)")
    print("=" * 65)
    
    summary = {}
    for name, fn in BENCHMARKS:
        res = fn()
        summary[name] = res
        print(f"\n>> {name}")
        for k, v in res.items():
            if isinstance(v, float):
                print(f"   - {k:35s}: {v:.4f}")
            else:
                print(f"   - {k:35s}: {v}")

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/master_benchmarks.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("\n" + "=" * 65)
    print(" Master Benchmark Suite completed. Output saved to outputs/master_benchmarks.json")
    print("=" * 65)

if __name__ == "__main__":
    main()
