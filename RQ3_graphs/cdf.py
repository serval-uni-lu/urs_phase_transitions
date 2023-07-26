import pandas as pd
import numpy as np

import sklearn.metrics as metrics
import scipy.stats as stats

import matplotlib.pyplot as mpl

mpl.rcParams['text.usetex'] = True

xlabel = "$|F| / |Var(F)|$"
ylabel = "time (s)"

dpi = 200
f_id = 0


for sampler in ['d4', 'spur', 'unigen3', 'sharpSAT', 'mcTw']:
    cnf =  pd.read_csv("data/ncls_smp_subsumtion.csv", skipinitialspace = True, index_col = 'file')
    d4 =  pd.read_csv(f"data/{sampler}.csv", skipinitialspace = True, index_col = 'file')
    mc =  pd.read_csv("data/mc.csv", skipinitialspace = True, index_col = 'file')

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
    mpl.plot(X, Y, label = 'done')

    X = np.sort(fail[field].to_numpy())
    Y = np.arange(len(fail))
    mpl.plot(X, Y, label = 'fail')


    mpl.ylabel("Number of formulas")
    mpl.xlabel(xlabel)
    mpl.legend()
    mpl.minorticks_on()
    f.savefig(f"cdf_{sampler}.png", dpi = dpi, bbox_inches = 'tight')

    crit = 2.2
    print(f"Sampler: {sampler}")
    print(f"done b: {len(done[done.r <= crit])} ; a: {len(done[done.r > crit])}")
    print(f"fail b: {len(fail[fail.r <= crit])} ; a: {len(fail[fail.r > crit])}")
    print(f"mem b: {len(mem[mem.r <= crit])} ; a: {len(mem[mem.r > crit])}")
    print(f"time b: {len(time[time.r <= crit])} ; a: {len(time[time.r > crit])}")
