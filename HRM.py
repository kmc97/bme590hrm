import pandas as pd
import numpy as np
from scipy.signal import savgol_filter, argrelmax
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
    
    def signalProcess(self):
        import matplotlib.pyplot as plt
        voltage = self.data[:,1]
        norm_voltage = voltage - np.mean(voltage)
        smooth_voltage = savgol_filter(norm_voltage, 15,3)
#        plt.plot(smooth_voltage)
#        plt.show()
        return smooth_voltage
    
    def max_find_correlation(self, smooth_voltage):
        import matplotlib.pyplot as plt
        subset_max_index = argrelmax(smooth_voltage, order = len(smooth_voltage))
        subset_max_index = subset_max_index[0]        
        subset_max_index = subset_max_index[0]
      
        interval = 30
        if subset_max_index < interval:
            interval = subset_max_index -1
        if (len(smooth_voltage)-subset_max_index < interval):
            interval = len(smooth_voltage)- subset_max_index-1 
        else:
            interval = interval
        print(subset_max_index)

        subset = smooth_voltage[(subset_max_index-interval):(subset_max_index+interval)]
        subset = subset - np.mean(subset)
        subset = savgol_filter(subset,15,3)
       
        corr_values = np.correlate(smooth_voltage, subset)
        corr_values = corr_values -np.mean(corr_values)
        
 #       plt.subplot(2,1,1)
 #       plt.plot(subset)
 #       plt.subplot(2,1,2)
  #      plt.plot(corr_values)
   #     plt.show()

        corr_values_class = detectHeartBeat(corr_values)
        return corr_values_class
      
    

class detectHeartBeat:
    def __init__(self,corr_values_class):
        self.corr_values = corr_values_class

    def get_rid_of_neg(self):
        import matplotlib.pyplot as plt
        pos_corr_values = self.corr_values
        pos_corr_values[pos_corr_values < 0] = 0
        
        df = pd.DataFrame(pos_corr_values)
        mov_avg = df.rolling(30,center= False).mean()
        mov_avg = mov_avg.rolling(30, center = False).mean()
        
        poss_corr_values = mov_avg.as_matrix()
        return pos_corr_values


    def find_peaks(self, pos_corr_values):
        import matplotlib.pyplot as plt
        average = np.mean(pos_corr_values)
        print(average)
 
        threshold = average*8
        plt.plot(pos_corr_values)
        plt.plot((0, len(pos_corr_values)),(threshold,threshold), 'k-')
        plt.show()


        relative_max =argrelmax(pos_corr_values, order = 20)
        beats = pos_corr_values[relative_max [0]]
        beats = [item for item in beats if item >= threshold]

        print(len(beats))


def main(filename):
    x = importData(filename)
    data = x.readInData()
    data = x.makeObject(data)
    smooth_voltage =data.signalProcess()
    corr_values_class = data.max_find_correlation(smooth_voltage)   
    pos_corr_values = corr_values_class.get_rid_of_neg()
    corr_values_class.find_peaks(pos_corr_values)

#main('test_data1.csv')

