#!/bin/bash

function nb_cls_header {
    echo "file, #v, #c, #l"
}

function nb_cls {
    r=$(grep -E "^p cnf " "$1" | head -n 1)
    v=$(echo "$r" | cut -d ' ' -f 3)
    c=$(echo "$r" | cut -d ' ' -f 4)
    l=$(cat "$1" | grep -E "^ *-?[0-9]+" | sed 's/ 0$//g' | grep -E -o "\-?[0-9]+" | wc -l)
    echo "$1, $v, $c, $l"
}
export -f nb_cls

nb_cls_header > "$1_cls.csv"
find "$1" -name "*.cnf" | parallel -n 1 -P 4 nb_cls >> "$1_cls.csv"
