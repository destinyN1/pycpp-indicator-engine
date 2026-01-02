import csv

with open('data.txt', 'r') as file:
    data = file.read()
    close = csv.reader(data.splitlines())
    for row in close:
        if len(row) >= 2:
            print(row[-2])
