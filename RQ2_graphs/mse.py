import pandas as pd
import numpy as np

import matplotlib.pyplot as mpl

mpl.rcParams['text.usetex'] = True
mpl.rcParams["figure.figsize"] = (6.4,4.1)
mpl.rcParams['font.size'] = '14'
nb_fig = 1
dpi = 100

def median_vals(data, xkey, ykey, epsilon = 0.01):
    vals = set(data[xkey].to_numpy())

    res = {}

    for nc in vals:
        mask = [data[xkey][i] > nc - epsilon and data[xkey][i] < nc + epsilon for i in data[xkey].keys()]
        # tmp = data[data[xkey] >= nc - epsilon or data[xkey] <= nc + epsilon]
        tmp = data[mask]
        tmp = tmp[ykey].to_numpy()
        # tmp = np.median(tmp)
        tmp = np.mean(tmp)
        res[nc] = [tmp]

    return pd.DataFrame(res).T

# ylabel_f1 = 'relative memory'
# ylabel_f2 = 'relative memory ; $log_2(|R_F|) / |Var(F)|$'
# ylabel_f4 = '$|F| / |Var(F)|$'
# yfield = 'mem'

ylabel_f1 = 'relative time'
ylabel_f2 = 'relative time ; $log_2(|R_F|) / |Var(F)|$'
ylabel_f4 = '$|F| / |Var(F)|$'
yfield = 'time'

# for s in ["d4", "spur", "sharpSAT", "ug3", "mcTw"]:
for s in ["d4"]:
    f1 = mpl.figure(nb_fig)
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
        d.mem /= d.mem.max()

        mlmc = median_vals(d, 'lmc_ratio', yfield, epsilon = 0.02)
        mr = median_vals(d, 'ratio', yfield, epsilon = 0.3)

        fail = d[d.state != 'done']
        succ = d[d.state == 'done']
        mem = d[d.state == 'mem']
        t = d[d.state == 'timeout']

        mpl.figure(f1)
        mpl.scatter(succ['ratio'], succ[yfield], label = f'k = {i}', marker = '.')
        mpl.scatter(mem['ratio'], mem[yfield], label = f'(out of mem) k = {i}', marker = '.')
        mpl.scatter(t['ratio'], t[yfield], label = f'(timeout) k = {i}', marker = '.')

        if i == 4:
            mpl.scatter(mr[0].keys(), mr[0], marker = '.', color = 'black')

        mpl.figure(f3)
        mpl.scatter(succ.lmc_ratio, succ[yfield], label = f'k = {i}', marker = '.')

        if i == 4:
            mpl.scatter(mlmc[0].keys(), mlmc[0], marker = '.', color = 'black')


    mpl.figure(f1)
    mpl.legend()
    # mpl.grid()
    mpl.xlabel("$|F| / |Var(F)|$")
    mpl.ylabel(ylabel_f1)
    mpl.minorticks_on()
    # mpl.xlim(right = 7)
    mpl.savefig(f"var_k_f1_{s}.png", dpi = dpi, bbox_inches = 'tight')


    mpl.figure(f3)
    mpl.legend()
    # mpl.grid()
    mpl.xlabel("$log_2(|R_F|) / |Var(F)|$")
    mpl.ylabel(ylabel_f1)
    mpl.minorticks_on()
    # mpl.xlim(left = 0.1)
    mpl.savefig(f"var_k_f3_{s}.png", dpi = dpi, bbox_inches = 'tight')
