#!/usr/bin/env python3

import sys
import os
import time
import numpy as np

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import indicators
import indicator_engine

def load_test_data(filepath):
    """Load test data from .npy file"""
    data = np.load(filepath)
    return data

def benchmark_function(func, data, window, name, iterations=10):
    """Benchmark a function and return timing statistics"""
    times = []
    
    # Warmup run
    func(data, window)
    
    # Actual benchmark
    for _ in range(iterations):
        start = time.perf_counter()
        result = func(data, window)
        end = time.perf_counter()
        times.append(end - start)
    
    avg_time = np.mean(times)
    std_time = np.std(times)
    min_time = np.min(times)
    max_time = np.max(times)
    
    return {
        'name': name,
        'avg': avg_time,
        'std': std_time,
        'min': min_time,
        'max': max_time,
        'times': times
    }

def main():
    print("\n" + "="*80)
    print("BENCHMARK: Python vs C++ Moving Average Implementations")
    print("="*80)
    
    # Load test data
    data_path = os.path.join(os.path.dirname(__file__), 'close_prices.npy')
    
    if not os.path.exists(data_path):
        print(f"\n❌ ERROR: Test data not found at {data_path}")
        return False
    
    close_prices = load_test_data(data_path)
    close_prices_cpp = close_prices.astype(np.float64)
    
    print(f"\n✓ Loaded test data: {len(close_prices)} price points")
    print(f"✓ Data type: {close_prices.dtype}")
    
    # Benchmark parameters
    window_sizes = [10, 20, 50, 100]
    iterations = 20
    
    print(f"\n{'='*80}")
    print(f"Benchmark Configuration")
    print(f"{'='*80}")
    print(f"Window sizes: {window_sizes}")
    print(f"Iterations per test: {iterations}")
    print(f"Data points: {len(close_prices)}")
    
    # Run benchmarks
    results = {}
    
    for window in window_sizes:
        print(f"\n{'#'*80}")
        print(f"# Window Size: {window}")
        print(f"{'#'*80}")
        
        # SMA Benchmark
        print(f"\nBenchmarking SMA (window={window})...")
        py_sma_result = benchmark_function(
            indicators.simple_moving_average,
            close_prices,
            window,
            f"Python SMA (w={window})",
            iterations
        )
        print(f"  Python SMA: {py_sma_result['avg']*1000:.4f} ± {py_sma_result['std']*1000:.4f} ms")
        
        cpp_sma_result = benchmark_function(
            indicator_engine.simple_moving_average,
            close_prices_cpp,
            window,
            f"C++ SMA (w={window})",
            iterations
        )
        print(f"  C++ SMA:    {cpp_sma_result['avg']*1000:.4f} ± {cpp_sma_result['std']*1000:.4f} ms")
        
        sma_speedup = py_sma_result['avg'] / cpp_sma_result['avg']
        print(f"  Speedup:    {sma_speedup:.2f}x")
        
        # EMA Benchmark
        print(f"\nBenchmarking EMA (window={window})...")
        py_ema_result = benchmark_function(
            indicators.exponential_moving_average,
            close_prices,
            window,
            f"Python EMA (w={window})",
            iterations
        )
        print(f"  Python EMA: {py_ema_result['avg']*1000:.4f} ± {py_ema_result['std']*1000:.4f} ms")
        
        cpp_ema_result = benchmark_function(
            indicator_engine.exponential_moving_average,
            close_prices_cpp,
            window,
            f"C++ EMA (w={window})",
            iterations
        )
        print(f"  C++ EMA:    {cpp_ema_result['avg']*1000:.4f} ± {cpp_ema_result['std']*1000:.4f} ms")
        
        ema_speedup = py_ema_result['avg'] / cpp_ema_result['avg']
        print(f"  Speedup:    {ema_speedup:.2f}x")
        
        # Store results
        results[window] = {
            'sma': {
                'python': py_sma_result,
                'cpp': cpp_sma_result,
                'speedup': sma_speedup
            },
            'ema': {
                'python': py_ema_result,
                'cpp': cpp_ema_result,
                'speedup': ema_speedup
            }
        }
    
    # Print summary
    print(f"\n{'='*80}")
    print("SUMMARY TABLE")
    print(f"{'='*80}")
    
    print(f"\n{'Window':<10} {'Metric':<12} {'Python (ms)':<15} {'C++ (ms)':<15} {'Speedup':<10}")
    print(f"{'-'*80}")
    
    for window in window_sizes:
        # SMA
        py_time = results[window]['sma']['python']['avg'] * 1000
        cpp_time = results[window]['sma']['cpp']['avg'] * 1000
        speedup = results[window]['sma']['speedup']
        print(f"{window:<10} {'SMA':<12} {py_time:<15.4f} {cpp_time:<15.4f} {speedup:<10.2f}x")
        
        # EMA
        py_time = results[window]['ema']['python']['avg'] * 1000
        cpp_time = results[window]['ema']['cpp']['avg'] * 1000
        speedup = results[window]['ema']['speedup']
        print(f"{window:<10} {'EMA':<12} {py_time:<15.4f} {cpp_time:<15.4f} {speedup:<10.2f}x")
    
    # Overall statistics
    print(f"\n{'='*80}")
    print("OVERALL STATISTICS")
    print(f"{'='*80}")
    
    sma_speedups = [results[w]['sma']['speedup'] for w in window_sizes]
    ema_speedups = [results[w]['ema']['speedup'] for w in window_sizes]
    
    print(f"\nSMA Speedup: {np.mean(sma_speedups):.2f}x average (min: {np.min(sma_speedups):.2f}x, max: {np.max(sma_speedups):.2f}x)")
    print(f"EMA Speedup: {np.mean(ema_speedups):.2f}x average (min: {np.min(ema_speedups):.2f}x, max: {np.max(ema_speedups):.2f}x)")
    
    print(f"\n{'='*80}\n")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

