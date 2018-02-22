import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#data = pd.read_csv("test_data1.csv", names= ["time", "voltage"])
#time = data["time"]
#voltage = data["voltage"]

#plt.plot(time,voltage, "o")

class HeartRate:

    def __init__ (self, filename = None):
        self.filename = filename


    def parseData(self):
        data = pd.read_csv(self.filename, names = ["Time", "Voltage"])
        time = data["Time"]
        voltage = data["Voltage"]
        return time, voltage

x = HeartRate("test_data1.csv")
print (x.parseData())

#
