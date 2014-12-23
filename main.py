import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os.path import join

import analysis

ROOT_LOC = "/home/tammy/WorkDiary/Projects/captainchirp_samples/"
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
    cut_off_bin = 60 #avoid the initial noise
    N_samples = len(input_array)
    MAX = float(np.amax(input_array))
    print "Use MAX value = %i to normalize." %MAX
    new_MAX = -1
    for i in range(0, N_samples/N_group):
        value = st.sum_slice(array=input_array, s=i*N_group, e=i*N_group+N_group)/N_group/MAX
        if value > new_MAX:
            new_MAX = value 
        array.append(value)
    return np.array(array[cut_off_bin:]), new_MAX

def main():

    parser = argparse.ArgumentParser(description='Post ibs info to Launchpad.')
    parser.add_argument('-e', '--export', action="store_const", const=True ,
            default=False, help='Export PNG file (defailt: False)')
    parser.add_argument('-t','--title', 
            default="Wave Display", help='Title of the figure (default: "Wave Display")')
    parser.add_argument('-f','--filter', 
            default="HPF", help='Filter to be used: HPF. (default: HPF)')
    parser.add_argument('-o','--exportloc',
            default="/tmp", help='Location to export image (default: /tmp)')
    parser.add_argument('-l', '--logy', action="store_const", const=True ,
            default=False, help='Set log scale for y axis (defailt: False)')
    parser.add_argument('-p','--legpos', type=int,
            default=0, help='Position of legend (default: 0)')
    parser.add_argument('-r','--rows', type=int,
            default=3, help='Number of rows (default: 3)')

    args = parser.parse_args()
    N_ROW = args.rows

    wave_files = list_files()
    _N_total = len(wave_files)
    N_COL = _N_total/N_ROW if _N_total%N_ROW == 0 else _N_total/N_ROW + 1

    EXPORT_NAME = create_file_name_from_now()
    plt.close('all')
    plt.title(args.title)
    fig, axes = plt.subplots(nrows=N_ROW, ncols=N_COL)

    for i in range(0, _N_total):
        FILENAME = join(ROOT_LOC, wave_files[i])
        results, SAMPLERATE = wa.open_wav_audiolab(FILENAME)
        #results, SAMPLERATE = wa.open_wav_wave(FILENAME)
        #results = np.fromfile(open(FILENAME),np.int16)[24:]

        results = abs(results)
        normalized_array, max_value = normalize_array(results)
        d = {'Raw Data': normalized_array}
        if args.filter == 'HPF':
            high_pass_data = wa.high_pass_filter(results)
            normalized_high_pass, max_2 = normalize_array(high_pass_data)
            d['High Pass'] = normalized_high_pass

        kw = {'ax': axes[i/N_ROW, i%N_ROW], 'legend': False}
        if i == args.legpos:
            kw['legend'] = True
        if args.logy:
            kw['logy'] = True
        else:
            axes[i/N_ROW, i%N_ROW].set_ylim([0, max_value*1.05])
        df = pd.DataFrame(d)
        df.plot(**kw)
        axes[i/N_ROW, i%N_ROW].set_title(wave_files[i])

    plt.tight_layout()

    if args.export:
        fullpath = args.exportloc + '/' + EXPORT_NAME
        plt.savefig(fullpath)
        print "Image is saved to %s" %fullpath
    else:
        plt.show() #Can either show or savefig

if __name__ == "__main__":
    main()


