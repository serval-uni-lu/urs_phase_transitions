#!/bin/bash

function run {
  # k = 3, ratio = 2
  r1=$(cnf_to_lp "$1" 3 2 | lp_solve)
  # k = 4, ratio = 3.5
  # r2=$(cnf_to_lp "$1" 4 3 | lp_solve)
  
  if [ "$r1" = "This problem is infeasible" ] ; then
    echo "$1, 0, 0, 0"
  else
    Z=$(echo "$r1" | grep -E "^Value of objective function: " | sed 's/^Value of objective function: //g')
    nbc=$(echo "$r1" | grep -E "^c" | grep -E " 1$" | wc -l)
    nbv=$(echo "$r1" | grep -E "^v" | grep -E " 1$" | wc -l)

    echo "$1, $Z, $nbv, $nbc"
  fi
}

export -f run

head -n 503 cnf_list | tail -n 503 | parallel -n 1 -P 4 run
