#!/usr/bin/env python3

import sys
import os
import numpy as np

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import indicators
import indicator_engine

def load_test_data(filepath):
    """Load test data from .npy file"""
    data = np.load(filepath)
    return data

def compare_arrays(python_result, cpp_result, name, tolerance=1e-9, allow_shape_diff=False):
    """Compare Python and C++ results with tolerance"""
    print(f"\n{'='*60}")
    print(f"Comparing {name}")
    print(f"{'='*60}")
    
    if python_result.shape != cpp_result.shape:
        if allow_shape_diff:
            print(f"⚠ SHAPE DIFFERENCE (allowed for SMA):")
            print(f"   Python shape: {python_result.shape}")
            print(f"   C++ shape: {cpp_result.shape}")
            print(f"   Note: Python SMA uses mode='valid', C++ pads with zeros")
            
            # For SMA, skip comparing the padded zeros at the start
            # Find where Python SMA starts having non-zero values
            cpp_offset = cpp_result.shape[0] - python_result.shape[0]
            print(f"   Offset: {cpp_offset}")
            
            # Compare the overlapping portions
            cpp_compare = cpp_result[cpp_offset:]
            diff = np.abs(python_result - cpp_compare)
            max_diff = np.max(diff)
            mean_diff = np.mean(diff)
            
            print(f"\nDifference Statistics (for overlapping portion):")
            print(f"  Max difference: {max_diff:.2e}")
            print(f"  Mean difference: {mean_diff:.2e}")
            
            non_zero_diffs = np.count_nonzero(diff > tolerance)
            print(f"  Elements exceeding tolerance ({tolerance:.2e}): {non_zero_diffs}/{len(python_result)}")
            
            if non_zero_diffs == 0:
                print(f"\n✓ PASS: All overlapping values match within tolerance!")
                return True
            else:
                print(f"\n✗ FAIL: {non_zero_diffs} values exceed tolerance")
                return False
        else:
            print(f"❌ SHAPE MISMATCH:")
            print(f"   Python shape: {python_result.shape}")
            print(f"   C++ shape: {cpp_result.shape}")
            return False
    
    print(f"✓ Shapes match: {python_result.shape}")
    
    # Calculate differences
    diff = np.abs(python_result - cpp_result)
    max_diff = np.max(diff)
    mean_diff = np.mean(diff)
    
    # Count non-zero differences
    non_zero_diffs = np.count_nonzero(diff > tolerance)
    
    print(f"\nDifference Statistics:")
    print(f"  Max difference: {max_diff:.2e}")
    print(f"  Mean difference: {mean_diff:.2e}")
    print(f"  Elements exceeding tolerance ({tolerance:.2e}): {non_zero_diffs}/{len(python_result)}")
    
    print(f"\nFirst 20 values comparison:")
    print(f"{'Index':<6} {'Python':<18} {'C++':<18} {'Diff':<18}")
    print(f"{'-'*62}")
    for i in range(min(20, len(python_result))):
        py_val = python_result[i]
        cpp_val = cpp_result[i]
        d = abs(py_val - cpp_val)
        status = "✓" if d <= tolerance else "✗"
        print(f"{i:<6} {py_val:<18.10f} {cpp_val:<18.10f} {d:<18.2e} {status}")
    
    print(f"\nLast 10 values comparison:")
    print(f"{'Index':<6} {'Python':<18} {'C++':<18} {'Diff':<18}")
    print(f"{'-'*62}")
    start_idx = max(0, len(python_result) - 10)
    for i in range(start_idx, len(python_result)):
        py_val = python_result[i]
        cpp_val = cpp_result[i]
        d = abs(py_val - cpp_val)
        status = "✓" if d <= tolerance else "✗"
        print(f"{i:<6} {py_val:<18.10f} {cpp_val:<18.10f} {d:<18.2e} {status}")
    
    if non_zero_diffs == 0:
        print(f"\n✓ PASS: All values match within tolerance!")
        return True
    else:
        print(f"\n✗ FAIL: {non_zero_diffs} values exceed tolerance")
        return False

def main():
    print("\n" + "="*60)
    print("INDICATOR ENGINE TEST: Python vs C++ Implementation")
    print("="*60)
    
    # Load test data
    data_path = os.path.join(os.path.dirname(__file__), '..', 'close_prices.npy')
    
    if not os.path.exists(data_path):
        print(f"\n❌ ERROR: Test data not found at {data_path}")
        return False
    
    close_prices = load_test_data(data_path)
    print(f"\n✓ Loaded test data: {len(close_prices)} price points")
    
    # Test parameters
    window_sizes = [5, 10, 20, 50, 100]
    all_passed = True
    
    for window in window_sizes:
        print(f"\n\n{'#'*60}")
        print(f"# Testing with window size: {window}")
        print(f"{'#'*60}")
        
        # Compute SMA
        print(f"\nComputing SMA with window={window}...")
        py_sma = indicators.simple_moving_average(close_prices, window)
        cpp_sma = indicator_engine.simple_moving_average(close_prices.astype(np.float64), window)
        
        sma_passed = compare_arrays(py_sma, cpp_sma, f"SMA (window={window})", tolerance=1e-10, allow_shape_diff=True)
        all_passed = all_passed and sma_passed
        
        # Compute EMA
        print(f"\nComputing EMA with window={window}...")
        py_ema = indicators.exponential_moving_average(close_prices, window)
        cpp_ema = indicator_engine.exponential_moving_average(close_prices.astype(np.float64), window)
        
        ema_passed = compare_arrays(py_ema, cpp_ema, f"EMA (window={window})", tolerance=1e-9)
        all_passed = all_passed and ema_passed
    
    # Summary
    print(f"\n\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("\nPython and C++ implementations produce matching results.")
        return True
    else:
        print("✗ SOME TESTS FAILED")
        print("\nThere are discrepancies between Python and C++ implementations.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

