import pandas as pd
import numpy as np
from scipy.signal import savgol_filter, argrelextrema
import math


class importData:
    def __init__ (self, filename = None):
        self.filename = filename

    def readInData(self):
        file_data = pd.read_csv(self.filename, header= None)
        file_data_to_numpy = file_data.as_matrix()
        return file_data_to_numpy

    def makeObject(self, file_data_to_numpy):
        data = HeartRateData(file_data_to_numpy)
        return data

class HeartRateData:
    def __init__ (self, data):
        self.data = data
    
    def find_correlation(self):
        import matplotlib.pyplot as plt
        voltage = self.data[:,1]
        norm_voltage = voltage - np.mean(voltage)
        smooth_voltage = savgol_filter(norm_voltage, 15,3)
        plt.plot(smooth_voltage)
        plt.show()
        return smooth_voltage
    
    def max_find_correlation(self, smooth_voltage):
        import matplotlib.pyplot as plt
        subset_max_index = argrelextrema(smooth_voltage, np.greater)
        subset_max = smooth_voltage[subset_max_index [0]]
        max_value_index = np.argmax(subset_max)

        interval = 50
        if max_value_index < 50:
            interval = max_value_index -1
        if (len(smooth_voltage)-max_value_index < 50):
            interval = len(smooth_voltage)- max_value_index-1 
        else:
            interval = interval

        subsetv2 = smooth_voltage[(max_value_index-interval):(max_value_index+interval)]
        subsetv2 = subsetv2 - np.mean(subsetv2)
        subsetv2 = savgol_filter(subsetv2,15,3)
        
        plt.plot(subsetv2)
        plt.show()
       
        corr_values2 = np.correlate(smooth_voltage, subsetv2)
        corr_values2 = corr_values2 -np.mean(corr_values2)
        corr_values_class = detectHeartBeat(corr_values2)
        return corr_values_class

    def correlation_find_correlation(self, smooth_voltage):
        import matplotlib.pyplot as plt
        corr_values = np.correlate(smooth_voltage,smooth_voltage, 'same')
        max_index = np.argmax(corr_values)
        subset = smooth_voltage[(max_index-60):(max_index+60)]
        subset = subset- np.mean(subset)
        subset = savgol_filter(subset,15,3)
     
        plt.plot(subset)
        plt.show()
        corr_values = np.correlate(smooth_voltage,subset)
        corr_values = corr_values - np.mean(corr_values)
        corr_values_class = detectHeartBeat(corr_values)

        return corr_values_class

       
#        plt.subplot(511)
 #       plt.plot(smooth_voltage)
     #   plt.subplot(512)
     #   plt.plot(subset)
     #   plt.subplot(514)
    #    plt.plot(subsetv2)
    #    plt.subplot(513)
     #   plt.plot(corr_values2)
      #  plt.subplot(515)
      #  plt.plot(corr_values2)  
      #  plt.show()
      
    

class detectHeartBeat:
    def __init__(self,corr_values_class):
        self.corr_values = corr_values_class

    def find_peaks(self):
        import matplotlib.pyplot as plt
        rect_values = self.corr_values
#        rect_values = np.absolute(self.corr_values)  
        plt.subplot(311)
        plt.plot(rect_values)
#        derivative = np.diff(rect_values)
        derivative = abs(np.diff(rect_values))  
        plt.subplot(312)
        plt.plot(derivative)
        
        
        df = pd.DataFrame(derivative)
        avg_hr = np.mean(derivative)

        mov_avg = df.rolling(45, center=False).mean()
        mov_avg = mov_avg.rolling(40, center=False).mean()
        mov_avg = mov_avg.rolling(50, center= False).mean()
        mov_avg= mov_avg.rolling(10, center=False).mean()
        mov_avg[np.isnan(mov_avg)]= avg_hr 
        mov_avg = mov_avg- np.mean(mov_avg)

           
        plt.subplot(313)
        plt.plot(mov_avg)
        plt.show()

        mov_avg_numpy = mov_avg.as_matrix()
        local_max_index =argrelextrema(mov_avg_numpy, np.greater)
        values = mov_avg_numpy[argrelextrema(mov_avg_numpy, np.greater) [0]]
        values = [item for item in values if item >= (avg_hr)]
        print(avg_hr)
        print(len(values))


def main(filename):
    x = importData(filename)
    data = x.readInData()
    data = x.makeObject(data)
    smooth_voltage =data.find_correlation()
    corr_values_class1 = data.max_find_correlation(smooth_voltage)   
    corr_values_class2 = data.correlation_find_correlation(smooth_voltage)
    corr_values_class1.find_peaks()
    corr_values_class2.find_peaks()

#main('test_data8.csv')
