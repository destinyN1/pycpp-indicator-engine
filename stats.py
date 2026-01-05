import strategy
import backtest
import load_data
import numpy as np
import matplotlib.pyplot as plt
import indicators

#this file will run the full backtest when executed and compute some stats

def compute_total_returns(prices, signals, return_type):
    if return_type == "simple":
        returns = backtest.compute_simple_returns(prices)
        total_return = backtest.addup_simmple_returns(returns)
    elif return_type == "log":
        returns = backtest.compute_log_returns(prices)
        total_return = backtest.addup_log_returns(returns)
    else:
        raise ValueError("Invalid return type. Use 'simple' or 'log'.")
    
    return total_return

def compute_maximum_drawdown(prices):
    max_drawdown = 0
    peak = prices[0]

    for price in prices:
        if price > peak:
            peak = price
        drawdown = (peak - price) / peak
        if drawdown > max_drawdown:
            max_drawdown = drawdown

    return max_drawdown

def compute_sharpe_ratio(returns, risk_free_rate=0.0):
    import numpy as np

    returns = np.array(returns)
    excess_returns = returns - risk_free_rate
    avg_excess_return = np.mean(excess_returns)
    std_dev = np.std(returns)

    if std_dev == 0:
        return 0.0

    sharpe_ratio = avg_excess_return / std_dev
    return sharpe_ratio

def run_full_strategy(file_path, fast, slow):
    close_prices, sma_fast, sma_slow, ema_fast, ema_slow = strategy.run_strategy(file_path, fast, slow)

    sma_signals = strategy.moving_average_crossover_strategy(sma_fast, sma_slow)
    ema_signals = strategy.moving_average_crossover_strategy(ema_fast, ema_slow)
    
    #Plot SMA crossover with signals
    plt.figure(figsize=(12, 6))
    plt.plot(sma_fast, label='SMA Fast')
    plt.plot(sma_slow, label='SMA Slow')
    for i, sig in enumerate(sma_signals):
        if sig == "BUY":
            plt.scatter(i, sma_fast[i], marker='^', color='green')
        elif sig == "SELL":
            plt.scatter(i, sma_fast[i], marker='v', color='red')
    plt.legend()
    plt.title('SMA Crossover with Buy/Sell Signals')
    plt.show()
    
    # Plot EMA crossover with signals
    plt.figure(figsize=(12, 6))
    plt.plot(ema_fast, label='EMA Fast')
    plt.plot(ema_slow, label='EMA Slow')
    for i, sig in enumerate(ema_signals):
        if sig == "BUY":
            plt.scatter(i, ema_fast[i], marker='^', color='green')
        elif sig == "SELL":
            plt.scatter(i, ema_fast[i], marker='v', color='red')
    plt.legend()
    plt.title('EMA Crossover with Buy/Sell Signals')
    plt.show()
    
    # 
    # Compute positions
    sma_positions = backtest.compute_positions(sma_signals)
    ema_positions = backtest.compute_positions(ema_signals)
    
    # Compute equity curves
    equity_sma = backtest.compute_equity_curve(close_prices, sma_positions)
    equity_ema = backtest.compute_equity_curve(close_prices, ema_positions)
    
    # Compute returns
    sma_simple_returns = backtest.compute_simple_returns(close_prices)
    sma_log_returns = backtest.compute_log_returns(close_prices)
    ema_simple_returns = backtest.compute_simple_returns(close_prices)
    ema_log_returns = backtest.compute_log_returns(close_prices)
    
    # Total returns
    total_sma_simple = backtest.addup_simmple_returns(sma_simple_returns)
    total_sma_log = backtest.addup_log_returns(sma_log_returns)
    total_ema_simple = backtest.addup_simmple_returns(ema_simple_returns)
    total_ema_log = backtest.addup_log_returns(ema_log_returns)
    
    # Max drawdown
    max_dd_sma = compute_maximum_drawdown(equity_sma)
    max_dd_ema = compute_maximum_drawdown(equity_ema)
    
    # Sharpe ratio (assuming daily returns, risk-free rate 0)
    sharpe_sma = compute_sharpe_ratio(sma_simple_returns)
    sharpe_ema = compute_sharpe_ratio(ema_simple_returns)
    
    # Print stats
    print(f"SMA Total Simple Return: {total_sma_simple:.4f}")
    print(f"SMA Total Log Return: {total_sma_log:.4f}")
    print(f"SMA Max Drawdown: {max_dd_sma:.4f}")
    print(f"SMA Sharpe Ratio: {sharpe_sma:.4f}")
    print()
    print(f"EMA Total Simple Return: {total_ema_simple:.4f}")
    print(f"EMA Total Log Return: {total_ema_log:.4f}")
    print(f"EMA Max Drawdown: {max_dd_ema:.4f}")
    print(f"EMA Sharpe Ratio: {sharpe_ema:.4f}")
    
    # Plot equity curves
    backtest.plot_equity_curve(equity_sma, title="SMA Strategy Equity Curve")
    backtest.plot_equity_curve(equity_ema, title="EMA Strategy Equity Curve")
    
    # Plot positions over time
    backtest.plot_positions_over_time(sma_positions, title="SMA Positions Over Time")
    backtest.plot_positions_over_time(ema_positions, title="EMA Positions Over Time")

    #plot 

    return close_prices, sma_fast, sma_slow, ema_fast, ema_slow 


if __name__ == "__main__":   
    import sys
    if len(sys.argv) != 4:
        print("Usage: python stats.py <csv_path> <fast> <slow>")
        sys.exit(1)
    file_path = sys.argv[1]
    fast = int(sys.argv[2])
    slow = int(sys.argv[3])
    run_full_strategy(file_path, fast, slow)
    
    
