# URS and #SAT phase transitions

## RQk

The `RQk_graphs` folders contain a python scripts used to create
graphs from the data in the respective `csv` folders.

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
make
```

Usage:
```
./smp input.cnf > output.cnf
```

The measuring program is build as follows:
```
cd smp
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


## Singularity

The `singularity` folder contains the `.def` files used to create
the containers.

The containers depend on the `wrapper` program which needs to be build
before building the containers.
Building the `D4` container is done as follows:
```
cd singularity
cd wrapper
make
cd ..

cd d4
make -j4
cd ..

singularity build --fakeroot "d4.sif" "d4.def"
```

The other containers are build similarily.
