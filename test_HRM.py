import pytest
import pandas as pd
import numpy as np

def test_import():
    from HRM import importData
    x = importData('test_data1.csv')
    voltage = x.readInData()
    assert(voltage[0,0] == 0)
    assert(voltage[8,1] == -.12)
