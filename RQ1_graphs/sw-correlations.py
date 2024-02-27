import pandas as pd
import numpy as np
import scipy.stats as stats

import matplotlib.pyplot as mpl

mpl.rcParams['text.usetex'] = True
mpl.rcParams["figure.figsize"] = (6.4,4.1)
mpl.rcParams['font.size'] = '14'
nb_fig = 1
dpi = 600

def correlations(data, idx, xkey, ykey, f, epsilon = 0.3):
    vals = set(data[idx].to_numpy())

    xs = []
    ys = []
    pv = []

    for nc in vals:
        mask = [data[idx][i] > nc - epsilon and data[idx][i] < nc + epsilon for i in data[idx].keys()]
        tmp = data[mask]

        X = tmp[xkey].to_numpy()
        Y = tmp[ykey].to_numpy()

        xs.append(nc)

        corr, pval = f(X, Y)

        ys.append(corr)
        pv.append(pval)

    return (xs, ys, pv)


# for dataset in ["c5", "c8", "c15"]:
for dataset in ["c5"]:
    for s in ["d4", "ug3", "mcTw", "sharpSAT", "spur"]:
        datasets = None

        for i in range(3, 9):
            cnf =  pd.read_csv(f"{dataset}/r75k3q0.{i}{dataset}_cls.csv", skipinitialspace = True, index_col = 'file')
            # mc =  pd.read_csv(f"{dataset}/r75k3q0.{i}{dataset}_mc.csv", skipinitialspace = True, index_col = 'file')
            mod =  pd.read_csv(f"{dataset}/r75k3q0.{i}{dataset}_mod.csv", skipinitialspace = True, index_col = 'file')

            data = cnf
            # data = data.join(mc, on = 'file')
            data['ratio'] = data['#c'] / data['#v']
            # data['ratio_lmc'] = data['log2(#m)'] / data['#v']

            sampler = pd.read_csv(f"{dataset}/r75k3q0.{i}{dataset}_{s}.csv", skipinitialspace = True, index_col = 'file')
            sampler = sampler.join(data, on = 'file').join(mod, on = 'file')
            sampler = sampler[sampler.state == 'done']

            if datasets is None:
                datasets = sampler
            else:
                datasets = pd.concat([datasets, sampler])

        print(f"sampler: {s} (dataset: {dataset})")
        corr, pv = stats.kendalltau(datasets.time, datasets.q)
        print(f"   {corr} ({pv})")

        xs, ys, pv = correlations(datasets, 'ratio', 'q', 'time', stats.kendalltau)
        tmp = pd.DataFrame({'x': xs, 'corr': ys, 'pval': pv})

        pv1 = tmp[tmp.pval >= 0.01]
        pvb = tmp[tmp.pval >= 0.05]

        fig = mpl.figure(nb_fig)
        nb_fig += 1
        ax = fig.add_axes([0, 0, 1, 1])
        ax.scatter(tmp['x'], tmp['corr'], label = 'p-value $<$ 0.01', marker = '.')
        ax.scatter(pv1['x'], pv1['corr'], label = 'p-value $\ge$ 0.01', marker = '.')
        ax.scatter(pvb['x'], pvb['corr'], label = 'p-value $\ge$ 0.05', marker = '.')
        # mpl.scatter(xs, ys, label = 'correlations', marker = '.')
        # mpl.scatter(xs, pv, label = 'p-values', marker = '.')

        # mpl.ylim(top = 0.05)

        ticks = np.arange(-0.9, 0.45, step = 0.2)
        mticks = np.arange(-0.9, 0.45, step = 0.1)
        # print(ticks)
        # print(mticks)
        ax.set_yticks(ticks)
        ax.set_yticks(mticks, minor = True)

        ax.set_xlabel("$|F| / |Var(F)|$")
        ax.set_ylabel("Kendall's $\\tau$")
        ax.legend()
        # ax.grid(alpha = 0.3, which = 'minor')
        # mpl.minorticks_on()
        fig.savefig(f"corr_{s}_{dataset}.png", dpi = dpi, bbox_inches = 'tight')


