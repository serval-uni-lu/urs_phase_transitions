import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

EF = mean_absolute_error

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

    return (pd.DataFrame(res).T).sort_index()

def pred(data, x):
    xs = data[0].keys().to_numpy()

    pos = -1
    for i in range(0, len(xs) - 1):
        if xs[i] == x:
            return data[0][xs[i]]
        elif xs[i + 1] == x:
            return data[0][xs[i + 1]]
        elif xs[i] <= x and xs[i + 1] >= x:
            pos = i
            break

    dx = xs[pos + 1] - xs[pos]
    lx = (x - xs[pos]) / dx

    dy = data[0][xs[pos + 1]] - data[0][xs[pos]]
    py = data[0][xs[pos]] + (dy * lx)

    return py

yfield = 'time'

for s in ["d4", "spur", "sharpSAT", "ug3", "mcTw"]:
# for s in ["d4", "spur", "ug3"]:

    print(f"### {s}")
    i = 4
    ncls = pd.read_csv(f"data/r50k{i}_cls.csv", skipinitialspace = True, index_col = 'file')
    sp = pd.read_csv(f"data/r50k{i}_{s}.csv", skipinitialspace = True, index_col = 'file')
    mc = pd.read_csv(f"data/r50k{i}_mc.csv", skipinitialspace = True, index_col = 'file')

    d = ncls.join(sp, on = 'file').join(mc, on = 'file')
    d['ratio'] = d['#c'] / d['#v']
    d['lmc_ratio'] = d['log2(#m)'] / d['#v']

    d.time /= d.time.max()
    d.mem /= d.mem.max()

    mlmc = median_vals(d, 'lmc_ratio', yfield, epsilon = 0.06)
    mr = median_vals(d, 'ratio', yfield, epsilon = 0.3)

    mlmc[0] /= mlmc[0].max()
    mr[0] /= mr[0].max()

    ytrue = d['time'].to_numpy()
    xs = d['ratio'].to_numpy()
    ypred = [pred(mr, x) for x in xs]
    tmp = EF(ytrue, ypred)
    print(f"   k = 4 (#c / #v): {tmp}")

    ytrue = d['time'].to_numpy()
    xs = d['lmc_ratio'].to_numpy()
    ypred = [pred(mlmc, x) for x in xs]
    tmp = EF(ytrue, ypred)
    print(f"   k = 4 (r): {tmp}")


    i = 3
    ncls = pd.read_csv(f"data/r50k{i}_cls.csv", skipinitialspace = True, index_col = 'file')
    sp = pd.read_csv(f"data/r50k{i}_{s}.csv", skipinitialspace = True, index_col = 'file')
    mc = pd.read_csv(f"data/r50k{i}_mc.csv", skipinitialspace = True, index_col = 'file')

    d = ncls.join(sp, on = 'file').join(mc, on = 'file')
    d['ratio'] = d['#c'] / d['#v']
    d['lmc_ratio'] = d['log2(#m)'] / d['#v']

    d.time /= d.time.max()
    d.mem /= d.mem.max()

    ytrue = d['time'].to_numpy()
    xs = d['ratio'].to_numpy()
    ypred = [pred(mr, x) for x in xs]
    tmp = EF(ytrue, ypred)
    print(f"   k = 3 (#c / #v): {tmp}")

    ytrue = d['time'].to_numpy()
    xs = d['lmc_ratio'].to_numpy()
    ypred = [pred(mlmc, x) for x in xs]
    tmp = EF(ytrue, ypred)
    print(f"   k = 3 (r): {tmp}")

