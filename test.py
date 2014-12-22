import pandas as pd
from scipy.io.wavfile import read as scipy_read
import matplotlib.pyplot as plt
import numpy as np
import statistics

FILENAME = "/home/tammy/WorkDiary/Projects/captainchirp/client/test/samples/1-ipad.wav"
N_skip = 24
N_group = 100 #On iphone, roughly equal to 137
st = statistics.Statistics()

results = np.fromfile(open(FILENAME),np.int16)[N_skip:]
N_samples = len(results)


#For drawing only
array = []
for i in range(0, N_samples/N_group):
    value = st.sum_slice(array=results, s=i*N_group, e=i*N_group+N_group)
    array.append(value/N_group)
s = pd.Series(array)
s.plot()
plt.show()
