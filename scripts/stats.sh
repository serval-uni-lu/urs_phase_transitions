#!/bin/bash

function run {
  stats "$1"
}

export -f run

echo "file, #v, #vu, #vf, #c-u, #c2, #v2, #c3, #v3, #c4, #v4, #c5, #v5"
head -n 503  cnf_list | tail -n 503 | parallel -n 1 -P 3 run
