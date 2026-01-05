import csv
import numpy as np
import os

def create_close_price_array(file_path):
    """
    Read CSV at file_path, extract the 5th column (index 4) as floats (closing prices),
    save './close_prices.npy' and return the numpy array.

    This version does NOT append to an existing CSV file; it builds the array in memory
    and overwrites the .npy file each time so runs are deterministic.
    """
    close_prices = []
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue
            # guard against short rows or headers
            try:
                val = float(row[4])
            except (IndexError, ValueError):
                # skip headers or malformed rows
                continue
            close_prices.append(val)

    close_prices = np.array(close_prices, dtype=float)
    # Save the array to .npy so other parts of the code that expect the file still work
    np.save('./close_prices.npy', close_prices)
    return close_prices

# keep this helper if you need to create a numpy array directly from a csv file
def create_close_price_numpy_array(file_path):
    close_prices = np.loadtxt(file_path, delimiter=',')
    np.save('./close_prices.npy', close_prices)
    return close_prices

if __name__ == "__main__":
    # example usage - replace path with your CSV path
    create_close_price_array('/home/destiny/Programming/Kraken_OHLCVT/1INCHEUR_1440.csv')