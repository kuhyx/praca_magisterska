#!/bin/bash
# Install NVIDIA Nsight tools on Arch Linux
# This script installs Nsight Systems and Nsight Compute

set -e

echo "=== NVIDIA Nsight Installation Script for Arch Linux ==="
echo ""

# Check if running on Arch Linux
if [ ! -f /etc/arch-release ]; then
    echo "Error: This script is designed for Arch Linux."
    exit 1
fi

# Update system first
echo "=== Updating system packages ==="
sudo pacman -Syu --noconfirm

# Check NVIDIA drivers
echo ""
echo "=== Checking NVIDIA drivers ==="
if pacman -Qs nvidia-utils &> /dev/null; then
    echo "NVIDIA utils already installed."
else
    echo "Installing NVIDIA open drivers..."
    sudo pacman -S --needed --noconfirm nvidia-open nvidia-utils nvidia-settings
fi

# Install CUDA toolkit (optional but recommended)
echo ""
echo "=== Installing CUDA toolkit ==="
sudo pacman -S --needed --noconfirm cuda

# Install Nsight tools from official repositories
echo ""
echo "=== Installing NVIDIA Nsight tools ==="

echo ""
echo "Installing Nsight Systems (system-wide performance analysis)..."
sudo pacman -S --needed --noconfirm nsight-systems

echo ""
echo "Installing Nsight Compute (CUDA kernel profiling)..."
sudo pacman -S --needed --noconfirm nsight-compute

# Set up environment variables
echo ""
echo "=== Setting up environment variables ==="
CUDA_PATH="/opt/cuda"
if [ -d "$CUDA_PATH" ]; then
    # Add to .bashrc if not already present
    if ! grep -q "CUDA_HOME" ~/.bashrc 2>/dev/null; then
        echo "" >> ~/.bashrc
        echo "# NVIDIA CUDA and Nsight tools" >> ~/.bashrc
        echo "export CUDA_HOME=$CUDA_PATH" >> ~/.bashrc
        echo "export PATH=\$PATH:\$CUDA_HOME/bin" >> ~/.bashrc
        echo "Environment variables added to ~/.bashrc"
    else
        echo "CUDA environment variables already configured in .bashrc"
    fi
    
    # Add to .zshrc if zsh is used
    if [ -f ~/.zshrc ]; then
        if ! grep -q "CUDA_HOME" ~/.zshrc 2>/dev/null; then
            echo "" >> ~/.zshrc
            echo "# NVIDIA CUDA and Nsight tools" >> ~/.zshrc
            echo "export CUDA_HOME=$CUDA_PATH" >> ~/.zshrc
            echo "export PATH=\$PATH:\$CUDA_HOME/bin" >> ~/.zshrc
            echo "Environment variables added to ~/.zshrc"
        else
            echo "CUDA environment variables already configured in .zshrc"
        fi
    fi
fi

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Installed tools:"
echo "  - Nsight Systems: Performance analysis for CPU/GPU workloads"
echo "  - Nsight Compute: Detailed CUDA kernel profiling"  
echo ""
echo "To launch the tools, use:"
echo "  nsys-ui          (Nsight Systems GUI)"
echo "  nsys             (Nsight Systems CLI)"
echo "  ncu-ui           (Nsight Compute GUI)"
echo "  ncu              (Nsight Compute CLI)"
echo ""
echo "Note: You may need to restart your terminal or run 'source ~/.zshrc'"
echo "      to use the CUDA tools from command line."
