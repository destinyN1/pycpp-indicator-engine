import indicator_engine
import numpy as np

prices = np.load('close_prices.npy')
sma = indicator_engine.simple_moving_average(prices, 10)
ema = indicator_engine.exponential_moving_average(prices, 10)
print("SMA:", sma)
print("EMA:", ema)