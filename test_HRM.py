import pytest
import pandas as pd
import numpy as np


def test_import():
    from HRM import ManipulateData
    x = ManipulateData('test_data1.csv')
    voltage = x.readInData()
    assert(voltage[0,0] == 0)
    assert(voltage[8,1] == -.12)

from HRM import HeartRateData
data_matrix = np.array([[1,2],[3,9],[-1212,-1]])
x = HeartRateData(data_matrix)

def test_min_max_extremes(): 
    extrema = x.find_voltage_extremes()
    assert(extrema[0] == -1)
    assert(extrema[1] == 9)
    
def test_duration():
    duration = x.find_duration()
    assert duration == -1212


def test_index_finder():
    index_time = x.find_beat_times(data_matrix, [1,2])
    assert index_time == [3, -1212]    


average_matrix= np.array([1,3,6,10])
y = HeartRateData(average_matrix)

def test_average():
    average = y.find_avg_hr(average_matrix)
    assert  average == 20


from HRM import detectHeartBeat
data_array = np.array([1,2,3,19191,23,41,-2,41])
z = detectHeartBeat(data_array)

def test_positive_values():
    values = z.get_rid_of_neg()
    if (values >= 0).all():
        x = 0
    else:
        x = 1
    assert x == 0

def test_beat_threshold():
    avg = np.mean(data_array)*5.5
    values = z.find_peaks(data_array)
    if (values>= avg).all():
        x = 0
    else:
        x = 1
    assert x == 0

def test_find_index():
    values = z.find_peak_index([19191], data_array)
    assert values == [3]

