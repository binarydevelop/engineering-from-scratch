import os
import sys
import pytest
import torch
import torch.nn as nn

sys.path.insert(0, os.path.dirname(__file__))

from manual_training_loop import run_manual_training_loop, TinyMLP
from cross_entropy_from_scratch import verify_cross_entropy, cross_entropy_scratch
from autograd_debugger import trace_backward_graph, demonstrate_gradient_block_bug
from custom_optimizers import CustomSGD, CustomAdamW
from gradient_accumulation import train_with_gradient_accumulation
from gradient_clipping import clip_grad_norm_scratch
from checkpoint_manager import CheckpointManager

def test_manual_training_loop():
    losses = run_manual_training_loop(epochs=3, lr=0.1)
    assert len(losses) == 3
    # Loss should decrease
    assert losses[-1] < losses[0]

def test_cross_entropy_stability():
    diff = verify_cross_entropy()
    assert diff < 1e-4

def test_autograd_debugger():
    assert demonstrate_gradient_block_bug() is True

def test_custom_optimizers():
    w = torch.tensor([5.0], requires_grad=True)
    opt = CustomAdamW([w], lr=0.1)
    
    # Run 5 optimization steps on loss = w^2
    for _ in range(5):
        loss = w ** 2
        loss.backward()
        opt.step()
        opt.zero_grad()
        
    assert abs(w.item()) < 5.0 # Value moved toward 0

def test_gradient_accumulation():
    model = TinyMLP()
    x = torch.randn(16, 8)
    y = torch.randint(0, 2, (16,))
    losses = train_with_gradient_accumulation(model, x, y, micro_batch_size=4, accumulation_steps=2)
    assert len(losses) == 4

def test_gradient_clipping():
    p = torch.tensor([1.0], requires_grad=True)
    p.grad = torch.tensor([100.0]) # Massive gradient
    norm = clip_grad_norm_scratch([p], max_norm=1.0)
    assert norm > 99.0
    assert p.grad.item() <= 1.01

def test_checkpointing(tmp_path):
    mgr = CheckpointManager(checkpoint_dir=str(tmp_path))
    model = TinyMLP()
    opt = torch.optim.SGD(model.parameters(), lr=0.01)

    ckpt_path = mgr.save_checkpoint(step=10, model=model, optimizer=opt, metrics={"loss": 0.42})
    assert os.path.exists(ckpt_path)

    new_model = TinyMLP()
    res = mgr.load_checkpoint(ckpt_path, model=new_model)
    assert res["step"] == 10
    assert res["metrics"]["loss"] == 0.42
