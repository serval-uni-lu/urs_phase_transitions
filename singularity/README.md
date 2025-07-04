# Build and basic usage

## D4

To build the container run the following command in this folder.
``singularity build --fakeroot d4.sif d4.def``

You may then use the following command to compute the model count of a formula `t.cnf`:
``./d4.sif -mc t.cnf``

The following command will compute the model count and output the d-DNNF to a file
called `res.nnf`:
``./d4.sif -dDNNF t.cnf -out=res.nnf``

The `wrapper` program will add a line to the standard error with the following content:
``/d4/d4 -dDNNF t.cnf -out=res.nnf, done, 575410, 0.021675``
where `575410` is the amount of memory used in kilobytes and `0.021675` is the execution
time in seconds. `done` indicates that the program exited successfully (i.e.,
no errors, timeouts or out of memory errors).

## MCtW

The container for MCtW is build with:
``singularity build --fakeroot mctw.sif mctw.def``

Running MCtW is done as follows:
``./mctw.sif < t.cnf``

Similarily to D4, the wrapper generates the following line:
``/mctw/swats, done, 6225, 0.0108641``

## sharpSAT

sharpSAT is build with the following command:
``singularity build --fakeroot sharpSAT.sif sharpSAT.def``

Basic usage:
``./sharpSAT.sif t.cnf``

The resulting wrapper line:
``/sharpSAT t.cnf, done, 30404, 0.0113189``

## SPUR

Build command:
``singularity build --fakeroot spur.sif spur.def``

Basic usage:
``./spur.sif -s <number of samples> -out <output file> -cnf t.cnf``

The `<output file>` will contain the samples.

The resulting wrapper line:
``/spur/build/Release/spur -s 10 -out res -cnf t.cnf, done, 27385, 0.00986107``

## UniGen3

Build command:
``singularity build --fakeroot unigen3.sif unigen3.def``

Basic usage:
``./unigen3.sif --seed <random seed> --samples <number of samples> t.cnf``

The resulting wrapper line:
``/unigen/build/unigen --seed 18110 --samples 10 t.cnf, done, 11464, 0.0568049``

## Makefile

A basic makefile is provided with the above build commands.

# Basic usage

The tools can then simply be run with a bash script as follows:

``
function run {
    tool.sif "$1" &> "$1.tool"
}
export -f run

find "dataset" -name "*.cnf" | parallel -n 1 -P 4 run
``

The csv data can then be recovered with:

``
function run {
    r=$(cat "$1.tool" | grep -E "^/")
    echo "$1, $r"
}
expor -f run

echo "file, command, state, memory, time" > tool.csv
find "dataset" -name "*.cnf" | parallel -n 1 -P 4 run >> tool.csv
``
