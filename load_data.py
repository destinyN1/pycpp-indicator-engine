import csv
import numpy as np

#/home/destiny/Programming/Kraken_OHLCVT/1INCHEUR_1440.csv

#save to a seperate file
            # with open('/home/destiny/Programming/close_prices.csv', 'a') as close_file:
            #     close_writer = csv.writer(close_file)
            #     close_writer.writerow([row[4]])
     
def create_close_price_array(file_path): #put variable path here
    with open(file_path, 'r') as file:
        data = file.read()
        close = csv.reader(data.splitlines())
        for row in close:
        #print only the closing prices
           # print(row[4])
            #append to an npy array and save the file
            with open('./close_prices.csv', 'a') as close_file:
                close_writer = csv.writer(close_file)
                close_writer.writerow([row[4]])

    create_close_price_numpy_array('./close_prices.csv')                  

        
     
def create_close_price_numpy_array(file_path): #this function needs to be imported into the next part of the flow #variable file path here as well for cli tool
    close_prices = np.loadtxt(file_path, delimiter=',') 
    np.save('./close_prices.npy', close_prices)
    print(close_prices)
    return close_prices


if __name__ == "__main__":
    create_close_price_array('/home/destiny/Programming/Kraken_OHLCVT/1INCHEUR_1440.csv')

   # create_close_price_numpy_array()



        