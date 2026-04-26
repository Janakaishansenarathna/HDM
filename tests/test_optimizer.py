"""Unit tests for HDMOptimizer"""
import unittest
import torch
import torch.nn as nn
from hdm_optimizer import HDMOptimizer


class TestHDMOptimizer(unittest.TestCase):
    """Test cases for HDM Optimizer"""
    
    def setUp(self):
        """Set up test fixtures"""
        torch.manual_seed(42)
        self.model = nn.Linear(10, 1)
        self.x = torch.randn(32, 10)
        self.y = torch.randn(32, 1)
    
    def test_initialization(self):
        """Test optimizer initialization"""
        optimizer = HDMOptimizer(self.model.parameters(), lr=0.01)
        self.assertIsNotNone(optimizer)
    
    def test_parameter_validation(self):
        """Test parameter validation"""
        with self.assertRaises(ValueError):
            HDMOptimizer(self.model.parameters(), lr=-0.01)
        
        with self.assertRaises(ValueError):
            HDMOptimizer(self.model.parameters(), beta=1.5)
        
        with self.assertRaises(ValueError):
            HDMOptimizer(self.model.parameters(), alignment_ema=1.5)
    
    def test_step(self):
        """Test single optimization step"""
        optimizer = HDMOptimizer(self.model.parameters(), lr=0.01)
        
        # Forward pass
        output = self.model(self.x)
        loss = nn.MSELoss()(output, self.y)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        
        # Get initial parameters
        initial_params = [p.clone() for p in self.model.parameters()]
        
        # Step
        optimizer.step()
        
        # Check parameters changed
        for initial, current in zip(initial_params, self.model.parameters()):
            self.assertFalse(torch.equal(initial, current))
    
    def test_convergence_simple(self):
        """Test convergence on simple problem"""
        # Create simple linear problem
        torch.manual_seed(42)
        true_w = torch.randn(10, 1)
        x = torch.randn(100, 10)
        y = x @ true_w
        
        model = nn.Linear(10, 1, bias=False)
        optimizer = HDMOptimizer(model.parameters(), lr=0.01, gamma=2.0)
        
        initial_loss = nn.MSELoss()(model(x), y).item()
        
        # Train
        for _ in range(100):
            optimizer.zero_grad()
            loss = nn.MSELoss()(model(x), y)
            loss.backward()
            optimizer.step()
        
        final_loss = nn.MSELoss()(model(x), y).item()
        
        # Loss should decrease
        self.assertLess(final_loss, initial_loss)
        self.assertLess(final_loss, 1e-3)
    
    def test_warmup_schedule(self):
        """Test warmup scheduling"""
        optimizer = HDMOptimizer(
            self.model.parameters(),
            lr=0.01,
            warmup_steps=10,
            total_steps=100
        )
        
        # Run a few steps and check state
        for i in range(20):
            output = self.model(self.x)
            loss = nn.MSELoss()(output, self.y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            # Check step counter
            for group in optimizer.param_groups:
                for p in group['params']:
                    if p.grad is not None:
                        state = optimizer.state[p]
                        self.assertEqual(state['step'], i + 1)
    
    def test_state_dict(self):
        """Test state dict save/load"""
        optimizer1 = HDMOptimizer(self.model.parameters(), lr=0.01)
        
        # Run a step
        output = self.model(self.x)
        loss = nn.MSELoss()(output, self.y)
        optimizer1.zero_grad()
        loss.backward()
        optimizer1.step()
        
        # Save state
        state_dict = optimizer1.state_dict()
        
        # Create new optimizer and load state
        optimizer2 = HDMOptimizer(self.model.parameters(), lr=0.01)
        optimizer2.load_state_dict(state_dict)
        
        # States should match
        self.assertEqual(
            optimizer1.state[list(self.model.parameters())[0]]['step'],
            optimizer2.state[list(self.model.parameters())[0]]['step']
        )


if __name__ == '__main__':
    unittest.main()
