import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class readInData:

    def __init__ (self, filename = None):
        self.filename = filename


    def parseData(self):
        data = pd.read_csv(self.filename, names = ["Time", "Voltage"]) 
        return data

    def plotData(self):
        data = x.parseData()
        plt.plot(data["Time"],data["Voltage"])
        plt.show()


x = readInData("test_data1.csv")
x.plotData()

