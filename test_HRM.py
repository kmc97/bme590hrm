import pytest

from HRM import HeartRate

test_file1 = HeartRate("test_data1.csv")


def test_import():
    voltage = test_file1.parseData()
    assert(voltage.iloc[15]['Voltage'] == -0.175)
