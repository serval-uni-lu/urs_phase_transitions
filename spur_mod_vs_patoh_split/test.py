import pandas as pd
import numpy as np

import scipy.stats as stats

import matplotlib.pyplot as mpl

for sampler in ["spur"]:
    d4 =  pd.read_csv(f"data/{sampler}.csv", skipinitialspace = True, index_col = 'file')
    patoh =  pd.read_csv("data/split_cost_s75.csv", skipinitialspace = True, index_col = 'file')
    mod =  pd.read_csv("data/mod.csv", skipinitialspace = True, index_col = 'file')

    data = d4.join(mod, on = 'file')
    data = data.join(patoh, on = 'file')

    data.dropna(inplace = True)

    print(stats.kendalltau(data.time, data.cost, nan_policy = 'raise'))
    print(stats.kendalltau(data.time, data['q'], nan_policy = 'raise'))
