import math
import numpy as np
import pandas as pd
from scipy.signal import butter, lfilter


class WaveAnalysis:
    def __init__(self, input_data = None):
        self.cutoffFrequency = 7800
        self.sample_rate = 44100

    def butter_bandpass(self, lowcut=0, highcut=-1, fs=8000, order=1):
        if highcut < 0:
            highcut = self.cutoffFrequency
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a


    def butter_bandpass_filter(self, lowcut=0, highcut=-1,
                               fs=8000, order=1):
        if highcut < 0:
            highcut = self.cutoffFrequency
        b, a = self.butter_bandpass(lowcut=lowcut, highcut=highcut,
                                     fs=fs, order=order)
        y = lfilter(b, a, data)
        return y

    def open_wav_audiolab(self, filename):
        #http://scikits.appspot.com/audiolab
        from scikits.audiolab import wavread
        results, sample_frequency,encoding = wavread(filename)
        self.sample_rate = sample_frequency
        print 'Sample Rate is ', sample_frequency
        return results, self.sample_rate

    def open_wav_wave(self, filename):
        import wave, struct
        results = []
        waveFile = wave.open(filename, 'r')
        length = waveFile.getnframes()
        for i in range(0,length):
            waveData = waveFile.readframes(1)
            data = struct.unpack("<h", waveData)
            results.append(int(data[0]))
        print 'Sample Rate is ', self.sample_rate
        return np.array(results), self.sample_rate

    def high_pass_filter(self, data):
        #http://phrogz.net/js/framerate-independent-low-pass-filter.html
        k = math.exp(-(self.cutoffFrequency*2*3.1415)/self.sample_rate)
        new_data = []
        print "Sample Rate = %i, Cutoff F = %i, k = %2f" %(self.sample_rate, self.cutoffFrequency, k)
        for i in range(0, len(data)):
            if len(new_data) > 0:
                new_data.append(k*new_data[i-1] + data[i] + data[i-1])
            else:
                new_data.append(data[i])
        return new_data

class Statistics:
    def __init__(self, input_array = None):
        self.input_array = input_array

    def sum_slice(self, array=None, s=0, e=None):
        if array is None:
            array = self.input_array
        if e is None:
            e = len(array) - 1
        return sum(array[s:e])


