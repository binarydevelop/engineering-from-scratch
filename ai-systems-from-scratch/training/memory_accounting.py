"""
Training Memory Accounting & Budgeting (Phase 75).
Computes exact theoretical VRAM memory consumption across:
1. Model Parameters (Weights)
2. Gradients
3. Optimizer States (AdamW: 8 bytes per parameter in FP32)
4. Activation Memory
"""

from typing import Dict

def compute_training_memory(
    num_parameters: int,
    dtype_bytes: int = 2, # 2 for FP16/BF16, 4 for FP32
    optimizer: str = "adamw",
    batch_size: int = 4,
    seq_len: int = 2048,
    hidden_dim: int = 4096,
    num_layers: int = 32
) -> Dict[str, float]:
    """Calculates breakdown in Megabytes and Gigabytes."""
    # 1. Weights
    weight_bytes = num_parameters * dtype_bytes
    
    # 2. Gradients
    gradient_bytes = num_parameters * dtype_bytes
    
    # 3. Optimizer State
    # AdamW stores 1st moment (FP32: 4 bytes) + 2nd moment (FP32: 4 bytes) + master weights (4 bytes if mixed precision)
    if optimizer.lower() == "adamw":
        # Standard mixed precision AdamW stores 8 bytes (m and v in FP32) + 4 bytes FP32 master weight copy = 12-16 bytes/param
        optimizer_bytes = num_parameters * 12
    elif optimizer.lower() == "sgd_momentum":
        optimizer_bytes = num_parameters * 4
    else: # Vanilla SGD
        optimizer_bytes = 0

    # 4. Activation Memory (Rough approximation for standard Transformer layer)
    # Activations ~ num_layers * seq_len * batch_size * hidden_dim * (34 to 40 bytes)
    activation_bytes = num_layers * seq_len * batch_size * hidden_dim * 34

    total_bytes = weight_bytes + gradient_bytes + optimizer_bytes + activation_bytes

    return {
        "parameters_gb": weight_bytes / (1024 ** 3),
        "gradients_gb": gradient_bytes / (1024 ** 3),
        "optimizer_gb": optimizer_bytes / (1024 ** 3),
        "activations_gb": activation_bytes / (1024 ** 3),
        "total_gb": total_bytes / (1024 ** 3)
    }

if __name__ == "__main__":
    # 7B Model training accounting
    breakdown = compute_training_memory(num_parameters=7_000_000_000, dtype_bytes=2)
    print("7B Full Fine-Tuning Memory Breakdown (GB):", breakdown)
