import pytest
import pandas as pd
import numpy as np


def test_import():
    from HRM import ReadWriteData
    x = ReadWriteData('test_data1.csv')
    voltage = x.read_in_data()
    assert(voltage[0,0] == 0)
    assert(voltage[8,1] == -.12)

def test_file_name():
    from HRM import ReadWriteData
    with pytest.raises(IOError):
        y = ReadWriteData('csv_less')
        y.read_in_data()

def test_values_in_matrix():
    from HRM import ReadWriteData
    with pytest.raises(TypeError):
        z = ReadWriteData('wrong.csv')
        z.read_in_data()

def test_json_file_creation():
    import os
    import json

    from HRM import ReadWriteData
    x = ReadWriteData('test_data1.csv')
    x.export_data('test_data1.csv', [1,2,3,4,5])

    if os.path.isfile('test_data1.json'):
        x= 1
    else:
        x = 0
    
    assert x == 1

    data = open('test_data1.json').read()
    values = json.loads(data)
    assert values[0] == {'avg_hr:': 1}
 

from HRM import HeartRateData
data_matrix = np.array([[1,2], [3,9],[-1212,-1], [50,4]])
x = HeartRateData(data_matrix)

def test_min_max_extremes(): 
    extrema = x.find_voltage_extremes()
    assert(extrema[0] == -1)
    assert(extrema[1] == 9)
    
def test_duration():
    duration = x.find_duration()
    assert duration == 50

def test_index_finder():
    index_time = x.find_beat_times(data_matrix, [1,2,3])
    assert index_time == [3, -1212,50]    

def test_num_beats():
    num_beats = x.find_number_beats()
    assert num_beats == 3


def test_average():
    pass
    # this function is super gross to test and in future iterations would need to clean it up

def test_attribute_return():
    attributes = x.return_attributes(25, [1,2])
    assert len(attributes) ==5 

from HRM import DetectHeartBeat
data_array = np.array([1,-21,1,1,4,490,5,-1,1,2,3,4,5,-1,1,5,5,2,2,4,-1,32,1,1,1,3,3,3,3,3])
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
    values = z.find_peaks()
    if (values>= avg).all():
        x = 0
    else:
        x = 1
    assert x == 0

def test_find_index():
    values = z.find_peak_index()
    assert values == [5]


