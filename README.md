# bme590hrm
Heart Rate Monitor Assignment

Description: Program transforms ECG strip into useful information such as average heart rate value, the voltage extremes, the duration of the ECG strip, the number of detected beats and a list of times at which the heart beats occur.

Inputs: a single .csv file is used in the main function of this script

Outputs: a .json file that contains a list of the BPM, voltage extremes, duration of ECG strip, beats detected and list of times at which the heart beat occurs.

Limitations: the correlation values are determined by taking the MAXIMUM QRS peak, if the signal were to suddently drift off this could lead to a poor correlation subset.

[![Build Status](https://travis-ci.org/kmc97/bme590hrm.svg?branch=master)](https://travis-ci.org/kmc97/bme590hrm)

MIT License
Copyright (c) [2018] [Katie Carroll]
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRNATIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
