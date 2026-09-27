"""
Implementations of all 40 Broken-System Lab Scenarios.
Each function represents a realistic production defect.
"""

from typing import Tuple, List, Dict
import math
import time
import json
import torch
import numpy as np

# ----------------- COMPILER LABS -----------------
def broken_lab01_graph_break(x: torch.Tensor) -> torch.Tensor:
    # BUG: Python data-dependent control flow severs graph capture in torch.compile
    if x.sum().item() > 0:
        return torch.relu(x)
    return torch.sigmoid(x)

def broken_lab02_recompilation_storm(models_compiled, shapes: list):
    # BUG: Every new shape triggers expensive recompilation without dynamic shape markup
    compile_counts = 0
    for s in shapes:
        x = torch.randn(s, 64)
        # Without dynamic shapes, each distinct batch size recompiles
        compile_counts += 1
    return compile_counts

def broken_lab03_constant_folding(graph_dict: dict) -> dict:
    # BUG: In-place mutation of input graph dictionary causes side effects on shared references
    graph_dict["folded"] = True
    return graph_dict

def broken_lab04_dead_node_pruning(nodes: list, outputs: list) -> list:
    # BUG: Blindly deletes all nodes with no consumers, including logging or state-mutating ops
    pruned = [n for n in nodes if n["name"] in outputs]
    return pruned

def broken_lab05_fusion_dtype(a: torch.Tensor, b: torch.Tensor) -> torch.dtype:
    # BUG: Silently promotes FP16 inputs to FP32 accumulator and fails to downcast
    acc = a.to(torch.float32) + b.to(torch.float32)
    return acc.dtype # Returns float32 instead of requested float16!

# ----------------- KERNEL LABS -----------------
def broken_lab06_strided_access(matrix: np.ndarray) -> float:
    # BUG: Accessing column-wise in row-major matrix destroys cache line prefetching
    rows, cols = matrix.shape
    total = 0.0
    for j in range(cols):
        for i in range(rows):
            total += matrix[i, j]
    return total

def broken_lab07_out_of_bounds_mask(n_elements: int, block_size: int = 64) -> list:
    # BUG: Strict equality mask == instead of < leaves trailing elements unmasked
    offsets = list(range(block_size))
    # Buggy mask: misses boundary check
    mask = [o == n_elements for o in offsets]
    return mask

def broken_lab08_fp16_underflow(logits: torch.Tensor) -> torch.Tensor:
    # BUG: Missing max-subtraction stabilization causes exp(-100) to underflow to 0 in FP16
    unstable_exp = torch.exp(logits.to(torch.float16))
    return unstable_exp / torch.sum(unstable_exp)

def broken_lab09_shared_memory_race() -> bool:
    # BUG: Simultaneous thread writes to shared address without atomic add or barrier
    return True # Race condition demonstrated

def broken_lab10_missing_sync() -> float:
    # BUG: Reading timer before CUDA stream synchronization yields misleading near-zero time
    t0 = time.perf_counter()
    # Mock GPU async dispatch (not synchronized)
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0 # ~0.001 ms false latency!

# ----------------- TRAINING LABS -----------------
def broken_lab11_omitted_zero_grad(model, x, y, optimizer, criterion) -> list:
    # BUG: Omitted optimizer.zero_grad() causes gradients to explode across steps
    grads = []
    for _ in range(3):
        out = model(x)
        loss = criterion(out, y)
        loss.backward()
        optimizer.step()
        # OMITTED: optimizer.zero_grad()
        grads.append(model.fc1.weight.grad.norm().item())
    return grads

def broken_lab12_learning_rate_explosion(weight: torch.Tensor) -> bool:
    # BUG: Extreme learning rate (1e4) causes weights to immediately become NaN
    lr = 10000.0
    grad = torch.tensor([5.0])
    weight.data.add_(grad, alpha=-lr)
    loss = (weight ** 2).sum()
    return torch.isnan(loss).item() or torch.isinf(loss).item()

def broken_lab13_detached_gradient(w: torch.Tensor, x: torch.Tensor) -> bool:
    # BUG: .detach() cuts backward computational chain
    h = (w * x).detach()
    loss = (h - 5.0) ** 2
    return loss.requires_grad is False

def broken_lab14_adamw_bias_uncorrected(step: int, beta1: float = 0.9) -> float:
    # BUG: Omitting 1 - beta1^t causes step size to be severely decayed on step 1 (0.1x of expected)
    correction = 1.0 # Omitted correction
    return correction

def broken_lab15_checkpoint_rng_drift() -> Tuple[float, float]:
    # BUG: Resumes model weights but does not restore torch RNG state
    torch.manual_seed(42)
    val1 = torch.randn(1).item()
    # Checkpoint restore without torch.set_rng_state()
    val2 = torch.randn(1).item()
    return val1, val2

# ----------------- FINE-TUNING LABS -----------------
def broken_lab16_eval_contamination(train_set: list, test_set: list) -> bool:
    # BUG: 100% test set contamination in training data
    return test_set[0] in train_set

def broken_lab17_chat_template_mismatch(messages: list) -> str:
    # BUG: Encodes ChatML with wrong Llama-3 special token syntax
    return "### Instruction:\n" + messages[0]["content"]

def broken_lab18_lora_unattached(named_modules: list, target_modules: list) -> int:
    # BUG: Target module names do not match actual architecture layers
    attached = [m for m in named_modules if m in target_modules]
    return len(attached) # 0 attached!

def broken_lab19_sequence_truncation(answers: list, cutoff: int = 10) -> int:
    # BUG: Aggressive cutoff truncates valid responses mid-sentence
    truncated = [a[:cutoff] for a in answers]
    return sum(len(t) < len(a) for t, a in zip(truncated, answers))

def broken_lab20_catastrophic_forgetting(baseline_general_score: float, finetuned_score: float) -> bool:
    # BUG: General capability regresses > 50%
    return finetuned_score < (baseline_general_score * 0.5)

# ----------------- SERVING LABS -----------------
def broken_lab21_static_batching(lengths: list) -> int:
    # BUG: Batch finishes at max length, forcing short requests to wait
    return max(lengths)

def broken_lab22_kv_cache_collision(base_addr: int, req1_len: int) -> int:
    # BUG: Assigns same base address to second request without offsetting
    req2_addr = base_addr # Collision!
    return req2_addr

def broken_lab23_continuous_starvation(queue: list) -> list:
    # BUG: Scheduler starvations: never schedules decode if prefill queue is non-empty
    return [q for q in queue if q.get("is_prefill")]

def broken_lab24_quant_asymmetric_scale(val_min: float, val_max: float) -> float:
    # BUG: Divides by 127 instead of 255 for uint8 asymmetric range
    return (val_max - val_min) / 127.0

def broken_lab25_speculative_vocab_mismatch(draft_vocab_size: int, target_vocab_size: int) -> bool:
    # BUG: Vocabularies differ; token IDs map to different words
    return draft_vocab_size != target_vocab_size

# ----------------- RETRIEVAL LABS -----------------
def broken_lab26_lexical_miss(query: str, doc: str) -> bool:
    # BUG: Exact keyword match fails on synonyms
    return query in doc

def broken_lab27_chunk_boundary(text: str, chunk_size: int = 50) -> list:
    # BUG: Arbitrary character split severs sentences in half
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def broken_lab28_metadata_drop(tenant_str: str, record_tenant_int: int) -> bool:
    # BUG: Comparing string '10' to int 10 fails in Python without casting
    return tenant_str == record_tenant_int # False!

def broken_lab29_inverted_similarity(scores: list) -> list:
    # BUG: Returns lowest similarity chunks first
    return sorted(scores)

def broken_lab30_hallucinated_citation(retrieved_docs_count: int, cited_doc_id: int) -> bool:
    # BUG: Cites doc 4 when only 2 were retrieved
    return cited_doc_id > retrieved_docs_count

# ----------------- AGENT LOOPS LABS -----------------
def broken_lab31_infinite_tool_loop(call_history: list) -> bool:
    # BUG: Same query executed 10 times consecutively
    return len(call_history) >= 10 and len(set(call_history)) == 1

def broken_lab32_unvalidated_int(arg: int) -> bool:
    # BUG: Accepts negative or multi-billion integer
    return arg > 10_000_000

def broken_lab33_json_double_escape(raw_str: str) -> bool:
    # BUG: Naive regex crashes on escaped quotes
    try:
        json.loads(raw_str)
        return False
    except json.JSONDecodeError:
        return True

def broken_lab34_tool_timeout_unhandled(tool_hangs: bool) -> str:
    if tool_hangs:
        # BUG: Hangs process indefinitely without timeout wrapper
        raise TimeoutError("Tool blocked forever")
    return "OK"

def broken_lab35_memory_overwrite(memory_dict: dict, key: str, old_val: str, new_val: str) -> str:
    # BUG: Stale sync overwrites fresh user update
    memory_dict[key] = old_val
    return memory_dict[key]

# ----------------- SECURITY & RELIABILITY LABS -----------------
def broken_lab36_indirect_injection(untrusted_doc: str) -> str:
    # BUG: Untrusted retrieved text concatenated directly into instructions
    return f"System Instruction:\n{untrusted_doc}"

def broken_lab37_double_charge(charge_calls: list) -> int:
    # BUG: Retrying payment without idempotency key causes 2 transactions
    charge_calls.append("charge_processed")
    charge_calls.append("charge_processed")
    return len(charge_calls)

def broken_lab38_multi_tenant_leak(query: str) -> bool:
    # BUG: SELECT statement omits WHERE tenant_id = ?
    return "WHERE tenant_id" not in query

def broken_lab39_secret_in_trace(headers: dict) -> str:
    # BUG: Logs raw Authorization Bearer token to telemetry
    return f"Span: {headers.get('Authorization')}"

def broken_lab40_thundering_herd(retries: int) -> list:
    # BUG: Synchronous retry without exponential backoff or jitter
    return [1.0 for _ in range(retries)]
