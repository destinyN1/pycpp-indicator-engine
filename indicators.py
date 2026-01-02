import numpy as np
#implement a simple moving average indicator
def simple_moving_average(data, window_size):
    
    weights = np.ones(window_size) / window_size
    sma = np.convolve(data, weights, mode='valid')
    return sma

    
def import_close_prices(file_path='/home/destiny/Programming/pycpp-indicator-engine/close_prices.csv'):
    close_prices = np.loadtxt(file_path, delimiter=',')
    return close_prices