# HDM Optimizer - H. Dilpriya's Momentum

[![PyPI version](https://badge.fury.io/py/hdm-optimizer.svg)](https://badge.fury.io/py/hdm-optimizer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

**H. Dilpriya's Momentum (HDM)** is a multi-strategy gradient-aligned optimizer with proven convergence guarantees for deep learning.

*A tribute to Ms. Hirushi Dilpriya Thilakarathne*

## 🏆 Key Features

- **Adaptive Gamma Scheduling**: Warmup + cosine annealing for stable training
- **Alignment-Weighted Momentum**: Boosts momentum when gradients are consistent
- **EMA Smoothing**: Prevents oscillations from noisy gradients
- **Combined Correction**: Balances instant and smoothed alignment signals
- **O(n) Complexity**: <5% overhead vs standard momentum
- **Proven Convergence**: O(κ log(1/ε)) for strongly convex functions

## 📊 Performance

| Benchmark | Metric | HDM Rank | HDM Score | Best Score |
|-----------|--------|----------|-----------|------------|
| MNIST | Gradient Alignment | 🏆 #1 | 8.22% | 8.22% (HDM) |
| MNIST | Test Accuracy | ✅ #2 | 98.22% | 98.30% |
| CIFAR-10 | Test Accuracy | ✅ #2 | 83.94% | 85.69% |
| Synthetic (κ=1000) | Convergence | ✅ #2 | 140 iters | 107 iters |

## 🚀 Installation

**Install and view welcome banner (one-liner):**
```bash
pip install hdm-optimizer && python -m hdm_optimizer --version
```

**Or install only:**
```bash
pip install hdm-optimizer
```

## 📖 Quick Start

```python
import torch
import torch.nn as nn
from hdm_optimizer import HDMOptimizer

# Define your model
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Linear(256, 10)
)

# Initialize HDM optimizer
optimizer = HDMOptimizer(
    model.parameters(),
    lr=0.01,           # Learning rate
    beta=0.9,          # Momentum coefficient
    gamma=2.0,         # Correction coefficient (2.0 for accuracy, 1.5 for alignment)
    warmup_steps=1000, # Warmup period
    total_steps=10000  # Total training steps (for cosine annealing)
)

# Training loop
for epoch in range(num_epochs):
    for batch in dataloader:
        optimizer.zero_grad()
        loss = criterion(model(batch.x), batch.y)
        loss.backward()
        optimizer.step()
```

## 🎯 Parameter Recommendations

### Classification Tasks (MNIST, CIFAR-10)
```python
optimizer = HDMOptimizer(
    model.parameters(),
    lr=0.01,              # 0.01 for MLP, 0.1 for CNN/ResNet
    beta=0.9,
    gamma=2.0,            # Higher for accuracy optimization
    warmup_steps=epoch_steps // 10,  # 10% of total steps
    total_steps=epoch_steps * num_epochs,
    alignment_ema=0.95
)
```

### Gradient Alignment Tasks
```python
optimizer = HDMOptimizer(
    model.parameters(),
    lr=0.01,
    beta=0.9,
    gamma=1.5,            # Lower for stability
    warmup_steps=1000,
    total_steps=10000,
    alignment_ema=0.95
)
```

## 🔍 Version Check

Display the HDM banner with version information:

```bash
python -m hdm_optimizer --version
```

Output:
```
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                     A Tribute to Ms. Hirushi Dilpriya Thilakarathne
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

                                        ██╗  ██╗ ██████╗  ███╗   ███╗
                                        ██║  ██║ ██╔══██╗ ████╗ ████║
                                        ███████║ ██║  ██║ ██╔████╔██║
                                        ██╔══██║ ██║  ██║ ██║╚██╔╝██║
                                        ██║  ██║ ██████╔╝ ██║ ╚═╝ ██║
                                        ╚═╝  ╚═╝ ╚═════╝  ╚═╝     ╚═╝

                           H. Dilpriya's Momentum (HDM) Multi-Strategy Gradient Optimizer
                                   Hirushi Dilpriya Momentum (HDM) | Version 3.0.0

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
```

## 📚 Algorithm Details

HDM implements four key strategies:

1. **Adaptive Gamma Scheduling**:
   ```
   γ_t = γ_base × warmup_factor × annealing_factor
   ```

2. **Alignment-Weighted Momentum**:
   ```
   m_t = β·m_{t-1} + (1 + 0.3·alignment_weight)·g_t
   ```

3. **EMA Smoothing**:
   ```
   alignment_ema_t = 0.95·alignment_ema_{t-1} + 0.05·cos_similarity_t
   ```

4. **Combined Correction**:
   ```
   correction = γ_t × (0.3·instant + 0.7·smoothed) × g_t
   ```

## 🎓 Citation

If you use HDM in your research, please cite:

```bibtex
@software{hdm_optimizer_2025,
  title={H. Dilpriya's Momentum (HDM): Multi-Strategy Gradient-Aligned Optimizer},
  author={H. Dilpriya Research Team},
  year={2025},
  note={A tribute to Ms. Hirushi Dilpriya Thilakarathne}
}
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

This work is dedicated to **Ms. Hirushi Dilpriya Thilakarathne**, whose profound expertise in pure mathematics and deep learning inspired this research.

### Research Team

**Developer:** Janaka Ishan Senarathna

**Research Supervisor:** Ms. Hirushi Dilpriya Thilakarathne
- 🎓 Expert in Pure Mathematics and Deep Learning
- 🏆 Supervisor of the HDM Optimizer Research Project
- 🔗 Profile: [LinkedIn](https://www.linkedin.com/in/hirushi-dilpriya-a5498a215/) | [Google Scholar](https://scholar.google.com/citations?user=6B8J9eYAAAAJ&hl=en&oi=ao)

This optimizer is named in her honor, recognizing her invaluable guidance and mentorship throughout the development of the multi-strategy gradient alignment techniques.

## 🔗 Links

- **Documentation**: [GitHub Wiki](https://github.com/Janakaishansenarathna/HDM-Optimizer/wiki)
- **Issues**: [GitHub Issues](https://github.com/Janakaishansenarathna/HDM-Optimizer/issues)
- **PyPI**: [hdm-optimizer](https://pypi.org/project/hdm-optimizer/)

## 📝 Requirements

- Python >= 3.7
- PyTorch >= 1.10.0

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Built with ❤️ by the Janaka Ishan Senarathna**
#
