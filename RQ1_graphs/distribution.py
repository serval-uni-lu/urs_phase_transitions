import pandas as pd
import numpy as np

import matplotlib.pyplot as mpl

mpl.rcParams['text.usetex'] = True
mpl.rcParams["figure.figsize"] = (6.4,4)
mpl.rcParams['font.size'] = '14'
nb_fig = 1
dpi = 600


for dataset in ["c5", "c8", "c15"]:
    q_f_fig = nb_fig
    mpl.figure(nb_fig)
    nb_fig += 1

    q_rf_fig = nb_fig
    mpl.figure(nb_fig)
    nb_fig += 1

    for i in range(3, 9):
        ncls = pd.read_csv(f"csv/{dataset}/r75k3q0.{i}{dataset}_cls.csv", skipinitialspace = True, index_col = 'file')
        mc = pd.read_csv(f"csv/{dataset}/r75k3q0.{i}{dataset}_mc.csv", skipinitialspace = True, index_col = 'file')
        mod = pd.read_csv(f"csv/{dataset}/r75k3q0.{i}{dataset}_mod.csv", skipinitialspace = True, index_col = 'file')

        mc = mc.join(ncls, on = 'file')
        mc = mc.join(mod, on = 'file')

        mc['ratio'] = mc['#c'] / mc['#v']
        mc['lmc_ratio'] = mc['log2(#m)'] / mc['#v']


        mpl.figure(q_f_fig)
        mpl.scatter(mc.ratio, mc['q'], label = f'Q = 0.{i}', marker = '.')

        mpl.figure(q_rf_fig)
        mpl.scatter(mc.lmc_ratio, mc['q'], label = f'Q = 0.{i}', marker = '.')

    mpl.figure(q_f_fig)
    # mpl.grid()
    mpl.xlabel("$|F| / |Var(F)|$")
    mpl.ylabel("$\\tilde{Q}$")
    mpl.minorticks_on()
    mpl.legend()
    mpl.savefig(f"Figure 2 - modularity/mod_f_{dataset}.png", dpi = dpi, bbox_inches = 'tight')


    mpl.figure(q_rf_fig)
    # mpl.grid()
    mpl.xlabel("$log_2(|R_F|) / |Var(F)|$")
    mpl.ylabel("$\\tilde{Q}$")
    mpl.minorticks_on()
    mpl.legend()
    mpl.savefig(f"Figure 2 - modularity/mod_rf_{dataset}.png", dpi = dpi, bbox_inches = 'tight')

