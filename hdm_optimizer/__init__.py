"""
H. Dilpriya Momentum (HDM) Optimizer
Multi-Strategy Gradient-Aligned Optimizer with Convergence Guarantees

A tribute to Ms. Hirushi Dilpriya Thilakarathne
"""

from .optimizer import HDMOptimizer
from .__version__ import (
    __version__,
    __author__,
    __description__,
    __url__,
    __license__
)

__all__ = ['HDMOptimizer']
