# Installation Guide for HDM Optimizer

## For Development and Testing (Local Installation)

### 1. Install in Development Mode

From the `hdm-optimizer` directory:

```bash
cd hdm-optimizer
pip install -e .
```

This installs the package in "editable" mode, so changes to the code are immediately reflected.

### 2. Test the Installation

**Display banner:**
```bash
python -m hdm_optimizer --version
```

**Test import:**
```python
from hdm_optimizer import HDMOptimizer
print("✓ Successfully imported HDMOptimizer")
```

**Run unit tests:**
```bash
python -m unittest tests.test_optimizer -v
```

**Run example:**
```bash
cd examples
python synthetic_example.py
```

---

## For Publishing to PyPI (Production)

### 1. Build the Package

```bash
pip install build twine
python -m build
```

This creates `dist/` folder with:
- `hdm_optimizer-3.0.0-py3-none-any.whl`
- `hdm_optimizer-3.0.0.tar.gz`

### 2. Test on TestPyPI (Optional)

```bash
twine upload --repository testpypi dist/*
```

Then test installation:
```bash
pip install --index-url https://test.pypi.org/simple/ hdm-optimizer
```

### 3. Upload to PyPI

```bash
twine upload dist/*
```

You'll need:
- PyPI account
- API token (recommended) or username/password

### 4. Users Can Install

After publishing:
```bash
pip install hdm-optimizer
```

---

## Quick Usage After Installation

```python
import torch
import torch.nn as nn
from hdm_optimizer import HDMOptimizer

# Create model
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Linear(256, 10)
)

# Initialize optimizer
optimizer = HDMOptimizer(
    model.parameters(),
    lr=0.01,
    beta=0.9,
    gamma=2.0,
    warmup_steps=1000,
    total_steps=10000
)

# Training loop
for epoch in range(num_epochs):
    optimizer.zero_grad()
    loss = criterion(model(x), y)
    loss.backward()
    optimizer.step()
```

---

## Verify Installation

```bash
# Show version banner
python -m hdm_optimizer --version

# Or in Python
python -c "from hdm_optimizer import HDMOptimizer; print('✓ HDM Optimizer installed!')"
```

---

## Requirements

- Python >= 3.7
- PyTorch >= 1.10.0

Install PyTorch:
```bash
pip install torch
```

---

## Troubleshooting

**Issue:** `ModuleNotFoundError: No module named 'hdm_optimizer'`

**Solution:** Install the package:
```bash
pip install -e .  # For development
# OR
pip install hdm-optimizer  # From PyPI
```

**Issue:** Banner not displaying

**Solution:** Make sure to run:
```bash
python -m hdm_optimizer --version
```

NOT just:
```bash
python hdm_optimizer --version
```

---

## Uninstall

```bash
pip uninstall hdm-optimizer
```
