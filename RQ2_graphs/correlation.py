import pandas as pd
import numpy as np

import scipy.stats as stats

for i in range(3, 5):
    ncls = pd.read_csv(f"data/r50k{i}_cls.csv", skipinitialspace = True, index_col = 'file')
    mc = pd.read_csv(f"data/r50k{i}_mc.csv", skipinitialspace = True, index_col = 'file')
    mod = pd.read_csv(f"data/r50k{i}_mod.csv", skipinitialspace = True, index_col = 'file')

    mc = mc.join(ncls, on = 'file')
    mc = mc.join(mod, on = 'file')

    mc['ratio'] = mc['#c'] / mc['#v']
    mc['lmc_ratio'] = mc['log2(#m)'] / mc['#v']

    for s in ["d4", "ug3", "mcTw", "sharpSAT", "spur"]:
        sd = pd.read_csv(f"data/r50k{i}_{s}.csv", skipinitialspace = True, index_col = 'file')

        data = sd.join(mc, on = 'file')

        print(f"sampler: {s} (k = {i})")
        corr, pv = stats.kendalltau(data.time, data.q)
        print(f"   {corr} ({pv})")
