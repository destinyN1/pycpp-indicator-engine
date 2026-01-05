import strategy
import load_data
import numpy as np

#compute simple return from price series
def compute_simple_returns(prices):
    returns = []
    for i in range(1, len(prices)):
        simple_return = (prices[i] - prices[i-1]) / prices[i-1]
        returns.append(simple_return)
    return returns

#compute log return from price series
def compute_log_returns(prices):
    import math
    log_returns = []
    for i in range(1, len(prices)):
        log_return = math.log(prices[i] / prices[i-1])
        log_returns.append(log_return)
    return log_returns

#compute position array based on signals ("BUY", "SELL", "HOLD")
def compute_positions(signals):
    positions = []
    current_position = 0  # 1 = long, -1 = short, 0 = flat

    for signal in signals:
        if signal == "BUY":
            current_position = 1
            positions.append(current_position)
        elif signal == "SELL":
            current_position = 0
            positions.append(current_position)
        elif signal == "HOLD":
            positions.append(2)  # indicator only, does NOT change state

    return positions

    

if __name__ == "__main__":
    #import sma and ema signals
    sma_signals = np.load('./sma_signals.npy')
    ema_signals = np.load('./ema_signals.npy')
    #import close prices
    close_prices = np.load('./close_prices.npy')

    sma_positions = compute_positions(sma_signals)
    print("Positions based on SMA signals:", sma_positions)
    ema_positions = compute_positions(ema_signals)
    print("Positions based on EMA signals:", ema_positions)
