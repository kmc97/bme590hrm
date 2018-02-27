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
    def __init__ (self, data, index_time= None):
        self.data = data
        self.index_time = index_time
    
    def signalProcess(self):
        import matplotlib.pyplot as plt
        voltage = self.data[:,1]
        norm_voltage = voltage - np.mean(voltage)
        smooth_voltage = savgol_filter(norm_voltage, 15,3)
#        plt.plot(smooth_voltage)
#        plt.show()
        return smooth_voltage

    def find_voltage_extremes(self):
        min_ = np.min(self.data[:,1])
        max_ = np.max(self.data[:,1])
        min_max = (min_,max_)
        print('Voltage Extremes (V):', min_max)
        return min_max

    def find_duration(self):
        time = self.data[:,0]
        time_duration = time[len(time)-1]
        print('Time Duration of ECG strip (s):', time_duration)
        return time_duration

    def find_beat_times(self,data, index_time):
        beat_times = []
        time = data[:,0]

        for i in index_time:
            beat_times.append(time[i])
        beat_times =np.array(beat_times)
        print('Times of Beat Event (s):', beat_times)
     
        return(beat_times)


    def find_avg_hr(self, beat_times):
        beat_diffs = np.diff(beat_times)
        avg_interval = np.mean(beat_diffs)
        bpm = round(avg_interval*2*60)
        print('Average Heart Rate (BPM):', bpm)
        
        return(bpm)

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


        subset = smooth_voltage[(subset_max_index-interval):(subset_max_index+interval)]
        subset = subset - np.mean(subset)
        subset = savgol_filter(subset,15,3)
       
        corr_values = np.correlate(smooth_voltage, subset)
        corr_values = corr_values -np.mean(corr_values)
        
#        plt.subplot(2,1,1)
 #       plt.plot(subset)
  #      plt.subplot(2,1,2)
   #     plt.plot(corr_values)
    #    plt.show()

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
        
        poss_corr_values = mov_avg.as_matrix()
        return pos_corr_values


    def find_peaks(self, pos_corr_values):
        import matplotlib.pyplot as plt
        average = np.mean(pos_corr_values)
 
        threshold = average*8
        plt.plot(pos_corr_values)
        plt.plot((0, len(pos_corr_values)),(threshold,threshold), 'k-')
        plt.show()


        relative_max =argrelmax(pos_corr_values, order = 20)
        beats = pos_corr_values[relative_max [0]]
        beats = [item for item in beats if item >= threshold]
        detected_beats = len(beats)
        print('Number of Detected Beats:', detected_beats)

        return beats

    def find_peak_index(self, beats, pos_corr_values):
        index_int = []
        for beat_index, k in enumerate(beats):
            for index_interval, j in enumerate(pos_corr_values):
           
                if j == beats[beat_index]:
                    index_int.append(index_interval)

        return index_int

    def make_time_object(self, index_int):
        index_time = HeartRateData(index_int)

        return index_time

      

def main(filename):
    x = importData(filename)
    data = x.readInData()
    data_obj = x.makeObject(data)
    data_obj.find_voltage_extremes()
    data_obj.find_duration()
    smooth_voltage =data_obj.signalProcess()
    corr_values_class = data_obj.max_find_correlation(smooth_voltage)   
    pos_corr_values = corr_values_class.get_rid_of_neg()
    beats = corr_values_class.find_peaks(pos_corr_values)
    index_int = corr_values_class.find_peak_index(beats,pos_corr_values)
    index_time = corr_values_class.make_time_object(index_int)   
    beat_times= index_time.find_beat_times(data,index_int)
    index_time.find_avg_hr(beat_times)


#main('test_data1.csv')

