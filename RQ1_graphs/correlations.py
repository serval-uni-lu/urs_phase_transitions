import pandas as pd
import scipy.stats as stats

for dataset in ["c5", "c8", "c15"]:
    for s in ["d4", "ug3", "mcTw", "sharpSAT", "spur"]:
        datasets = None

        for i in range(3, 9):
            cnf =  pd.read_csv(f"csv/{dataset}/r75k3q0.{i}{dataset}_cls.csv", skipinitialspace = True, index_col = 'file')
            mod =  pd.read_csv(f"csv/{dataset}/r75k3q0.{i}{dataset}_mod.csv", skipinitialspace = True, index_col = 'file')

            data = cnf

            sampler = pd.read_csv(f"csv/{dataset}/r75k3q0.{i}{dataset}_{s}.csv", skipinitialspace = True, index_col = 'file')
            sampler = sampler.join(data, on = 'file').join(mod, on = 'file')
            sampler = sampler[sampler.state == 'done']

            if datasets is None:
                datasets = sampler
            else:
                datasets = pd.concat([datasets, sampler])

        print(f"sampler: {s} (dataset: {dataset})")
        corr, pv = stats.kendalltau(datasets.time, datasets.q)
        print(f"   {corr} ({pv})")
