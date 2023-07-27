import pandas as pd
import numpy as np

import matplotlib.pyplot as mpl

mpl.rcParams['text.usetex'] = True
mpl.rcParams["figure.figsize"] = (6.4,4.1)
nb_fig = 1
dpi = 200

q_f_fig = nb_fig
mpl.figure(nb_fig)
nb_fig += 1

q_rf_fig = nb_fig
mpl.figure(nb_fig)
nb_fig += 1

for i in range(3, 5):
    ncls = pd.read_csv(f"data/r50k{i}_cls.csv", skipinitialspace = True, index_col = 'file')
    mc = pd.read_csv(f"data/r50k{i}_mc.csv", skipinitialspace = True, index_col = 'file')
    mod = pd.read_csv(f"data/r50k{i}_mod.csv", skipinitialspace = True, index_col = 'file')

    mc = mc.join(ncls, on = 'file')
    mc = mc.join(mod, on = 'file')

    mc['ratio'] = mc['#c'] / mc['#v']
    mc['lmc_ratio'] = mc['log2(#m)'] / mc['#v']

    mpl.figure(nb_fig)
    nb_fig += 1
    mpl.hist(mc.ratio, bins = 40, label = f'k = {i}')

    mpl.grid()
    mpl.xlabel("$|F| / |Var(F)|$")
    mpl.ylabel("number of formulas")
    mpl.minorticks_on()
    # mpl.xlim(right = 7)
    mpl.savefig(f"dist_cls_k{i}.png", dpi = dpi, bbox_inches = 'tight')

    mpl.figure(nb_fig)
    nb_fig += 1
    mpl.hist(mc.lmc_ratio, bins = 40, label = f'k = {i}')

    mpl.grid()
    mpl.xlabel("$log_2(|R_F|) / |Var(F)|$")
    mpl.ylabel("number of formulas")
    mpl.minorticks_on()
    # mpl.xlim(right = 7)
    mpl.savefig(f"dist_lmc_k{i}.png", dpi = dpi, bbox_inches = 'tight')

    mpl.figure(q_f_fig)
    mpl.scatter(mc.ratio, mc['q'], label = f'k = {i}', marker = '.')

    mpl.figure(q_rf_fig)
    mpl.scatter(mc.lmc_ratio, mc['q'], label = f'k = {i}', marker = '.')

mpl.figure(q_f_fig)
mpl.grid()
mpl.xlabel("$|F| / |Var(F)|$")
mpl.ylabel("Q")
mpl.minorticks_on()
mpl.legend()
# mpl.xlim(right = 7)
mpl.savefig(f"mod_f.png", dpi = dpi, bbox_inches = 'tight')


mpl.figure(q_rf_fig)
mpl.grid()
mpl.xlabel("$log_2(|R_F|) / |Var(F)|$")
mpl.ylabel("Q")
mpl.minorticks_on()
mpl.legend()
# mpl.xlim(right = 7)
mpl.savefig(f"mod_rf.png", dpi = dpi, bbox_inches = 'tight')

