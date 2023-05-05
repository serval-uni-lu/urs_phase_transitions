import pandas as pd
import matplotlib.pyplot as mpl

mpl.rcParams['text.usetex'] = True

fig_dim = (4, 4)
fig_nb = 1

xlabel = "$|F| / |Var(F)|$"
ylabel = "time (s)"

# for s in ["spur"]:
for dataset in ["c5", "c8", "c15"]:
    for s in ["d4", "ug3", "mcTw", "sharpSAT", "spur"]:
        f = mpl.figure(fig_nb)
        fig_nb += 1
        mpl.xlabel(xlabel)
        mpl.ylabel(ylabel)

        for i in range(3, 9):
            cnf =  pd.read_csv(f"{dataset}/r75k3q0.{i}{dataset}_cls.csv", skipinitialspace = True, index_col = 'file')
            # mc =  pd.read_csv(f"{dataset}/r75k3q0.{i}{dataset}_mc.csv", skipinitialspace = True, index_col = 'file')

            data = cnf
            # data = data.join(mc, on = 'file')
            data['ratio'] = data['#c'] / data['#v']
            # data['ratio_lmc'] = data['log2(#m)'] / data['#v']

            sampler =  pd.read_csv(f"{dataset}/r75k3q0.{i}{dataset}_{s}.csv", skipinitialspace = True, index_col = 'file')
            sampler = sampler.join(data, on = 'file')
            sampler = sampler[sampler.state == 'done']

            # print(sampler)

            mpl.scatter(sampler['ratio'], sampler['time'], label = f'Q = {i / 10}', marker = '.')

        mpl.legend()
        mpl.grid()
        mpl.minorticks_on()
        mpl.savefig(f"gr/{s}_{dataset}.png", dpi = 200, bbox_inches = 'tight')
