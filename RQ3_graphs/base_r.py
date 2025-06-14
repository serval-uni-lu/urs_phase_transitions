import pandas as pd
import numpy as np

import sklearn.metrics as metrics
import scipy.stats as stats

import matplotlib.pyplot as mpl

mpl.rcParams['text.usetex'] = True
# default: [6.4, 4.8]
mpl.rcParams["figure.figsize"] = (6.4,4)
mpl.rcParams['font.size'] = '14'

xlabel = "$log_2(|R_F|) / |Var(F)|$"
ylabel = "time (s)"

dpi = 600

def get_v(data):
    # X = np.abs(((data['#c-u']) / (data['#v'] - data['#vu'] - data['#vf'] + 1)))
    X = data['log2(#m)'] / data['#v']
    Y = data.time
    return X, Y

total_time = dict()

f_id = 0
for sampler in ["unigen3", "spur", "d4", "sharpSAT", "mcTw"]:
    # cnf =  pd.read_csv("csv/ncls_smp.csv", skipinitialspace = True, index_col = 'file')
    cnf =  pd.read_csv("csv/ncls_smp_subsumtion.csv", skipinitialspace = True, index_col = 'file')
    d4 =  pd.read_csv(f"csv/{sampler}.csv", skipinitialspace = True, index_col = 'file')
    mc =  pd.read_csv("csv/mc.csv", skipinitialspace = True, index_col = 'file')

    data = cnf.join(d4, on = 'file')
    data = data.join(mc, on = 'file')
    data.dropna(inplace = True)


    if sampler not in total_time:
        total_time[sampler] = 0
    # data.dropna(inplace = True)

    data['#vc'] = data['#v'] - data['#vu'] - data['#vf']
    data = data[data['#vc'] > 0]
    # data['r'] = data['#c-u'] / (data['#v'] - data['#vu'] - data['#vf'])
    data['r'] = data['log2(#m)'] / data['#v']

    # data = data[data['r'] <= 10]

    done = data[data['state'] == 'done']
    mem = data[data['state'] == 'mem']
    time = data[data['state'] == 'timeout']
    nb = len(data)

    # done['rlmc'] = done['log2(#m)'] / done['#vc']


    total_time[sampler] += done.time.sum()

    orig_r = data.r

    print(f"{sampler}: nb data points: {len(data)}")

    X, Y = get_v(data)
    # data = data[data['#c-u'] / (data['#v'] - data['#vu'] - data['#vf'] + 1) <= 10]
    X_r, Y_r = get_v(data)

    done_r = data[data['state'] == 'done']
    mem_r = data[data['state'] == 'mem']
    time_r = data[data['state'] == 'timeout']
    nb_r = len(data)

    Xd, Yd = get_v(done)
    Xm, Ym = get_v(mem)
    Xt, Yt = get_v(time)

    Xd_r, Yd_r = get_v(done_r)
    Xm_r, Ym_r = get_v(mem_r)
    Xt_r, Yt_r = get_v(time_r)

    f = mpl.figure(f_id)
    f_id += 1

    mpl.ylabel("Number of formulae")
    mpl.xlabel(xlabel)
    mpl.hist(orig_r, 100, color='grey', alpha = 0.5, label = "number of formulae")
    mpl.twinx()

    mpl.ylabel(ylabel)
    mpl.minorticks_on()
    # mpl.title("nb points: " + str(nb))
    mpl.scatter(Xd, Yd, marker = '.', label = 'success')
    mpl.scatter(Xm, Ym, marker = '.', label = 'out of memory')
    mpl.scatter(Xt, Yt, marker = '.', label = 'timeout')
    mpl.legend()
    f.savefig(f"Figure 8 - base/{sampler}_r_complete.png", dpi = dpi, bbox_inches = 'tight')


print("")
for s in total_time:
    print(f"{s}:\t{total_time[s]}")
