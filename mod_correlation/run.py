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

    l = [ "F1: " + str(metrics.f1_score(Y, ype))
    , "ROC AUC: " + str(metrics.roc_auc_score(Y, ype))
    , "precision: " + str(metrics.precision_score(Y, ype))
    ]

    for i in l:
        print(i)

def get_v(data):
    X = np.abs(((data['#c-u']) / (data['#v'] - data['#vu'] - data['#vf'] + 1)))
    Y = data.time
    return X, Y

samplers = ["unigen3", "spur", "d4", "sharpSAT", "mcTw"]
res = {}

f_id = 0
for sampler in samplers:
    res[sampler] = {}
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
    mod = pd.read_csv("data/mod_smp.csv", skipinitialspace = True, index_col = 'file')
    cost = pd.read_csv("./data/split_cost_s75.csv", skipinitialspace = True, index_col = 'file')
    tw = pd.read_csv("data/tw.csv", skipinitialspace = True, index_col = 'file')

    data = cnf.join(d4, on = 'file')
    data = data.join(subfm, on = 'file')
    data = data.join(mod, on = 'file')
    data = data.join(cost, on = 'file')
    data = data.join(tw, on = 'file')
    # data = data.join(subfmk3, on = 'file', rsuffix = '_k3')
    # data = data.join(mc, on = 'file')

    data.dropna(inplace = True)

    data['#rv'] = data['#v'] - data['#vu'] - data['#vf']
    data['#rc'] = data['#c-u']
    data['r'] = data['#c-u'] / (data['#v'] - data['#vu'] - data['#vf'] + 1)

    # data = data[data['#rv'] < 10000]
    # mpl.hist(data['#rv'], bins = 1000)
    # mpl.show()

    # nbv = 1225
    # tol = 100
    # data = data[data['#rv'] <= nbv + tol]
    # data = data[data['#rv'] >= nbv - tol]
    # data = data[data.r >= 2.5]
    # data = data[data.r <= 3.5]

    done = data[data['state'] == 'done']
    mem = data[data['state'] == 'mem']
    time = data[data['state'] == 'timeout']
    nb = len(data)
    nb_fails = len(data[data.state != 'done'])
    nb_mem = len(mem)
    nb_time = len(time)
    nb_done = len(done)


    print(f"{sampler}: nb {nb}, done {nb_done}, fails {nb_fails}, mem {nb_mem}, time {nb_time}")
    print("(time, #rv): " + str(stats.kendalltau(done.time, done['#rv'], nan_policy = 'raise')))
    print("(time, mod): " + str(stats.kendalltau(done.time, done['q'], nan_policy = 'raise')))
    print("(time, mod / (1 + #rv)): " + str(stats.kendalltau(done['time'], done['q'] / (1 + done['#rv']), nan_policy = 'raise')))
    print("(time, tw): " + str(stats.kendalltau(done['time'], done['tw'], nan_policy = 'raise')))
    print("(time, tw / (1 + #rv)): " + str(stats.kendalltau(done['time'], done['tw'] / (1 + done['#rv']), nan_policy = 'raise')))
    print("(time, 1 / (1 + #rv)): " + str(stats.kendalltau(done['time'], 1 / (1 + done['#rv']), nan_policy = 'raise')))
    # print("(time, comms): " + str(stats.kendalltau(done.time, done['comms'], nan_policy = 'raise')))
    # print("(time, split cost): " + str(stats.kendalltau(done.time, done['cost'], nan_policy = 'raise')))
    print("(#rv, mod): " + str(stats.kendalltau(data['#rv'], data['q'], nan_policy = 'raise')))
    # print("(#rv, comms): " + str(stats.kendalltau(done['#rv'], done['comms'], nan_policy = 'raise')))
    # print("(time, mod / (1 + #rc)): " + str(stats.kendalltau(done['time'], done['q'] / (1 + done['#rc']), nan_policy = 'raise')))
    # print(stats.kendalltau(done['q'], done['cost'], nan_policy = 'raise'))
    # print(stats.spearmanr(done.time, done['q'], nan_policy = 'raise'))
    # print("--")
    # print(stats.pointbiserialr(data.state == 'done', data['q']))
    # print(stats.pointbiserialr(data.state == 'done', data['cost']))
    # print(stats.pointbiserialr(done.q > 0.7, done.time))

    # fm = done.filter(regex = '(FeatureModels|FMEasy)', axis = 0)
    # blasted = done.filter(regex = 'Blasted_Real', axis = 0)
    # v3 = done.filter(regex = '(V3|V7|V15)', axis = 0)

    # print(stats.kendalltau(fm.time, fm['q'], nan_policy = 'raise'))
    # print(stats.kendalltau(blasted.time, blasted['q'], nan_policy = 'raise'))
    # print(stats.kendalltau(v3.time, v3['q'], nan_policy = 'raise'))


    print("")

# print(pd.DataFrame(res))
