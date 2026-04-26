"""Command-line interface for HDM Optimizer."""

import sys
from .banner import display_banner


def main():
    """Main CLI entry point."""
    if len(sys.argv) > 1 and sys.argv[1] in ['--version', '-v']:
        display_banner()
    else:
        print("HDM Optimizer - H. Dilpriya's Momentum")
        print("\nUsage:")
        print("  python -m hdm_optimizer --version    Show version and information")
        print("\nFor usage in Python:")
        print("  from hdm_optimizer import HDMOptimizer")
        print("  optimizer = HDMOptimizer(model.parameters(), lr=0.01, gamma=2.0)")


if __name__ == '__main__':
    main()
