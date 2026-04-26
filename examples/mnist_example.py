"""
Simple MNIST training example with HDM Optimizer
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from hdm_optimizer import HDMOptimizer


class SimpleNet(nn.Module):
    """Simple 3-layer MLP for MNIST"""
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 10)
    
    def forward(self, x):
        x = x.view(-1, 784)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def train():
    # Setup
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Data
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    train_dataset = datasets.MNIST('../data', train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST('../data', train=False, transform=transform)
    
    train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)
    
    # Model
    model = SimpleNet().to(device)
    
    # HDM Optimizer
    num_epochs = 50
    steps_per_epoch = len(train_loader)
    total_steps = num_epochs * steps_per_epoch
    
    optimizer = HDMOptimizer(
        model.parameters(),
        lr=0.01,
        beta=0.9,
        gamma=2.0,  # For accuracy optimization
        warmup_steps=total_steps // 10,  # 10% warmup
        total_steps=total_steps,
        alignment_ema=0.95
    )
    
    criterion = nn.CrossEntropyLoss()
    
    # Training
    print("Training MNIST with HDM Optimizer...")
    print(f"Device: {device}")
    print(f"Total steps: {total_steps}")
    
    for epoch in range(num_epochs):
        model.train()
        train_loss = 0
        correct = 0
        total = 0
        
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
        
        # Test
        model.eval()
        test_loss = 0
        test_correct = 0
        test_total = 0
        
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                test_loss += criterion(output, target).item()
                _, predicted = output.max(1)
                test_total += target.size(0)
                test_correct += predicted.eq(target).sum().item()
        
        print(f'Epoch {epoch+1}/{num_epochs} | '
              f'Train Loss: {train_loss/len(train_loader):.4f} | '
              f'Train Acc: {100.*correct/total:.2f}% | '
              f'Test Loss: {test_loss/len(test_loader):.4f} | '
              f'Test Acc: {100.*test_correct/test_total:.2f}%')
    
    print("\n✓ Training completed!")
    print(f"Final Test Accuracy: {100.*test_correct/test_total:.2f}%")


if __name__ == '__main__':
    train()
