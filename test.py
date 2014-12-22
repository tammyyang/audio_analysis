import pandas as pd
from scipy.io.wavfile import read as scipy_read
import matplotlib.pyplot as plt
import numpy as np
import statistics

#FILENAME = "/home/tammy/WorkDiary/Projects/captainchirp/client/beep.wav"
FILENAME = "/home/tammy/WorkDiary/Projects/captainchirp/client/test/samples/1-ipad.wav"
N_skip = 24
N_group = 100 #On iphone, roughly equal to 137
st = statistics.Statistics()

results = np.fromfile(open(FILENAME),np.int16)[N_skip:]
N_samples = len(results)


#For drawing only
def create_file_name_from_now(suffix='png'):
    from datetime import datetime
    dt = datetime.now()
    return dt.strftime("%Y-%B-%d:%p_%I_%M") + "." + suffix.replace(".", "")

def draw_img(drawing_list, filename=None, loc='/tmp/', 
             export=True, title="Wave Display"):
    if filename is None:
        filename = create_file_name_from_now()
    s = pd.Series(drawing_list)
    plt.title(title)
    s.plot()
    if export:
        fullpath = loc + '/' + filename
        plt.savefig(fullpath)
        print "Image is saved to %s" %fullpath
    else:
        plt.show() #Can either show or savefig

new_results = results
'''
#http://phrogz.net/js/framerate-independent-low-pass-filter.html
#high pass filter
new_results = []
for i in range(0, len(results)):
    if len(new_results) > 0:
        new_results.append(new_results[i-1] + results[i] + results[i-1])
    else:
        new_results.append(results[i])

'''
array = []
for i in range(0, N_samples/N_group):
    value = st.sum_slice(array=new_results, s=i*N_group, e=i*N_group+N_group)
    array.append(value/N_group)
draw_img(array, export=False)
