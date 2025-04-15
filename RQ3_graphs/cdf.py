import pandas as pd
import numpy as np

import sklearn.metrics as metrics
import scipy.stats as stats

import matplotlib.pyplot as mpl

mpl.rcParams['text.usetex'] = True
# default: [6.4, 4.8]
mpl.rcParams["figure.figsize"] = (6.4,4.1)
mpl.rcParams['font.size'] = '14'

xlabel = "$|F| / |Var(F)|$"
ylabel = "time (s)"

dpi = 600
f_id = 0


for sampler in ['d4', 'spur', 'unigen3', 'sharpSAT', 'mcTw']:
    cnf =  pd.read_csv("csv/ncls_smp_subsumtion.csv", skipinitialspace = True, index_col = 'file')
    d4 =  pd.read_csv(f"csv/{sampler}.csv", skipinitialspace = True, index_col = 'file')
    mc =  pd.read_csv("csv/mc.csv", skipinitialspace = True, index_col = 'file')

    data = cnf.join(d4, on = 'file')
    data = data.join(mc, on = 'file')


    data['#vc'] = data['#v'] - data['#vu'] - data['#vf']
    data = data[data['#vc'] > 0]
    data['r'] = data['#c-u'] / (data['#v'] - data['#vu'] - data['#vf'])


    done = data[data['state'] == 'done']
    fail = data[data['state'] != 'done']
    mem = data[data['state'] == 'mem']
    time = data[data['state'] == 'timeout']
    nb = len(data)

# done['rlmc'] = done['log2(#m)'] / done['#vc']


    f = mpl.figure(f_id)
    f_id += 1

    field = 'r'

    X = np.sort(data[field].to_numpy())
    Y = np.arange(len(data))
    mpl.plot(X, Y, label = 'all')

    X = np.sort(done[field].to_numpy())
    Y = np.arange(len(done))
    mpl.plot(X, Y, label = 'success')

    X = np.sort(fail[field].to_numpy())
    Y = np.arange(len(fail))
    mpl.plot(X, Y, label = 'out of memory or timeout')


    mpl.ylabel("Number of formulae")
    mpl.xlabel(xlabel)
    mpl.legend()
    mpl.minorticks_on()
    # mpl.grid()
    f.savefig(f"Figure 9 - CDF/cdf_{sampler}.png", dpi = dpi, bbox_inches = 'tight')

    crit = 2.2
    print(f"Sampler: {sampler}")
    print(f"done b: {len(done[done.r <= crit])} ; a: {len(done[done.r > crit])}")
    print(f"fail b: {len(fail[fail.r <= crit])} ; a: {len(fail[fail.r > crit])}")
    print(f"mem b: {len(mem[mem.r <= crit])} ; a: {len(mem[mem.r > crit])}")
    print(f"time b: {len(time[time.r <= crit])} ; a: {len(time[time.r > crit])}")
