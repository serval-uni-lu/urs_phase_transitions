# Dependencies

To install the dependencies on Ubuntu please run (necessary for a native build):
``sudo apt install z3 libz3-dev libbsd-dev pkg-config make gcc g++``

# Build

For a native build, please install the dependencies and run `make`.

A container can be build with
``singularity build --fakeroot rsat.sif rsat.def``

or simply `make singularity`

# Generating k-CNF formulae

A basic help screen can be displayed with `./rsat.sif --help`

To generate formulae we can run
``
mkdir tmp
cd tmp
../rsat.sif --nvl 50 --nvh 55 --ncl 10 --nch 20 --k 3 --nf 2
``

This command will generate 3-CNF (`--k 3`) formulae
with between `--nvl 50` and `--nvh 55` variables (bound included)
and between `--ncl 10` and `--nch 20` clauses.
For each #clauses/#variables combination `--nf 2` formulae are generated.

If we want to generate formulae with `50` variables instead of a range
we can leave the `--nvh 55` argument out.
Similarily for the number of clauses and the `--nch 20` argument.

To generate only satisfiable formulae use the `--sat` option.
If present, the program will loop until the required number of formulae
have been generated and are satisfiable (note that this may be impossible or
highly unlikely).
