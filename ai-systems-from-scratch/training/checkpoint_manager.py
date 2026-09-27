"""
Atomic Checkpointing & State Restoration (Phases 79-80).
Saves and restores complete training state:
- Model state dict
- Optimizer state dict
- Step counter and loss metrics
- PyTorch RNG state and NumPy random state
Ensures fault tolerance during multi-day fine-tuning runs.
"""

import os
import torch
import numpy as np
from typing import Dict, Any

class CheckpointManager:
    def __init__(self, checkpoint_dir: str = "outputs/checkpoints"):
        self.checkpoint_dir = checkpoint_dir
        os.makedirs(checkpoint_dir, exist_ok=True)

    def save_checkpoint(
        self,
        step: int,
        model: torch.nn.Module,
        optimizer: Any,
        metrics: Dict[str, float]
    ) -> str:
        checkpoint_path = os.path.join(self.checkpoint_dir, f"checkpoint_step_{step}.pt")
        tmp_path = checkpoint_path + ".tmp"

        state = {
            "step": step,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict() if hasattr(optimizer, "state_dict") else {},
            "metrics": metrics,
            "torch_rng_state": torch.get_rng_state(),
            "numpy_rng_state": np.random.get_state()
        }

        # Atomic write: write to temp file then rename
        torch.save(state, tmp_path)
        os.replace(tmp_path, checkpoint_path)
        return checkpoint_path

    def load_checkpoint(
        self,
        checkpoint_path: str,
        model: torch.nn.Module,
        optimizer: Any = None
    ) -> Dict[str, Any]:
        state = torch.load(checkpoint_path, weights_only=False)
        model.load_state_dict(state["model_state_dict"])
        if optimizer and "optimizer_state_dict" in state and hasattr(optimizer, "load_state_dict"):
            optimizer.load_state_dict(state["optimizer_state_dict"])
        torch.set_rng_state(state["torch_rng_state"])
        np.random.set_state(state["numpy_rng_state"])
        return {
            "step": state["step"],
            "metrics": state["metrics"]
        }
