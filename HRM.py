import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def readInData(filename):
    file_data = pd.read_csv(filename)
    file_data_to_numpy = file_data.as_matrix()
    data = HeartRateData(file_data_to_numpy)
    return data

class HeartRateData:
    def __init__ (self, data):
        self.data = data
    
    def find_correlation(self):
        voltage = self.data[:,1]
        norm_voltage = voltage - np.mean(voltage)
        plt.subplot(311)
        plt.plot(norm_voltage)
        
        corr_values = np.correlate(norm_voltage,norm_voltage,"same")
        max_index =np.argmax(corr_values)
        subset = voltage[(max_index-100):(max_index+100)]
        subset = subset- np.mean(subset)
        
        plt.subplot(312)
        plt.plot(subset)
        #plt.plot(corr_values)
        corr_values = np.correlate(norm_voltage, subset)

        plt.subplot(313)
        plt.plot(corr_values)  
        plt.show()

        return corr_values

    def detect_event(self,corr_values):
#        corr_values = self.data.find_correlation()
        pass
 #       data = x.parseData()
 #       window_size = .5
#        fs = 1/(data.iloc[6]['Time'] - data.iloc[5]['Time'])


def main(filename):
    data = readInData(filename)
    data.find_correlation()
   # data.detect_event()


main('test_data7.csv')
