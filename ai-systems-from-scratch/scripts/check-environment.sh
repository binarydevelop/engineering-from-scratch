#!/usr/bin/env bash
# AI Systems From Scratch - Environment Checker
set -euo pipefail

echo "=========================================================="
echo "  AI Systems From Scratch - System Environment Check"
echo "=========================================================="
echo "Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "OS: $(uname -s) $(uname -r) ($(uname -m))"

PYTHON_BIN=".venv/bin/python"
if [ ! -f "$PYTHON_BIN" ]; then
    PYTHON_BIN="python3"
fi

echo "Python Executable: $(which $PYTHON_BIN || echo "$PYTHON_BIN")"
$PYTHON_BIN --version

$PYTHON_BIN -c "
import sys
import platform

print('Python Version:', platform.python_version())
print('Platform:', platform.platform())

# PyTorch Check
try:
    import torch
    print('PyTorch Version:', torch.__version__)
    print('CUDA Available:', torch.cuda.is_available())
    if torch.cuda.is_available():
        print('  CUDA Device Count:', torch.cuda.device_count())
        print('  Device Name:', torch.cuda.get_device_name(0))
        print('  CUDA Capability:', torch.cuda.get_device_capability(0))
    mps_available = hasattr(torch.backends, 'mps') and torch.backends.mps.is_available()
    print('Apple MPS Available:', mps_available)
except ImportError:
    print('PyTorch: NOT INSTALLED')

# Hugging Face Ecosystem Check
for pkg in ['transformers', 'peft', 'trl', 'accelerate', 'datasets', 'pydantic']:
    try:
        mod = __import__(pkg)
        ver = getattr(mod, '__version__', 'unknown')
        print(f'{pkg}: {ver}')
    except ImportError:
        print(f'{pkg}: NOT INSTALLED')

# Triton Check (Linux only)
try:
    import triton
    print('Triton Version:', triton.__version__)
except ImportError:
    print('Triton: NOT INSTALLED (Expected on macOS/CPU environments; Triton is required only for Linux/CUDA Tier 2/3)')
"

echo "----------------------------------------------------------"
echo "Environment check complete."
