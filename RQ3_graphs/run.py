import pandas as pd
import numpy as np

import sklearn.metrics as metrics
import scipy.stats as stats

import matplotlib.pyplot as mpl

mpl.rcParams['text.usetex'] = True

xlabel = "$|F| / |Var(F)|$"
ylabel = "time (s)"

dpi = 200

def score(title, Y, ype):
    print("## " + title)

    l = [ #"F1: " + str(metrics.f1_score(Y, ype))
    #, "ROC AUC: " + str(metrics.roc_auc_score(Y, ype))
    "precision: " + str(metrics.precision_score(Y, ype))
    ]

    for i in l:
        print(i)

def get_v(data):
    X = np.abs(((data['#c-u']) / (data['#v'] - data['#vu'] - data['#vf'] + 1)))
    Y = data.time
    return X, Y

total_time = dict()

f_id = 0
for sampler in ["unigen3", "spur", "d4", "sharpSAT", "mcTw"]:
    # nbcls_f = "./data/subfm_kge2_r3_subsum.csv"
    # nbcls_f = "data/subfm_kge3_r3_subsum.csv"
    nbcls_f = "data/subfm_k4.csv"
    nb_v_thresh = 150
    # nbcls_f = "data/subfm_k4.csv"
    # cnf =  pd.read_csv("data/ncls_smp.csv", skipinitialspace = True, index_col = 'file')
    cnf =  pd.read_csv("data/ncls_smp_subsumtion.csv", skipinitialspace = True, index_col = 'file')
    d4 =  pd.read_csv(f"data/{sampler}.csv", skipinitialspace = True, index_col = 'file')
    # mc =  pd.read_csv("data/mc.csv", skipinitialspace = True, index_col = 'file')
    subfm = pd.read_csv(nbcls_f, skipinitialspace = True, index_col = 'file')
    # subfmk3 = pd.read_csv("data/subfm_k3.csv", skipinitialspace = True, index_col = 'file')
    cost = pd.read_csv("./data/split_cost_s200.csv", skipinitialspace = True, index_col = 'file')

    data = cnf.join(d4, on = 'file')
    data = data.join(subfm, on = 'file')
    # data = data.join(subfmk3, on = 'file', rsuffix = '_k3')
    # data = data.join(mc, on = 'file')
    data = data.join(cost, on = 'file')


    if sampler not in total_time:
        total_time[sampler] = 0
    # data.dropna(inplace = True)


    done = data[data['state'] == 'done']
    mem = data[data['state'] == 'mem']
    time = data[data['state'] == 'timeout']
    nb = len(data)

    total_time[sampler] += done.time.sum()

    data['r'] = data['#c-u'] / (data['#v'] - data['#vu'] - data['#vf'] + 1)
    orig_r = data.r

    data['pred'] = data.nbv >= nb_v_thresh
    # data['pred'] = data.cost >= 5000
    data['bot'] = [False] * len(data)
    data['top'] = [True] * len(data)
    data['Y'] = data['state'] != 'done'

    tmp = data.dropna()

    score(sampler, tmp['Y'], tmp['pred'])
    # score("bot_" + sampler, tmp['Y'], tmp['bot'])
    score("top_" + sampler, tmp['Y'], tmp['top'])
    print("")

    print(f"nb data points: {len(data)}")

    X, Y = get_v(data)
    hard = data[data.pred]
    print(f"nb subfm hard: {len(hard)}")
    data = data[data['#c-u'] / (data['#v'] - data['#vu'] - data['#vf'] + 1) <= 10]
    X_r, Y_r = get_v(data)

    done_r = data[data['state'] == 'done']
    mem_r = data[data['state'] == 'mem']
    time_r = data[data['state'] == 'timeout']
    nb_r = len(data)

    hard_r = data[data.pred]


    Xd, Yd = get_v(done)
    Xm, Ym = get_v(mem)
    Xt, Yt = get_v(time)

    Xd_r, Yd_r = get_v(done_r)
    Xm_r, Ym_r = get_v(mem_r)
    Xt_r, Yt_r = get_v(time_r)

    Xh, Yh = get_v(hard)
    Xh_r, Yh_r = get_v(hard_r)


    f = mpl.figure(f_id)
    f_id += 1

    mpl.ylabel("Number of formulas")
    mpl.xlabel(xlabel)
    mpl.hist(orig_r, 100, color='grey', alpha = 0.5, label = "number of formulas")
    mpl.twinx()

    mpl.ylabel(ylabel)
    mpl.minorticks_on()
    # mpl.title("nb points: " + str(nb))
    mpl.scatter(Xd, Yd, marker = '.', label = 'success')
    mpl.scatter(Xm, Ym, marker = '.', label = 'out of memory')
    mpl.scatter(Xt, Yt, marker = '.', label = 'timeout')
    # mpl.scatter(Xh, Yh, linewidth=0.5, marker = 'x', color = 'black', label = 'subformula detected')
    mpl.legend()
    f.savefig(f"{sampler}_complete.png", dpi = dpi, bbox_inches = 'tight')

    # f = mpl.figure(f_id)
    # f_id += 1

    # mpl.ylabel("Number of formulas")
    # mpl.xlabel(xlabel)
    # mpl.hist(data.r, 100, color='grey', alpha = 0.5, label = "number of formulas")
    # mpl.twinx()

    # mpl.xlabel(xlabel)
    # mpl.ylabel(ylabel)
    # mpl.minorticks_on()
    # # mpl.title("nb points: " + str(nb_r))
    # mpl.scatter(Xd_r, Yd_r, marker = '.', label = 'success')
    # mpl.scatter(Xm_r, Ym_r, marker = '.', label = 'out of memory')
    # mpl.scatter(Xt_r, Yt_r, marker = '.', label = 'timeout')
    # mpl.scatter(Xh_r, Yh_r, linewidth = 0.5, marker = 'x', color = 'black', label = 'subformula detected')
    # mpl.legend()
    # f.savefig(f"{sampler}_r10.png", dpi = dpi, bbox_inches = 'tight')


for s in total_time:
    print(f"{s}:\t{total_time[s]}")
