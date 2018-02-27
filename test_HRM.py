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
  #  from HRM import HeartRateData
    duration = x.find_duration()
    assert duration == -1212


def test_index_finder():
    index_time = x.find_beat_times(data_matrix, [1,2])
    assert index_time == [3, -1212]    
