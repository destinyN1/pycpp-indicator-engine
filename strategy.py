import numpy as np
import matplotlib.pyplot as plt

def moving_average_crossover_strategy(fast_ma, slow_ma):
    # Ensure same length
    n = min(len(fast_ma), len(slow_ma))
    fast_ma = fast_ma[:n]
    slow_ma = slow_ma[:n]

    # Full-length signals so indices line up with your MA arrays
    signals = ["HOLD"] * n

    # Detect crossover events (need i-1, so start at 1)
    for i in range(1, n):
        if fast_ma[i] > slow_ma[i] and fast_ma[i-1] <= slow_ma[i-1]:
            signals[i] = "BUY"
        elif fast_ma[i] < slow_ma[i] and fast_ma[i-1] >= slow_ma[i-1]:
            signals[i] = "SELL"

    return signals


if __name__ == "__main__":
    sma_fast = np.load('/home/destiny/Programming/pycpp-indicator-engine/sma_fast.npy')
    sma_slow = np.load('/home/destiny/Programming/pycpp-indicator-engine/sma_slow.npy')
    ema_fast = np.load('/home/destiny/Programming/pycpp-indicator-engine/ema_fast.npy')
    ema_slow = np.load('/home/destiny/Programming/pycpp-indicator-engine/ema_slow.npy')

    sma_signals = moving_average_crossover_strategy(sma_fast, sma_slow)
    ema_signals = moving_average_crossover_strategy(ema_fast, ema_slow)

    # Plot SMA + crossover markers
    plt.figure(figsize=(12, 6))
    plt.plot(sma_fast, label='SMA Fast')
    plt.plot(sma_slow, label='SMA Slow')

    for i, sig in enumerate(sma_signals):
        if sig == "BUY":
            plt.scatter(i, sma_fast[i], marker='^')
        elif sig == "SELL":
            plt.scatter(i, sma_fast[i], marker='v')

    plt.legend()
    plt.show()

    # Plot EMA + crossover markers
    plt.figure(figsize=(12, 6))
    plt.plot(ema_fast, label='EMA Fast')
    plt.plot(ema_slow, label='EMA Slow')

    for i, sig in enumerate(ema_signals):
        if sig == "BUY":
            plt.scatter(i, ema_fast[i], marker='^')
        elif sig == "SELL":
            plt.scatter(i, ema_fast[i], marker='v')

    plt.legend()
    plt.show()
