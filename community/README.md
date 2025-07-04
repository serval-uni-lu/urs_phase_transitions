# Basic usage

`rsat` is the classical k-CNF generation models and can be used
to generate k-CNF formulae.

`communityAttachment` is the Community Attachment model.
A helper script (which depends on `z3`) is provided with `gen.sh`.
The first lines of the script allow to set the maximum number of variables
`nv` and maximum number of clauses `nc` to be generated.
For each value between 1 and `nv` (resp. `nc`) the script will generate `nb`
k-CNF formulae with k = `k` and the modularity parameter `Q` given to the algorithm.
The `comm` variable sets the number of communities in the formulae.

The paper used `nv = 75`, `nc = 900` and `nb = 3`.
We used `k = 3` and varied `Q` between 0.3 and 0.8 with 0.1 increments.
We set `comm` to the values 5, 10 or 15.
The script depends on `z3` to automatically remove unsatisfiable formulae.
The script should be run inside another folder as the formulae are generated
inside the current folder.
It is therefore easier to move the `commAttach` executable inside the `PATH`.
We may then run
``
mkdir tmp
cd tmp
bash ../gen.sh "Q"
``
With `Q`, the desired modularity parameter.
