from fileinput import filename
from json.tool import main
from unicodedata import name
import pandas as pd
import config_file


tripsFilePath = config_file.tripsFileSourcePath

def importTripsSource(filepath):
    dfSourceTrips = pd.read_csv(filepath)
    return dfSourceTrips

def main():
    # print('Hello World')
    dfTripsRaw = importTripsSource(tripsFilePath + 'trips.csv') ##Change after to recursive
    print(dfTripsRaw)

if __name__ == '__main__':
    main()

