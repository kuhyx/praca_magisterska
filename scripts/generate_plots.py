#!/usr/bin/env python3
"""
Script to generate performance comparison plots for the thesis.
Fill in the data arrays with actual measurements from NVIDIA Nsight.

Usage:
    python3 generate_plots.py

Output:
    - frame-time-comparison.pdf
    - gpu-utilization.pdf
    - memory-usage.pdf
    - draw-calls-comparison.pdf
    
All output files are saved to latex/tex/img/
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# Ensure output directory exists
output_dir = os.path.join('latex', 'tex', 'img')
os.makedirs(output_dir, exist_ok=True)

# ==============================================================================
# DATA SECTION - FILL WITH ACTUAL MEASUREMENTS
# ==============================================================================

# Frame time data (in milliseconds)
frame_time_unity = {
    'low': [0, 0, 0, 0, 0],      # Replace with actual data
    'medium': [0, 0, 0, 0, 0],   # Replace with actual data
    'high': [0, 0, 0, 0, 0]      # Replace with actual data
}

frame_time_unreal = {
    'low': [0, 0, 0, 0, 0],      # Replace with actual data
    'medium': [0, 0, 0, 0, 0],   # Replace with actual data
    'high': [0, 0, 0, 0, 0]      # Replace with actual data
}

# GPU utilization data (in percentage)
gpu_util_unity = {
    'low': [0, 0, 0, 0, 0],      # Replace with actual data
    'medium': [0, 0, 0, 0, 0],   # Replace with actual data
    'high': [0, 0, 0, 0, 0]      # Replace with actual data
}

gpu_util_unreal = {
    'low': [0, 0, 0, 0, 0],      # Replace with actual data
    'medium': [0, 0, 0, 0, 0],   # Replace with actual data
    'high': [0, 0, 0, 0, 0]      # Replace with actual data
}

# Memory usage data (in MB)
memory_unity = {
    'low': [0, 0, 0, 0, 0],      # Replace with actual data
    'medium': [0, 0, 0, 0, 0],   # Replace with actual data
    'high': [0, 0, 0, 0, 0]      # Replace with actual data
}

memory_unreal = {
    'low': [0, 0, 0, 0, 0],      # Replace with actual data
    'medium': [0, 0, 0, 0, 0],   # Replace with actual data
    'high': [0, 0, 0, 0, 0]      # Replace with actual data
}

# Draw calls data
draw_calls_unity = {
    'low': [0, 0, 0, 0, 0],      # Replace with actual data
    'medium': [0, 0, 0, 0, 0],   # Replace with actual data
    'high': [0, 0, 0, 0, 0]      # Replace with actual data
}

draw_calls_unreal = {
    'low': [0, 0, 0, 0, 0],      # Replace with actual data
    'medium': [0, 0, 0, 0, 0],   # Replace with actual data
    'high': [0, 0, 0, 0, 0]      # Replace with actual data
}

# ==============================================================================
# PLOTTING FUNCTIONS
# ==============================================================================

def setup_plot_style():
    """Configure matplotlib for academic paper style."""
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.titlesize'] = 11
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    plt.rcParams['legend.fontsize'] = 9
    plt.rcParams['figure.titlesize'] = 11
    plt.rcParams['figure.figsize'] = (6, 4)
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['savefig.bbox'] = 'tight'

def calculate_stats(data_dict):
    """Calculate mean and std for each scenario."""
    stats = {}
    for scenario, values in data_dict.items():
        stats[scenario] = {
            'mean': np.mean(values) if any(values) else 0,
            'std': np.std(values) if any(values) else 0
        }
    return stats

def plot_frame_time_comparison():
    """Generate frame time comparison plot."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    scenarios = ['Niski', 'Średni', 'Wysoki']
    x = np.arange(len(scenarios))
    width = 0.35
    
    unity_stats = calculate_stats(frame_time_unity)
    unreal_stats = calculate_stats(frame_time_unreal)
    
    unity_means = [unity_stats['low']['mean'], unity_stats['medium']['mean'], unity_stats['high']['mean']]
    unity_stds = [unity_stats['low']['std'], unity_stats['medium']['std'], unity_stats['high']['std']]
    
    unreal_means = [unreal_stats['low']['mean'], unreal_stats['medium']['mean'], unreal_stats['high']['mean']]
    unreal_stds = [unreal_stats['low']['std'], unreal_stats['medium']['std'], unreal_stats['high']['std']]
    
    bars1 = ax.bar(x - width/2, unity_means, width, yerr=unity_stds, 
                   label='Unity', capsize=5, color='#1f77b4', alpha=0.8)
    bars2 = ax.bar(x + width/2, unreal_means, width, yerr=unreal_stds,
                   label='Unreal Engine', capsize=5, color='#ff7f0e', alpha=0.8)
    
    ax.set_xlabel('Scenariusz testowy')
    ax.set_ylabel('Czas klatki [ms]')
    ax.set_title('Porównanie czasu renderowania klatki')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'frame-time-comparison.pdf')
    plt.savefig(output_path)
    print(f"✓ Saved: {output_path}")
    plt.close()

def plot_gpu_utilization():
    """Generate GPU utilization plot."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    scenarios = ['Niski', 'Średni', 'Wysoki']
    x = np.arange(len(scenarios))
    width = 0.35
    
    unity_stats = calculate_stats(gpu_util_unity)
    unreal_stats = calculate_stats(gpu_util_unreal)
    
    unity_means = [unity_stats['low']['mean'], unity_stats['medium']['mean'], unity_stats['high']['mean']]
    unity_stds = [unity_stats['low']['std'], unity_stats['medium']['std'], unity_stats['high']['std']]
    
    unreal_means = [unreal_stats['low']['mean'], unreal_stats['medium']['mean'], unreal_stats['high']['mean']]
    unreal_stds = [unreal_stats['low']['std'], unreal_stats['medium']['std'], unreal_stats['high']['std']]
    
    bars1 = ax.bar(x - width/2, unity_means, width, yerr=unity_stds,
                   label='Unity', capsize=5, color='#1f77b4', alpha=0.8)
    bars2 = ax.bar(x + width/2, unreal_means, width, yerr=unreal_stds,
                   label='Unreal Engine', capsize=5, color='#ff7f0e', alpha=0.8)
    
    ax.set_xlabel('Scenariusz testowy')
    ax.set_ylabel('Wykorzystanie GPU [%]')
    ax.set_title('Wykorzystanie mocy obliczeniowej GPU')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios)
    ax.set_ylim(0, 100)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'gpu-utilization.pdf')
    plt.savefig(output_path)
    print(f"✓ Saved: {output_path}")
    plt.close()

def plot_memory_usage():
    """Generate memory usage plot."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    scenarios = ['Niski', 'Średni', 'Wysoki']
    x = np.arange(len(scenarios))
    width = 0.35
    
    unity_stats = calculate_stats(memory_unity)
    unreal_stats = calculate_stats(memory_unreal)
    
    unity_means = [unity_stats['low']['mean'], unity_stats['medium']['mean'], unity_stats['high']['mean']]
    unity_stds = [unity_stats['low']['std'], unity_stats['medium']['std'], unity_stats['high']['std']]
    
    unreal_means = [unreal_stats['low']['mean'], unreal_stats['medium']['mean'], unreal_stats['high']['mean']]
    unreal_stds = [unreal_stats['low']['std'], unreal_stats['medium']['std'], unreal_stats['high']['std']]
    
    bars1 = ax.bar(x - width/2, unity_means, width, yerr=unity_stds,
                   label='Unity', capsize=5, color='#1f77b4', alpha=0.8)
    bars2 = ax.bar(x + width/2, unreal_means, width, yerr=unreal_stds,
                   label='Unreal Engine', capsize=5, color='#ff7f0e', alpha=0.8)
    
    ax.set_xlabel('Scenariusz testowy')
    ax.set_ylabel('Zużycie pamięci VRAM [MB]')
    ax.set_title('Zużycie pamięci karty graficznej')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'memory-usage.pdf')
    plt.savefig(output_path)
    print(f"✓ Saved: {output_path}")
    plt.close()

def plot_draw_calls():
    """Generate draw calls comparison plot."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    scenarios = ['Niski', 'Średni', 'Wysoki']
    x = np.arange(len(scenarios))
    width = 0.35
    
    unity_stats = calculate_stats(draw_calls_unity)
    unreal_stats = calculate_stats(draw_calls_unreal)
    
    unity_means = [unity_stats['low']['mean'], unity_stats['medium']['mean'], unity_stats['high']['mean']]
    unity_stds = [unity_stats['low']['std'], unity_stats['medium']['std'], unity_stats['high']['std']]
    
    unreal_means = [unreal_stats['low']['mean'], unreal_stats['medium']['mean'], unreal_stats['high']['mean']]
    unreal_stds = [unreal_stats['low']['std'], unreal_stats['medium']['std'], unreal_stats['high']['std']]
    
    bars1 = ax.bar(x - width/2, unity_means, width, yerr=unity_stds,
                   label='Unity', capsize=5, color='#1f77b4', alpha=0.8)
    bars2 = ax.bar(x + width/2, unreal_means, width, yerr=unreal_stds,
                   label='Unreal Engine', capsize=5, color='#ff7f0e', alpha=0.8)
    
    ax.set_xlabel('Scenariusz testowy')
    ax.set_ylabel('Liczba draw calls')
    ax.set_title('Efektywność wywołań renderowania')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'draw-calls-comparison.pdf')
    plt.savefig(output_path)
    print(f"✓ Saved: {output_path}")
    plt.close()

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    """Generate all plots."""
    print("Generating performance comparison plots...")
    print(f"Output directory: {output_dir}")
    print()
    
    setup_plot_style()
    
    plot_frame_time_comparison()
    plot_gpu_utilization()
    plot_memory_usage()
    plot_draw_calls()
    
    print()
    print("✓ All plots generated successfully!")
    print()
    print("Next steps:")
    print("1. Fill in the data arrays at the top of this script with actual measurements")
    print("2. Run the script again: python3 generate_plots.py")
    print("3. Uncomment the \\includegraphics lines in 5-testy-wydajnosci.tex")
    print("4. Compile your LaTeX document")

if __name__ == '__main__':
    main()
