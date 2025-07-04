# URS and #SAT phase transitions

This repository gives supplementary material related to the paper.
The main goal for the experimental results and raw data to be available
to users as well as additional graphs related to the paper.

## RQk

The `RQk_graphs` folders contain python scripts used to create the
graphs from the data in the respective `csv` folders as well as the Figures (some of which
are available in the paper).

### CSV

The `csv` folders contain our raw experimental results.
File names such as `r50k3_mcTw.csv` indicate that the file contains the
runtimes (in seconds) and the memory usage (in kilobytes) of the `mcTw` model counter
which was executed on the `r50k3` dataset which in this case is a `k-CNF` dataset
with `k = 3` and 50 variables.

File names such as `r50k3_mc.csv` contain the number of solutions of each formulae if we
managed to compute them with `D4`.

File names such as `r50k3_cls.csv` contain the number of variable (`#v`), the number of clauses (`#c`)
and the total number of literals (`#l`) of each formula.

File names such as `r50k3_mod.csv` contain a lower bound to the modularity `Q` computed
with the label propagation algorithm shown in [1].

The RQ1 dataset named `r75k3q0.3c15` indicates that the dataset was generated with the community
attachement (CA) model. Moreover, the dataset is composed of `k-CNF` formulae with 75 variables and `k = 3`.
The target modularity given to the CA model was `q = 0.3` and the number of communities was set to `c = 15`.

Each `csv` file contains a `file` column which can be used to join the files together depending on the needs.

## Community

The `community` folder contains the community attachment model
, by Jesús Giráldez-Cru and Jordi Levy,
which generates random k-CNF formulas with a community structure.
(https://www.ijcai.org/Abstract/15/277)

The folder also contains `rsat` which generates random k-CNF formulas
by using the classical model.

## SMP

The `smp` folder contains the program used to simplify a DIMACS file
and the program used to compute some structural metrics on a DIMACS file.

The simplifier program is build as follows:

```
cd smp
make clean
make
```

The container version can be build with `make singularity`
To install the dependencies on Ubuntu for the native version,
please run `sudo apt-get -y install libz3-dev make g++`.

Usage:
```
./smp input.cnf > output.cnf
```

The measuring program is build as follows:
```
cd smp
make clean
make STATS=1
```

Usage:
```
./smp input.cnf
```

The output is in csv format with the following columns:
`file, #v, #vu, #vf, #c-u, #c2, #v2, #c3, #v3, #c4, #v4, #c5, #v5`

`file` is the file name

`#v` is the number of variables

`#vu` is the number of unit variables

`#vf` is the number of unconstrained variables

`#c-u` is the number of clauses minus the number of unit clauses

`#ck` is the number of clauses of size k

`#vk` is the number of variables in the subset of the formula containing only clauses of size k

An effective way of running it on multiple files:
``find "dataset" -name "*.cnf" | parallel -n 1 -P 16 ./smp``
Note that this requires GNU parallel.


## Singularity

The `singularity` folder contains the `.def` files used to create
the containers.

# LPA

The `lpa` folder contains the program used to approximate the true
modularity of a formula.

# Scripts

The `scripts` folder contains example scripts that were used during our
experiments.

# Datasets

The Plazar dataset is available at `https://github.com/diverse-project/samplingfm`.
The Soos dataset is available at `https://zenodo.org/records/10449477`.
The Lagniez dataset is available at `https://www.cril.univ-artois.fr/KC/benchmarks.html`
in the `CNF` section.
The Sunderman dataset is available at `https://github.com/SoftVarE-Group/feature-model-benchmark`
and was generated with the command `python scripts/extract_collection.py --variants last --versions last --output_format dimacs`.

## Dependencies

This repository relies heavily on `Singularity` (now called `Apptainer`).
It is therefore required to build the containers.
The commands still use the old name `singularity`, therefore, it may be
necessary to create an alias from for singularity.

# References

[1] Ansótegui, Carlos, Jesús Giráldez-Cru, and Jordi Levy. "The community structure of SAT formulas." International Conference on Theory and Applications of Satisfiability Testing. Berlin, Heidelberg: Springer Berlin Heidelberg, 2012.
