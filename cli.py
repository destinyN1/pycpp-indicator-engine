#!/usr/bin/env python3

import argparse
import stats

def main():
    parser = argparse.ArgumentParser(description='Run backtest and compute stats for moving average crossover strategies.')
    parser.add_argument('csv_path', help='Path to the CSV file containing price data')
    parser.add_argument('fast', type=int, help='Window size for fast moving average')
    parser.add_argument('slow', type=int, help='Window size for slow moving average')
    
    args = parser.parse_args()
    
    # Run the full strategy with the provided arguments
    stats.run_full_strategy(args.csv_path, args.fast, args.slow)

if __name__ == "__main__":
    main()