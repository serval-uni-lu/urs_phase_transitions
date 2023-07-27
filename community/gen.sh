#!/bin/bash

nv=75
nc=900
nb=3

k=3
Q="$1" #0.3 -> 0.8
comm=5

for ic in $(seq 1 "$nc") ; do
    for j in $(seq 1 "$nb") ; do
        fname="$ic.$j.cnf"
        commAttach -n $nv -m $ic -c $comm -Q $Q -k $k -o "$fname" -s "$RANDOM"

        r=$(z3 -dimacs "$fname")
        unsat=$(echo "$r" | grep -E "^s UNSATISFIABLE$")
        if [ -n "$unsat" ] ; then
            rm "$fname"
        fi
    done
done
