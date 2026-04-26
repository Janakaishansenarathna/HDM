"""
Simple synthetic quadratic optimization example with HDM Optimizer
"""
import torch
from hdm_optimizer import HDMOptimizer


def create_quadratic_problem(n=50, kappa=100):
    """
    Create a quadratic optimization problem: L(θ) = 0.5 * θ^T H θ
    
    Args:
        n: Dimension
        kappa: Condition number
    
    Returns:
        H: Positive definite matrix
        theta_star: Optimal solution (zeros)
    """
    # Create eigenvalues with specific condition number
    lambda_min = 1.0
    lambda_max = kappa * lambda_min
    eigenvalues = torch.linspace(lambda_min, lambda_max, n)
    
    # Create random orthogonal matrix
    Q, _ = torch.qr(torch.randn(n, n))
    
    # H = Q * diag(eigenvalues) * Q^T
    H = Q @ torch.diag(eigenvalues) @ Q.t()
    
    theta_star = torch.zeros(n)
    
    return H, theta_star


def compute_gradient(theta, H):
    """Compute gradient: ∇L(θ) = H @ θ"""
    return H @ theta


def compute_loss(theta, H):
    """Compute loss: L(θ) = 0.5 * θ^T H θ"""
    return 0.5 * theta @ H @ theta


def optimize_quadratic(kappa=100, max_iters=1000, tolerance=1e-6):
    """
    Optimize quadratic function with HDM
    
    Args:
        kappa: Condition number
        max_iters: Maximum iterations
        tolerance: Convergence tolerance
    """
    print(f"\n{'='*60}")
    print(f"Optimizing Quadratic Problem (κ={kappa})")
    print(f"{'='*60}")
    
    # Setup problem
    n = 50
    H, theta_star = create_quadratic_problem(n, kappa)
    
    # Initialize parameter
    theta = torch.randn(n) * 10.0  # Random start
    theta.requires_grad = True
    
    # HDM Optimizer
    optimizer = HDMOptimizer(
        [theta],
        lr=0.01,
        beta=0.9,
        gamma=2.0,
        warmup_steps=100,
        total_steps=max_iters
    )
    
    print(f"Initial loss: {compute_loss(theta.data, H).item():.6f}")
    print(f"Initial ||θ||: {theta.data.norm().item():.6f}\n")
    
    # Optimize
    for iteration in range(max_iters):
        optimizer.zero_grad()
        
        # Compute loss and gradient
        loss = compute_loss(theta, H)
        loss.backward()
        
        optimizer.step()
        
        # Check convergence
        with torch.no_grad():
            error = (theta - theta_star).norm().item()
            
            if (iteration + 1) % 10 == 0:
                print(f"Iter {iteration+1:4d} | Loss: {loss.item():.8f} | "
                      f"||θ - θ*||: {error:.8f}")
            
            if error < tolerance:
                print(f"\n✓ Converged in {iteration+1} iterations!")
                print(f"  Final loss: {loss.item():.10f}")
                print(f"  Final error: {error:.10f}")
                return iteration + 1
    
    print(f"\n✗ Did not converge within {max_iters} iterations")
    print(f"  Final error: {error:.10f}")
    return max_iters


if __name__ == '__main__':
    print("\n" + "="*60)
    print("HDM Optimizer - Synthetic Quadratic Optimization")
    print("="*60)
    
    # Test on different condition numbers
    for kappa in [10, 100, 1000]:
        iters = optimize_quadratic(kappa=kappa)
        print(f"\nCondition number κ={kappa}: {iters} iterations\n")
