#!/bin/bash

function run {
    fname="$1"

    r=$(z3 -dimacs "$fname")
    unsat=$(echo "$r" | grep -E "^s UNSATISFIABLE$")
    if [ -n "$unsat" ] ; then
        rm "$fname"
    fi
}
export -f run

find "$1" -name "*.cnf" | parallel -n 1 -P 4 run

