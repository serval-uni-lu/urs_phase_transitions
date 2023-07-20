# modularity

Implementation of the LPA and GFA algorithms presented in

```
@inproceedings{Anstegui2012TheCS,
  title={The Community Structure of SAT Formulas},
  author={Carlos Ans{\'o}tegui and Jes{\'u}s Gir{\'a}ldez-Cru and Jordi Levy},
  booktitle={SAT},
  year={2012}
}
```

Currently only the LPA algorithm is working and is thus the only one that us
usable without modifying the program.

## Compilation and usage

Dependencies are `g++` and `make`.

To compile, just type `make`
The command `make debug` is available to compile the debug version with
the address sanitizer. This will create an executable calles
`modularity_d`.

Program usage:
`modularity <path to cnf formula> <nb repeats>`

example outputs for the file `benchmarks/blasted_case200.cnf`:
```
LPA
i 5
q 0.116006
s 2
```
or for the same file:
```
LPA
i 3
q 0
s 1
```

The line starting with `i` indicates the number of iterations.
Line `q` indicates the lower bound for the modularity and line `s`
indicates the number of communities.

## Singularity

A singularity script is also available. To create the container simply run
`make singularity`. This will create a `modularity.sif` container
which may be used like the executable file above.
