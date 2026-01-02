import numpy as np
#implement a simple moving average indicator
def simple_moving_average(data, window_size):
    
    weights = np.ones(window_size) / window_size
    sma = np.convolve(data, weights, mode='valid')
    return sma

    
def import_close_prices(file_path):
    #read numpy array from npy file
    close_prices_averaged = np.load(file_path)
    return close_prices_averaged
   




if __name__ == "__main__":
    close_prices_averaged = import_close_prices('/home/destiny/Programming/pycpp-indicator-engine/close_prices.npy')
    sma_10 = simple_moving_average(close_prices_averaged, 10)
    print("Simple Moving Average (10):", sma_10)