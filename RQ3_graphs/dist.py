import pandas as pd
import numpy as np

import matplotlib.pyplot as mpl

mpl.rcParams['text.usetex'] = True
# default: [6.4, 4.8]
mpl.rcParams["figure.figsize"] = (6.4,4.1)
mpl.rcParams['font.size'] = '14'
nb_fig = 1
dpi = 600

q_fig = nb_fig
mpl.figure(nb_fig)
nb_fig += 1

ncls = pd.read_csv(f"csv/ncls_smp_subsumtion.csv", skipinitialspace = True, index_col = 'file')
mc = pd.read_csv(f"csv/mc.csv", skipinitialspace = True, index_col = 'file')
# mod = pd.read_csv(f"csv/mod.csv", skipinitialspace = True, index_col = 'file')
d4 = pd.read_csv(f"csv/d4.csv", skipinitialspace = True, index_col = 'file')

mc = mc.join(ncls, on = 'file')
# mc = mc.join(mod, on = 'file')

# data = d4.join(ncls, on = 'file').join(mod, on = 'file')
data = d4.join(ncls, on = 'file')

mc['#vr'] = mc['#v'] - mc['#vf'] - mc['#vu']
mc = mc[mc['#vr'] != 0]
mc['ratio'] = mc['#c-u'] / (mc['#v'] - mc['#vf'] - mc['#vu'])
mc['lmc_ratio'] = mc['log2(#m)'] / mc['#v']

data['#vc'] = data['#v'] - data['#vu'] - data['#vf']
data = data[data['#vc'] > 0]
data['r'] = data['#c-u'] / (data['#v'] - data['#vu'] - data['#vf'])

done = data[data.state == 'done']
fail = data[data.state != 'done']
mem = data[data.state == 'mem']
time = data[data.state == 'timeout']

mpl.figure(nb_fig)
nb_fig += 1
mpl.hist(mc.ratio, bins = 40)

# mpl.grid()
mpl.xlabel("$|F| / |Var(F)|$")
mpl.ylabel("number of formulae")
mpl.minorticks_on()
# mpl.xlim(right = 7)
mpl.savefig(f"distributions/dist_cls.png", dpi = dpi, bbox_inches = 'tight')

mpl.figure(nb_fig)
nb_fig += 1
mpl.hist(mc.lmc_ratio, bins = 40)

# mpl.grid()
mpl.xlabel("$log_2(|R_F|) / |Var(F)|$")
mpl.ylabel("number of formulae")
mpl.minorticks_on()
# mpl.xlim(right = 7)
mpl.savefig(f"distributions/dist_lmc.png", dpi = dpi, bbox_inches = 'tight')

# mpl.figure(q_fig)
# # mpl.scatter(mc.ratio, mc['q'])
# mpl.scatter(done['#vc'], done.q, label = 'done', marker = '.')
# mpl.scatter(fail['#vc'], fail['q'], label = 'fail', marker = '.')
# 
# mpl.figure(q_fig)
# # mpl.grid()
# mpl.xlabel("$|Var(F)|$")
# mpl.ylabel("Q")
# mpl.minorticks_on()
# mpl.legend()
# # mpl.xlim(right = 7)
# mpl.savefig(f"distributions/mod.png", dpi = dpi, bbox_inches = 'tight')

