import numpy as np
#implement a simple moving average indicator
#import function from loadata.py (create_close_price_numpy_array)

import load_data


def simple_moving_average(data, window_size):
    #import close prices here
    
    weights = np.ones(window_size) / window_size
    sma = np.convolve(data, weights, mode='valid')
    return sma

def exponential_moving_average(data, window_size):
    #import close prices here as well (call the import close prices function)
    
    ema = np.zeros_like(data)
    alpha = 2 / (window_size + 1)
    ema[0] = data[0]
    for i in range(1, len(data)):
        ema[i] = alpha * data[i] + (1 - alpha) * ema[i - 1]
    return ema

#import close prices here to have them returned
def import_close_prices(file_path):

    load_data.create_close_price_array(file_path)
    
    #read numpy array from npy file
    close_prices = np.load('./close_prices.npy')
    return close_prices
   

def plot_close_prices_vs_sma(close_prices, sma):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12,6))
    plt.plot(close_prices, label='Close Prices')
    plt.plot(range(len(sma)), sma, label='Simple Moving Average', color='orange')
    plt.legend()
    plt.show()

def plot_close_prices_vs_ema(close_prices, ema):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12,6))
    plt.plot(close_prices, label='Close Prices')
    plt.plot(range(len(ema)), ema, label='Exponential Moving Average', color='green')
    plt.legend()
    plt.show()



if __name__ == "__main__":
    close_prices = import_close_prices('/home/destiny/Programming/Kraken_OHLCVT/1INCHEUR_1440.csv') 
    sma_fast= simple_moving_average(close_prices, 10) #sma_fast/slow, ema_fast/slow functions need to be imported into strategy.py
    sma_slow= simple_moving_average(close_prices, 100)
    ema_fast= exponential_moving_average(close_prices, 10)
    ema_slow= exponential_moving_average(close_prices, 100)
    #save sma_10/ema_10 to a npy file
    np.save('/home/destiny/Programming/pycpp-indicator-engine/sma_fast.npy', sma_fast)
    np.save('/home/destiny/Programming/pycpp-indicator-engine/ema_fast.npy', ema_fast)
    np.save('/home/destiny/Programming/pycpp-indicator-engine/sma_slow.npy', sma_slow)
    np.save('/home/destiny/Programming/pycpp-indicator-engine/ema_slow.npy', ema_slow)
    
    # plot_close_prices_vs_sma(close_prices, sma_fast)
    # plot_close_prices_vs_ema(close_prices, ema_fast)
    # plot_close_prices_vs_sma(close_prices, sma_slow)
    # plot_close_prices_vs_ema(close_prices, ema_slow)
  
  
  
  
   

# def compare_lengths_sma_close_prices(close_prices, sma):
#     len_close = len(close_prices)
#     len_sma = len(sma)
#     print(f"Length of Close Prices: {len_close}")
#     print(f"Length of SMA: {len_sma}")
#     if len_close > len_sma:
#         print(f"Close Prices is longer by {len_close - len_sma} elements.")
#     elif len_sma > len_close:
#         print(f"SMA is longer by {len_sma - len_close} elements.")
#     else:
#         print("Both arrays are of equal length.")