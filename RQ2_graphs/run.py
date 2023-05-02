import pandas as pd
import numpy as np

import matplotlib.pyplot as mpl

mpl.rcParams['text.usetex'] = True
nb_fig = 1
dpi = 200

for s in ["d4", "spur", "sharpSAT", "ug3", "mcTw"]:
    f1 = mpl.figure(nb_fig)
    nb_fig += 1
    f2 = mpl.figure(nb_fig)
    nb_fig += 1
    f3 = mpl.figure(nb_fig)
    nb_fig += 1

    for i in range(3, 5):
        ncls = pd.read_csv(f"data/r50k{i}_cls.csv", skipinitialspace = True, index_col = 'file')
        sp = pd.read_csv(f"data/r50k{i}_{s}.csv", skipinitialspace = True, index_col = 'file')
        mc = pd.read_csv(f"data/r50k{i}_mc.csv", skipinitialspace = True, index_col = 'file')

        d = ncls.join(sp, on = 'file').join(mc, on = 'file')
        d['ratio'] = d['#c'] / d['#v']
        d['lmc_ratio'] = d['log2(#m)'] / d['#v']

        # d.dropna(inplace = True)
        # data[i] = d[d.state == 'done']
        print(f"{s}: max time for k={i}: {d.time.max()} (min: {d.time.min()})")
        print(f"{s}: max mem for k={i}: {d.mem.max()} (min: {d.mem.min()})")
        d.time /= d.time.max()

        succ = d[d.state == 'done']
        mem = d[d.state == 'mem']
        t = d[d.state == 'timeout']

        mpl.figure(f1)
        mpl.scatter(succ['ratio'], succ['time'], label = f'k = {i}', marker = '.')
        mpl.scatter(mem['ratio'], mem['time'], label = f'(out of mem) k = {i}', marker = '.')
        mpl.scatter(t['ratio'], t['time'], label = f'(timeout) k = {i}', marker = '.')

        mpl.figure(f2)
        mpl.scatter(succ.ratio, succ.time, label = f'k = {i}', marker = '.')
        mpl.scatter(succ.ratio, succ.lmc_ratio, label = f'lmc / var k = {i}', marker = '.')

        mpl.figure(f3)
        mpl.scatter(succ.lmc_ratio, succ.time, label = f'k = {i}', marker = '.')


    mpl.figure(f1)
    mpl.legend()
    mpl.grid()
    mpl.xlabel("$|F| / |Var(F)|$")
    mpl.ylabel("relative time")
    mpl.minorticks_on()
    # mpl.xlim(right = 7)
    mpl.savefig(f"var_k_f1_{s}.png", dpi = dpi, bbox_inches = 'tight')


    mpl.figure(f2)
    mpl.legend()
    mpl.grid()
    mpl.xlabel("$|F| / |Var(F)|$")
    mpl.ylabel("relative time ; $log_2(|R_F|) / |Var(F)|$")
    mpl.minorticks_on()
    mpl.savefig(f"var_k_f2_{s}.png", dpi = dpi, bbox_inches = 'tight')

    mpl.figure(f3)
    mpl.legend()
    mpl.grid()
    mpl.xlabel("$log_2(|R_F|) / |Var(F)|$")
    mpl.ylabel("relative time")
    mpl.minorticks_on()
    # mpl.xlim(left = 0.1)
    mpl.savefig(f"var_k_f3_{s}.png", dpi = dpi, bbox_inches = 'tight')
