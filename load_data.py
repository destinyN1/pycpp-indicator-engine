import csv
import numpy as np


def create_close_price_array(): #put variable path here
    with open('/home/destiny/Programming/Kraken_OHLCVT/1INCHEUR_1440.csv', 'r') as file:
        data = file.read()
        close = csv.reader(data.splitlines())
        for row in close:
        #print only the closing prices
            #print(row[4])
       #save to a seperate file
            with open('/home/destiny/Programming/close_prices.csv', 'a') as close_file:
                close_writer = csv.writer(close_file)
                close_writer.writerow([row[4]])
     
def create_close_price_numpy_array(): #this function needs to be imported into the next part of the flow
    close_prices = np.loadtxt('/home/destiny/Programming/close_prices.csv', delimiter=',')
    np.save('/home/destiny/Programming/close_prices.npy', close_prices)
    print(close_prices)
    return close_prices


if __name__ == "__main__":
    create_close_price_array()
    create_close_price_numpy_array()



        
