import pandas as pd
import numpy as np
from scipy.signal import savgol_filter, argrelmax
import logging


logging.basicConfig(filename='logging.txt', format='%(asctime)s %(message)s', datefmt ='%m/%d/%Y &I:%M:%S %p', level=logging.DEBUG)


class ReadWriteData:

    def __init__ (self, filename = None):
        self.filename = filename
        self.file_data = None
        self.data = None
     
    def read_in_data(self):
        """Function takes in a csv file name and returns a numpy array

        :param self.filename: csv filename
        :returns self.file_data: a 2d numpy array with time and voltage
        :raises IOError: makes sure import file is a .csv file
        :raises TypeError: make sure values inside ECG trace are floats
        """

        if self.filename.endswith('.csv'):
            pass
        else:
            raise IOError("the file you are trying to input is not a .csv file")

        file_data = pd.read_csv(self.filename, header= None)
        self.file_data = file_data.as_matrix()
       
        times = self.file_data[:,0]
        volts = self.file_data[:,1]
        data_check = [times,volts]
        
        for columns in data_check:
            for values in times:
                if isinstance(values, float):
                    pass 
                else:
                    raise TypeError('.csv file must contain data type float')

        return self.file_data



    def make_time_voltage_object(self):
        """Function turns numpy array into object to be manipulated later
        
        :param self.file_datay: numpy array
        :returns self.data: instance of data containing times and voltages
        """
        self.data = HeartRateData(self.file_data)
        return self.data 

    def export_data(self,filename,attributes):
        """Function takes list of final attributes and exports json file
   
        :param filename: csv filename
        :param attributes: avg hr, Volt extremes, time duration, num of beats and beat time array
        :returns json_name: file name of json file
        """

        import json
        json_output = [{"avg_hr:": attributes[0]},
                       {"Voltage Extremes (V):" : attributes[1]},
                       {"ECG Time Duration (s):": attributes[2]},
                       {"Number of Beats:": attributes[3]},
                       {"Array of Heart Beat Times (s):": attributes[4]}]

        json_name = filename.replace('.csv', '.json')
        jsonfile = open(json_name, 'w')
        json.dump(json_output, jsonfile)
        jsonfile.write('\n')

        logging.info('INFO: Created .json file')

class HeartRateData:
    
    def __init__ (self, data, index_time= None):
        self.data = data
        self.index_time = index_time
        self.smooth_voltage = None
        self.min_max = None
        self.time_duration = None
        self.beat_times = None
        self.bpm = None
        self.corr_values_class = None
        self.num_beats = None

    def signal_process(self):
        """ Function removes noise with savgol filter and normalized

        :param self.data: data instance of time and voltage
        :returns smooth_voltage: single array of voltage
        """
        
        voltage = self.data[:,1]
        norm_voltage = voltage - np.mean(voltage)
        self.smooth_voltage = savgol_filter(norm_voltage, 15,3)

#        import matplotlib.pyplot as plt
  #      plt.plot(self.smooth_voltage)
   #     plt.show()

        return self.smooth_voltage

    def find_voltage_extremes(self):
        """ Function takes array of voltage and finds maximum and minimum

        :param self.data: unfiltered time and voltage array
        :returns min_max: tuple of min and max
        """

        min_ = np.min(self.data[:,1])
        max_ = np.max(self.data[:,1])
        self.min_max = (min_,max_)
#        print('Voltage Extremes (V):', self.min_max)

        return self.min_max

    def find_duration(self):
        """ Function returns last value of time array-- Duration of the ECG
   
        :param self.data: unfiltered time and voltage array
        :return self.time_duration: last value of time array
        """

        time = self.data[:,0]
        self.time_duration = time[len(time)-1]
 #       print('Time Duration of ECG strip (s):', self.time_duration)

        return self.time_duration

    def find_beat_times(self, data, index_time):
        """ Function takes index of heart beat events and returns the corresponding time values
       
        :param data: unfiltered time and voltage array
        :param index_time: an instance index of heart beat events
        :returns self.beat_times: array of times corresponding to heart beat events
        """
        time = data[:,0]
        self.beat_times = []
      
        for i in index_time:
            self.beat_times.append(time[i])
     
  #      print('Times of Beat Event (s):', self.beat_times)
     
        return(self.beat_times)

    def find_number_beats(self):
        """ Function returns number of heart beat events

        :param self.beat_times: array of beat times
        :returns self.num_beats: number of total beats
        """

        self.num_beats = len(self.beat_times)
   #     print('Number of detected Beats:', self.num_beats)

        return self.num_beats

    def find_avg_hr(self,data, index_int, interval):
       
        """Function finds average hr over user specified time interval
        
        :param data: array that contains time and voltages
        :param index_int: array containing indicies of heart beat events
        :param interval: user defined value in minutes
        :returns self.bpm: list of average heart beat per minute
        """
        time = data[:,0]
        avg_time_step = np.mean(np.diff(time))
         
        avg_int_index = interval*60/avg_time_step
        avg_int_index = int(avg_int_index/np.mean(np.diff(index_int)))
          
        beat_diffs =[index_int[x:x+avg_int_index] for x in range(0, len(index_int), avg_int_index)]
        
        self.bpm = []        
        avg_hrs= []
        for arrays in beat_diffs:
            arrays = np.diff(arrays)
            avg_hr = np.mean(arrays)*avg_time_step
            avg_hrs.append(avg_hr)
      
        self.bpm = [x/(1/60) for x in avg_hrs]
        
        print('Average Heart Rate (BPM):', self.bpm)
       
        return(self.bpm)

    def max_find_correlation(self):
        """Function finds correlation values by correlating subset (max QRS wave) to rest of signal

        :param self.smooth_voltage: filtered voltage array
        :returns self.corr_values_class: an instance of correlation values based on when heart beat occured
        """

        subset_max_index = argrelmax(self.smooth_voltage, order = len(self.smooth_voltage))
        subset_max_index = subset_max_index[0]        
        subset_max_index = subset_max_index[0]
      
        interval = 30
        if subset_max_index < interval:
            interval = subset_max_index -1
        if (len(self.smooth_voltage)-subset_max_index < interval):
            interval = len(self.smooth_voltage)- subset_max_index-1 
        else:
            interval = interval

        subset = self.smooth_voltage[(subset_max_index-interval):(subset_max_index+interval)]
        subset = subset - np.mean(subset)
        subset = savgol_filter(subset,15,3)
       
        corr_values = np.correlate(self.smooth_voltage, subset)
        corr_values = corr_values -np.mean(corr_values)
        
        self.corr_values_class = DetectHeartBeat(corr_values)

        return self.corr_values_class
      
    def return_attributes(self,duration,min_max):
        """ Function takes final attributes and exports a list to be used for data exportation
        
        :param duration: length of ECG array
        :param min_max: voltage extremes of ECG array
        :returns attributes: list of final attributes
        """

        attributes = [self.bpm, self.num_beats, self.beat_times, duration, min_max]
        logging.info('INFO: final attributes collected')

        return attributes


class DetectHeartBeat:
    def __init__(self,corr_values_class):
        self.corr_values = corr_values_class
        self.pos_corr_values = None
        self.beats = None
        self.num_detected_beats = None
        self.index_int = None

    def get_rid_of_neg(self):
        """Function removes negative correlation values to help detect positive correlation values

        :param self.corr_values: instance of correlation values
        :returns self.pos_corr_values: only positive correlation values
        """

        self.pos_corr_values = self.corr_values
        self.pos_corr_values[self.pos_corr_values < 0] = 0
        
        df = pd.DataFrame(self.pos_corr_values)
        mov_avg = df.rolling(50,center= False).mean()
        
        self.poss_corr_values = mov_avg.as_matrix()

        return self.pos_corr_values

    def find_peaks(self):
        """Function finds relative max of correlations then filters out values that do not pass threshold.

        :param self.pos_corr_values: array of positive correlation values
        :returns self.beats: array of correlation values at specific heart beat events
        """

        average = np.mean(self.pos_corr_values) 
        threshold = average*5.5
    
        # impot matplotlib.pyplot as plt
       # plt.plot(self.pos_corr_values)
       # plt.plot((0, len(self.pos_corr_values)),(threshold,threshold), 'k-')
        #plt.show() 

        relative_max =argrelmax(self.pos_corr_values, order = 20)
        self.beats = self.pos_corr_values[relative_max [0]]
        self.beats = [item for item in self.beats if item >= threshold]

        return self.beats


    def find_peak_index(self):
        """Function that takes relative max correlation values and finds indicies (heart beats)

        :param self.beats: array of correlation values at heart beat event
        :param self.pos_corr_values: array of correlation values
        :returns self.index_int: index of maximum correlation values (index of heart beat)
        """
        
        self.index_int = []
        for beat_index, k in enumerate(self.beats):
            for index_interval, j in enumerate(self.pos_corr_values):
           
                if j == self.beats[beat_index]:
                    self.index_int.append(index_interval)

        return self.index_int

    def make_object_time(self):
        """ Function that makes heart beat time instance
        
        :param self.index_int: index of maximum correlation values (indicies of heart beats)
        :returns self.index_time: object containing indicies of heart beats
        """

        self.index_time = HeartRateData(self.index_int)
        
        return self.index_time
def interval_check(interval):
    """ Function checks to make sure interval is greater than zero

    :param interval: user input time interval
    :raises ValueError: value error raised if interval is 0 or negative
    """

    if interval<= 0:
        logging.info('WARNING: Exception raised, incorrect user input')
        raise ValueError 
    else:
        pass

def main(filename):
    logging.info('INFO: ECG analysis has started')

    #Import Data & create voltage/time object
    x = ReadWriteData(filename)
    data =x.read_in_data()
    data_obj =x.make_time_voltage_object()

    #Determine voltage extremes and length of timeframe
    min_max = data_obj.find_voltage_extremes()
    duration = data_obj.find_duration()

    #Determine Correlation and create object of peak events
    data_obj.signal_process()
    corr_values_class = data_obj.max_find_correlation()   
    corr_values_class.get_rid_of_neg()
    corr_values_class.find_peaks()
      
    #Determine Time stamp of beats and create object of time values
    index_int = corr_values_class.find_peak_index()
    index_time = corr_values_class.make_object_time()   
   
    #Determine time of beat events, number of beats and average heart rate
    index_time.find_beat_times(data, index_int)
    interval = float(input("Enter interval value for avg hr in minutes: "))
    logging.info('INFO: user input in minutes recieved')
 
    try:
        interval_check(interval)
    except ValueError:
        print('Rerun program and choose different time interval in minutes')

    index_time.find_avg_hr(data, index_int,interval)
    index_time.find_number_beats() 

    # Organize and export final attributes
    import os
    attributes = index_time.return_attributes(duration, min_max) 
    x.export_data(filename,attributes)

    logging.info('INFO: ECG analysis has ended')

#main('test_data1.csv')
