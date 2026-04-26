# HDM Optimizer API Reference

## HDMOptimizer

```python
from hdm_optimizer import HDMOptimizer
```

### Class: `HDMOptimizer`

Multi-strategy gradient-aligned optimizer with convergence guarantees.

**Inherits from:** `torch.optim.Optimizer`

---

### Constructor

```python
HDMOptimizer(
    params,
    lr=0.01,
    beta=0.9,
    gamma=2.0,
    warmup_steps=100,
    total_steps=None,
    alignment_ema=0.95,
    eps=1e-8
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `params` | iterable | *required* | Iterable of parameters to optimize or dicts defining parameter groups |
| `lr` | float | 0.01 | Learning rate (α) |
| `beta` | float | 0.9 | Momentum coefficient (β). Must be in [0, 1) |
| `gamma` | float | 2.0 | Base correction coefficient (γ). Use 2.0 for accuracy tasks, 1.5 for alignment tasks |
| `warmup_steps` | int | 100 | Number of steps to gradually increase correction strength. Typically 10% of total steps |
| `total_steps` | int | None | Total training steps for cosine annealing. If None, uses constant annealing factor |
| `alignment_ema` | float | 0.95 | EMA coefficient for smoothing alignment signal. Higher values = more stability |
| `eps` | float | 1e-8 | Small constant for numerical stability |

#### Raises

- `ValueError`: If `lr < 0`
- `ValueError`: If `beta` not in [0, 1)
- `ValueError`: If `gamma < 0`
- `ValueError`: If `alignment_ema` not in (0, 1)
- `ValueError`: If `eps <= 0`

---

### Methods

#### `step(closure=None)`

Performs a single optimization step.

**Parameters:**
- `closure` (callable, optional): A closure that reevaluates the model and returns the loss

**Returns:**
- Loss value if closure is provided, otherwise None

**Example:**
```python
optimizer.zero_grad()
loss = criterion(model(input), target)
loss.backward()
optimizer.step()
```

#### `zero_grad(set_to_none=False)`

Clears gradients of all optimized parameters. Inherited from `torch.optim.Optimizer`.

**Parameters:**
- `set_to_none` (bool, optional): If True, set gradients to None instead of zero

#### `state_dict()`

Returns the state of the optimizer as a dict. Inherited from `torch.optim.Optimizer`.

#### `load_state_dict(state_dict)`

Loads the optimizer state. Inherited from `torch.optim.Optimizer`.

**Parameters:**
- `state_dict` (dict): Optimizer state (returned from `state_dict()`)

---

## Usage Examples

### Basic Usage

```python
import torch
import torch.nn as nn
from hdm_optimizer import HDMOptimizer

# Create model
model = nn.Linear(10, 1)

# Create optimizer
optimizer = HDMOptimizer(model.parameters(), lr=0.01, gamma=2.0)

# Training step
optimizer.zero_grad()
output = model(input)
loss = criterion(output, target)
loss.backward()
optimizer.step()
```

### MNIST Classification

```python
from hdm_optimizer import HDMOptimizer

# Model setup
model = MyMNISTModel()
criterion = nn.CrossEntropyLoss()

# Calculate total steps
num_epochs = 50
steps_per_epoch = len(train_loader)
total_steps = num_epochs * steps_per_epoch

# Create optimizer with warmup
optimizer = HDMOptimizer(
    model.parameters(),
    lr=0.01,
    beta=0.9,
    gamma=2.0,  # For accuracy optimization
    warmup_steps=total_steps // 10,  # 10% warmup
    total_steps=total_steps,
    alignment_ema=0.95
)

# Training loop
for epoch in range(num_epochs):
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
```

### Parameter Groups

```python
# Different learning rates for different layers
optimizer = HDMOptimizer([
    {'params': model.layer1.parameters(), 'lr': 0.001},
    {'params': model.layer2.parameters(), 'lr': 0.01}
], gamma=2.0)
```

### Saving and Loading

```python
# Save optimizer state
checkpoint = {
    'model': model.state_dict(),
    'optimizer': optimizer.state_dict(),
}
torch.save(checkpoint, 'checkpoint.pth')

# Load optimizer state
checkpoint = torch.load('checkpoint.pth')
model.load_state_dict(checkpoint['model'])
optimizer.load_state_dict(checkpoint['optimizer'])
```

---

## Algorithm Details

HDM implements four key strategies:

### 1. Adaptive Gamma Scheduling

```python
warmup_factor = min(1.0, step / warmup_steps)
annealing_factor = 0.5 + 0.5 * cos(π * step / total_steps)
γ_t = γ_base × warmup_factor × annealing_factor
```

### 2. Gradient Alignment

```python
cos_similarity = <g_t, g_{t-1}> / (||g_t|| × ||g_{t-1}|| + ε)
```

### 3. EMA Smoothing

```python
alignment_ema_t = ρ × alignment_ema_{t-1} + (1-ρ) × cos_similarity_t
```

### 4. Alignment-Weighted Momentum

```python
alignment_weight = max(0, alignment_ema)
m_t = β × m_{t-1} + (1 + 0.3 × alignment_weight) × g_t
```

### Update Rule

```python
combined_alignment = 0.3 × cos_similarity + 0.7 × alignment_ema
correction = γ_t × combined_alignment × g_t
θ_{t+1} = θ_t - α × (m_t + correction)
```

---

## Performance Guidelines

### Classification Tasks

**Recommended Settings:**
- `lr`: 0.01 (MLP), 0.1 (CNN/ResNet)
- `gamma`: 2.0
- `warmup_steps`: 10% of total steps
- `alignment_ema`: 0.95

**Expected Performance:**
- MNIST: ~98.2% accuracy (rank #2)
- CIFAR-10: ~84% accuracy (rank #2)

### Gradient Alignment Optimization

**Recommended Settings:**
- `lr`: 0.01
- `gamma`: 1.5 (reduced for stability)
- `warmup_steps`: 10% of total steps
- `alignment_ema`: 0.95

**Expected Performance:**
- Gradient alignment: 8-11% (rank #1)

### Ill-Conditioned Problems

**Recommended Settings:**
- `lr`: 0.01
- `gamma`: 2.0
- `warmup_steps`: 5-10% of expected convergence steps
- `total_steps`: Estimate of convergence iterations

**Expected Performance:**
- Converges on κ=1000 problems (rank #2)
- Stable across varying condition numbers

---

## Computational Complexity

- **Time per step:** O(n) where n = number of parameters
- **Memory overhead:** O(n) for momentum, previous gradient, and scalar states
- **Overhead vs standard momentum:** <5%

---

## State Variables

Each parameter maintains the following state:

| Variable | Type | Description |
|----------|------|-------------|
| `step` | int | Current step counter |
| `momentum` | Tensor | Momentum buffer (m_t) |
| `prev_grad` | Tensor | Previous gradient (g_{t-1}) |
| `alignment_ema` | float | EMA of gradient alignment |

---

## Convergence Theory

**Theorem (H. Dilpriya's Convergence Theorem):**

For μ-strongly convex functions with L-Lipschitz continuous gradients:

```
||θ_t - θ*|| ≤ ρ^t × ||θ_0 - θ*||
```

where ρ = 1 - μα/4 < 1.

**Iteration Complexity:** O(κ log(1/ε))

where κ = L/μ is the condition number.

---

## Troubleshooting

### Optimizer not converging

**Solution:** Reduce learning rate or increase warmup steps

```python
optimizer = HDMOptimizer(params, lr=0.001, warmup_steps=2000)
```

### Loss oscillating

**Solution:** Increase alignment EMA for more stability

```python
optimizer = HDMOptimizer(params, alignment_ema=0.99)
```

### Slower than expected

**Solution:** Reduce correction coefficient

```python
optimizer = HDMOptimizer(params, gamma=1.0)
```

### Memory issues

**Solution:** HDM requires O(n) extra memory. If this is an issue, consider gradient checkpointing or reducing model size.

---

## Version Information

Display version and information:

```bash
python -m hdm_optimizer --version
```

Check version programmatically:

```python
import hdm_optimizer
print(hdm_optimizer.__version__)
```

---

## Citation

```bibtex
@software{hdm_optimizer_2025,
  title={H. Dilpriya's Momentum (HDM): Multi-Strategy Gradient-Aligned Optimizer},
  author={H. Dilpriya Research Team},
  year={2025},
  note={A tribute to Ms. Hirushi Dilpriya Thilakarathne}
}
```

---

**A Tribute to Ms. Hirushi Dilpriya Thilakarathne**
