import pandas as pd
import matplotlib.pyplot as plt
from os.path import join
import numpy as np
import math
import analysis

ROOT_LOC = "/home/tammy/WorkDiary/Projects/captainchirp/client/test/samples/"
wa = analysis.WaveAnalysis()
st = analysis.Statistics()

def list_files(LOC=ROOT_LOC):
    from os import listdir
    from os.path import isfile
    return [ f for f in listdir(LOC) if isfile(join(LOC,f)) and f.find('.wav') != -1 ]

def create_file_name_from_now(suffix='png'):
    from datetime import datetime
    dt = datetime.now()
    return dt.strftime("%Y-%B-%d:%p_%I_%M") + "." + suffix.replace(".", "")

def normalize_array(input_array):
    array = []
    N_group = 100 #On iphone, roughly equal to 137
    MAX = float(np.amax(input_array))
    print "Use MAX value = %i to normalize." %MAX
    new_MAX = -1
    for i in range(0, N_samples/N_group):
        value = st.sum_slice(array=input_array, s=i*N_group, e=i*N_group+N_group)/N_group/MAX
        if value > new_MAX:
            new_MAX = value 
        array.append(value)
    return np.array(array), new_MAX

IS_EXPORT = False
FIG_LOC = '/tmp'
FIG_TITLE="Wave Display"

N_ROW = 3
_N_total = len(wave_files)
N_COL = _N_total/N_ROW if _N_total%N_ROW == 0 else _N_total/N_ROW + 1

wave_files = list_files()
EXPORT_NAME = create_file_name_from_now()
plt.close('all')
fig = plt.figure()
plt.title(FIG_TITLE)

for i in range(0, _N_total):
    FILENAME = join(ROOT_LOC, wave_files[i])
    results, SAMPLERATE = wa.open_wav_audiolab(FILENAME)
    #results, SAMPLERATE = wa.open_wav_wave(FILENAME)
    #results = np.fromfile(open(FILENAME),np.int16)[24:]
    results = abs(results)
    N_samples = len(results)
    ax = plt.subplot2grid((N_ROW, N_COL), (i/N_ROW, i%N_ROW))
    ax.set_title(wave_files[i])
    normalized_array, max_value = normalize_array(results)
    ax.set_ylim([0, max_value*1.1])
    print "(%i, %i), (%i, %i) i = %i" %(N_ROW, N_COL, i/N_ROW, i%N_ROW, i)
    s = pd.Series(normalized_array)
    s.plot(ax)
plt.tight_layout()

if IS_EXPORT:
    fullpath = FIG_LOC + '/' + EXPORT_NAME
    plt.savefig(fullpath)
    print "Image is saved to %s" %fullpath
else:
    plt.show() #Can either show or savefig

