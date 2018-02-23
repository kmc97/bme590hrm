import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def readInData(filename):
    file_data = pd.read_csv(filename, names = ["Time", "Voltage"])
    data = HeartRateData(file_data)
    return data

class HeartRateData:
    def __init__ (self, data):
        self.data = data

    def plotData(self):
        plt.plot(self.data["Time"],self.data["Voltage"])
        plt.show()

#    def find_peaks(self):
 #       correlation = data.corr()
 #       data = x.parseData()
 #       window_size = .5
#        fs = 1/(data.iloc[6]['Time'] - data.iloc[5]['Time'])


def main(filename):
    data = readInData(filename)
    data.plotData()


main('test_data1.csv')
