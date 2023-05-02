#!/bin/bash

function run {
  # arjun.sif "$1" "$1.arjun"
  # smp "$1" > "$1.smp"
  r=$(modularity "$1.smp")
  q=$(echo "$r" | grep -E "^q " | sed 's/^q //g')
  echo "$1, $q"
}

export -f run

echo "file, q"
head -n 503 cnf_list | tail -n 503 | parallel -n 1 -P 4 run
