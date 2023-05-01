#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as mpl
from scipy.stats import kendalltau as kt
import statistics
import math

data = {}
arr = pd.DataFrame()
for q in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
    cnf =  pd.read_csv(f"data/q{q}/cls.csv", skipinitialspace = True, index_col = 'file')
    spur = pd.read_csv(f"data/q{q}/spur.csv", skipinitialspace = True, index_col = 'file')

    tmp = cnf.join(spur, on = 'file')
    f = tmp[tmp.state != 'done']
    print(f"q{q} fails: {len(f)}")
    tmp = tmp[tmp.state == 'done']
    # tmp.time = np.log2(tmp.time)
    # tmp.mem = np.log2(tmp.mem)
    data[q] = tmp

    qarr = np.ones(len(tmp)) * q
    darr = tmp.time

    arr = pd.concat([arr, pd.DataFrame({'q': qarr, 'time': darr})])


print("KT: ")
print(kt(arr['q'], arr['time']))

############################################################

def gen_table(cnf, sampler):
    data = cnf.join(sampler, on = 'file')
    # data['ratio'] = np.abs(2 - (data['#c'] / data['#v']))
    data['ratio'] = (data['#c'] / data['#v'])

    # data.time /= data.time.max()
    # data.mem /= data.mem.max()
    return data

def get_arjun(sampler):
    data = sampler.filter(regex = ".arjun", axis = 0)
    ni = {}
    for i in data.index:
        ni[i] = i.replace(".arjun", "")

    return data.rename(index = ni)

def median_vals(data, field, ratio_f = 'ratio', resolution = 2):
    res = {}
    for f in data.index:
        r = data[ratio_f][f]
        r = round(r, resolution)
        res[r] = []

    for f in data.index:
        r = data[ratio_f][f]
        r = round(r, resolution)
        d = data[field][f]
        res[r].append(d)

    f = []
    for i in res:
        f.append({'ratio': i
                  , 'median': statistics.median(res[i]), 'mean': statistics.mean(res[i])
                  , 'min': min(res[i]), 'max': max(res[i])})

    return pd.DataFrame(f)

############################################################

mpl.figure(0)
mpl.grid()

f = 4
for q in data:
    df = data[q]
    df['ratio'] = df['#c'] / df['#v']

    mpl.figure(0)
    mpl.scatter(df.ratio, df.time, label = f'q = {q}', marker = '.')
    mpl.figure(1)
    mpl.scatter(df.ratio, df.mem, label = f'mem q{q}', marker = '.')

    med = median_vals(df, 'time')
    mpl.figure(2)
    mpl.scatter(med.ratio, med['mean'], label = f'mean time q{q}', marker = '.')

    med = median_vals(df, 'mem')
    mpl.figure(3)
    mpl.scatter(med.ratio, med['mean'], label = f'mean mem q{q}', marker = '.')

    mpl.figure(f)
    mpl.grid()
    mpl.scatter(df.ratio, df.time, label = f'time q{q}', marker = '.')
    mpl.xlabel("#c / #v")
    mpl.legend()
    mpl.savefig(f"time_q{q}.png", dpi = 600, bbox_inches = 'tight')

    mpl.figure(f + 1)
    mpl.grid()
    mpl.scatter(df.ratio, df.mem, label = f'mem q{q}', marker = '.')
    mpl.xlabel("#c / #v")
    mpl.legend()
    mpl.savefig(f"mem_q{q}.png", dpi = 600, bbox_inches = 'tight')

    f += 2
    mpl.figure(0)

mpl.figure(0)
mpl.xlabel("#c / #v")
mpl.ylabel("spur time (s)")
mpl.legend()
mpl.savefig("time.png", dpi = 600, bbox_inches = 'tight')


mpl.figure(1)
mpl.xlabel("#c / #v")
mpl.legend()
mpl.savefig("mem.png", dpi = 600, bbox_inches = 'tight')

mpl.figure(2)
mpl.xlabel("#c / #v")
mpl.legend()
mpl.savefig("mean_time.png", dpi = 600, bbox_inches = 'tight')

mpl.figure(3)
mpl.xlabel("#c / #v")
mpl.legend()
mpl.savefig("mean_mem.png", dpi = 600, bbox_inches = 'tight')
