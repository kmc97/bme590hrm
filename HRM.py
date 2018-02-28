import pandas as pd
import numpy as np
from scipy.signal import savgol_filter, argrelmax
import math


class ImportData:

    def __init__ (self, filename = None):
        self.filename = filename

    def read_in_data(self):
        """Function takes in a csv file name and returns a numpy array

        :param self.filename: csv filename
        :returns file_data_to_numpy: a 2d numpy array with time and voltage
        """

        file_data = pd.read_csv(self.filename, header= None)
        file_data_to_numpy = file_data.as_matrix()
        return file_data_to_numpy

    def make_object(self, file_data_to_numpy):
        """Function turns numpy array into object to be manipulated later
        
        :param file_data_to_numpy: numpy array
        :returns data: instance of data
        """
        data = HeartRateData(file_data_to_numpy)
        return data

 
class HeartRateData:
    
    def __init__ (self, data, index_time= None):
        self.data = data
        self.index_time = index_time
    
    def signal_process(self):
        """ Function removes noise with savgol filter and normalized

        :param self.data: data instance of time and voltage
        :returns smooth_voltage: single array of voltage
        """

     #   import matplotlib.pyplot as plt
        voltage = self.data[:,1]
        norm_voltage = voltage - np.mean(voltage)
        smooth_voltage = savgol_filter(norm_voltage, 15,3)
    #    plt.plot(smooth_voltage)
   #     plt.show()
        return smooth_voltage

    def find_voltage_extremes(self):
        """ Function takes array of voltage and finds maximum and minimum

        :param self.data: unfiltered time and voltage array
        :returns min_max: tuple of min and max
        """

        min_ = np.min(self.data[:,1])
        max_ = np.max(self.data[:,1])
        min_max = (min_,max_)
        print('Voltage Extremes (V):', min_max)
        return min_max

    def find_duration(self):
        """ Function returns last value of time array-- Duration of the ECG
   
        :param self.data: unfiltered time and voltage array
        :return time_duration: last value of time array
        """

        time = self.data[:,0]
        time_duration = time[len(time)-1]
        print('Time Duration of ECG strip (s):', time_duration)
        return time_duration

    def find_beat_times(self,data, index_time):
        """ Function takes index of heart beat events and returns the corresponding time values
       
        :param data: unfiltered time and voltage array
        :param index_time: an instance index of heart beat events
        :returns beat_times: array of times corresponding to heart beat events
        """
        beat_times = []
        time = data[:,0]

        for i in index_time:
            beat_times.append(time[i])
     
        print('Times of Beat Event (s):', beat_times)
     
        return(beat_times)


    def find_avg_hr(self, beat_times):
       
        """Function finds median time interval between heart beat events to calculate BPM
        :param beat_times: array of times of heart beat of events
        :returns bpm: average heart beat per minute
        """
        beat_diffs = np.diff(beat_times)
        median_interval = np.median(beat_diffs)
        bpm = round(60/median_interval)
        print('Average Heart Rate (BPM):', bpm)
        
        return(bpm)

    def max_find_correlation(self, smooth_voltage):
        """Function finds correlation values by correlating subset max QRS wave to rest of signal

        :param smooth_voltage: filtered voltage array
        :param subset_max_index: index of maximum voltage value
        :param subset: a subset of a single QRS wave based on maximum voltage value
        :returns corr_values_class: an instance of correlation values based on when heart beat occured
        """

#        import matplotlib.pyplot as plt
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
        
 #       plt.subplot(2,1,1)
  #      plt.plot(subset)
   #     plt.subplot(2,1,2)
    #    plt.plot(corr_values)
     #   plt.show()

        corr_values_class = DetectHeartBeat(corr_values)
        return corr_values_class
      
    

class DetectHeartBeat:
    def __init__(self,corr_values_class):
        self.corr_values = corr_values_class

    def get_rid_of_neg(self):
        """Function removes negative correlation values to help detect positive correlation values

        :param self.corr_values: instance of correlation values
        :returns pos_corr_values: only positive correlation values
        """

        pos_corr_values = self.corr_values
        pos_corr_values[pos_corr_values < 0] = 0
        
        df = pd.DataFrame(pos_corr_values)
        mov_avg = df.rolling(50,center= False).mean()
        
        poss_corr_values = mov_avg.as_matrix()
        return pos_corr_values


    def find_peaks(self, pos_corr_values):
        """Function finds relative max of correlations then filters out values that do not pass threshold.

        :param pos_corr_values: array of positive correlation values
        :param threshold: threshold to cuttoff what constitutes event, average*5.5
        :returns beats: array of correlation values at specific heart beat events
        """

      #  import matplotlib.pyplot as plt
        average = np.mean(pos_corr_values) 
        threshold = average*5.5
       # plt.plot(pos_corr_values)
       # plt.plot((0, len(pos_corr_values)),(threshold,threshold), 'k-')
       # plt.show()

        relative_max =argrelmax(pos_corr_values, order = 20)
        beats = pos_corr_values[relative_max [0]]
        beats = [item for item in beats if item >= threshold]

        return beats

    def number_beats(self, beats):
        """Function takes array of beat correlation values and returns the number of beats
  
        :param beats: array of correlation values at heart beat event
        :returns num_detected_beats: integer value number of beats
        """

        num_detected_beats = len(beats)
        print('Number of Detected Beats:', num_detected_beats)

        return num_detected_beats

    def find_peak_index(self, beats, pos_corr_values):
        """Function that takes relative max correlation values and finds indicies (heart beats)

        :param beats: array of correlation values at heart beat event
        :param pos_corr_values: array of correlation values
        :returns index_int: index of maximum correlation values (index of heart beat)
        """
        
        index_int = []
        for beat_index, k in enumerate(beats):
            for index_interval, j in enumerate(pos_corr_values):
           
                if j == beats[beat_index]:
                    index_int.append(index_interval)

        return index_int

    def make_object_time(self, index_int):
        index_time = HeartRateData(index_int)
        return index_time

def export_data(filename):
    """ Function takes all data and writes it into json file
 
    :param filename: csv filename
    :param attributes: avg hr, voltage extremes, ECG time duration, Number of beats, Beat times
    :returns json_name: file name of json file
    """

    import json
    json_name = filename.replace('.csv', '.json')
    attributes = get_data(filename)
    data = [{"avg_hr:" : attributes[0]},
            {"voltage extremes (V):": attributes[1]}, 
            {"ECG time duration (s):": attributes[2]},
            {"Number of Beats:": attributes[3]},
            {"array of heart beat times (s):": attributes[4]}]
    jsonfile = open(json_name, 'w')
    json.dump(data, jsonfile)
    jsonfile.write('\n')
 
    return json_name 

def get_data(filename):

    """ Function that messily calls all classes and functions to return data
    
    :param filename: csv filename
    :returns attributes: list of hr, volt_extremes, duration, num_beats, beat_times
    """

    #Import Data & create voltage/time object
    x = ImportData(filename)
    data = x.read_in_data()
    data_obj = x.make_object(data)

    #Determine voltage extremes and length of timeframe
    volt_extremes = data_obj.find_voltage_extremes()
    duration = data_obj.find_duration()

    #Determine Correlation and create object of peak events
    smooth_voltage =data_obj.signal_process()
    corr_values_class = data_obj.max_find_correlation(smooth_voltage)   
    pos_corr_values = corr_values_class.get_rid_of_neg()
    beats = corr_values_class.find_peaks(pos_corr_values)
   
    #Determine Number of beats
    num_beats = corr_values_class.number_beats(beats)
    
    #Determine Time stamp of beats and create object of time values
    index_int = corr_values_class.find_peak_index(beats,pos_corr_values)
    index_time = corr_values_class.make_object_time(index_int)   
   
    #Determine time of beat events and average heart rate
    beat_times= index_time.find_beat_times(data,index_int)
    hr = index_time.find_avg_hr(beat_times)
    
    attributes = [hr, volt_extremes, duration, num_beats, beat_times]   

    return attributes
    

def main(filename):
#    get_data(filename)
    export_data(filename)

#main('test_data4.csv')
