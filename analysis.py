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
        print 'Sample Rate is ', sample_frequency
        return results, self.sample_rate

'''
#http://phrogz.net/js/framerate-independent-low-pass-filter.html
#high pass filter
k = math.exp(1-(m_cutoffFrequency * 2 * 3.1415)/SAMPLERATE) #used for highpass filter
new_results = []
for i in range(0, len(results)):
    if len(new_results) > 0:
        new_results.append(new_results[i-1] + results[i] + results[i-1])
    else:
        new_results.append(results[i])

'''

class Statistics:
    def __init__(self, input_array = None):
        self.input_array = input_array

    def sum_slice(self, array=None, s=0, e=None):
        if array is None:
            array = self.input_array
        if e is None:
            e = len(array) - 1
        return sum(array[s:e])


