import numpy as np
#implement a simple moving average indicator
def simple_moving_average(data, window_size):
    
    weights = np.ones(window_size) / window_size
    sma = np.convolve(data, weights, mode='valid')
    return sma

def exponential_moving_average(data, window_size):
    ema = np.zeros_like(data)
    alpha = 2 / (window_size + 1)
    ema[0] = data[0]
    for i in range(1, len(data)):
        ema[i] = alpha * data[i] + (1 - alpha) * ema[i - 1]
    return ema
    
def import_close_prices(file_path):
    #read numpy array from npy file
    close_prices_averaged = np.load(file_path)
    return close_prices_averaged
   

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

def compare_lengths_sma_close_prices(close_prices, sma):
    len_close = len(close_prices)
    len_sma = len(sma)
    print(f"Length of Close Prices: {len_close}")
    print(f"Length of SMA: {len_sma}")
    if len_close > len_sma:
        print(f"Close Prices is longer by {len_close - len_sma} elements.")
    elif len_sma > len_close:
        print(f"SMA is longer by {len_sma - len_close} elements.")
    else:
        print("Both arrays are of equal length.")


if __name__ == "__main__":
    close_prices_averaged = import_close_prices('/home/destiny/Programming/pycpp-indicator-engine/close_prices.npy')
    sma_10 = simple_moving_average(close_prices_averaged, 200)
    ema_10 = exponential_moving_average(close_prices_averaged, 200)
    #save sma_10/ema_10 to a npy file
    np.save('/home/destiny/Programming/pycpp-indicator-engine/sma_10.npy', sma_10)
    np.save('/home/destiny/Programming/pycpp-indicator-engine/ema_10.npy', ema_10)
    #plot close prices vs sma and ema
    plot_close_prices_vs_sma(close_prices_averaged, sma_10)
    plot_close_prices_vs_ema(close_prices_averaged, ema_10)
    compare_lengths_sma_close_prices(close_prices_averaged, sma_10)
    ##print("Simple Moving Average (10):", sma_10)
