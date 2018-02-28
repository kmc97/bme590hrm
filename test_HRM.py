import pytest
import pandas as pd
import numpy as np


def test_import():
    from HRM import ImportData
    x = ImportData('test_data1.csv')
    voltage = x.read_in_data()
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


from HRM import DetectHeartBeat
data_array = np.array([1,2,3,19191,23,41,-2,41,1,2,3,4,5,6,7,8,8,2,2,4,24,32,1,41,141,13,3,3,3,3])
z = DetectHeartBeat(data_array)

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

from HRM import export_data
from HRM import get_data
def test_output_data():
    attributes = get_data('test_data1.csv')
    assert len(attributes) == 5

def test_json_writting():
    json_file_name = export_data('test_data1.csv')
    assert (json_file_name == 'test_data1.json')
     
