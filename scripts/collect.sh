#!/bin/bash

function urs_header {
    echo "file, state, mem, time"
}

function spur {
    r=$(grep -E "^/spur" "$1.sp" | sed 's#/spur/build/Release/spur -s 1000 -no-sample-write -cnf ##g')
    echo "$r"
}
export -f spur

function d4 {
    r=$(grep -E "^/d4" "$1.d4" | sed 's#/d4 .*-dDNNF -out=##g;s#.d4.nnf##g')
    echo "$r"
}
export -f d4

function ug3 {
    r=$(grep -E "^/unigen/build/unigen" "$1.ug3" | sed 's#/unigen/build/unigen --samples 1000 ##g')
    echo "$r"
}
export -f ug3

function sharpSAT {
    r=$(grep -E "^/sharpSAT " "$1.sharpSAT" | sed 's#/sharpSAT ##g')
    echo "$r"
}
export -f sharpSAT

function mcTw {
    r=$(grep -E "^/mcTw/swats" "$1.mcTw" | sed 's#^/mcTw/swats##g')
    echo "$1$r"
}
export -f mcTw

function addmc {
    r=$(grep -E "^/addmc" "$1.addmc" | sed 's#^/addmc##g')
    echo "$1$r"
}
export -f addmc

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

function mc_header {
    echo "file, #m, log2(#m)"
}

function mc {
    r=$(grep -E "^s [0-9]+" "$1.d4" | sed 's#^s ##g')
    lmc=$(python -c "import math
print(math.log2($r))")
    echo "$1, $r, $lmc"
}
export -f mc

urs_header > "$1_spur.csv"
find "$1" -name "*.cnf" | parallel -n 1 -P 4 spur >> "$1_spur.csv"
 
urs_header > "$1_d4.csv"
find "$1" -name "*.cnf" | parallel -n 1 -P 4 d4 >> "$1_d4.csv"

urs_header > "$1_ug3.csv"
find "$1" -name "*.cnf" | parallel -n 1 -P 4 ug3 >> "$1_ug3.csv"

urs_header > "$1_sharpSAT.csv"
find "$1" -name "*.cnf" | parallel -n 1 -P 4 sharpSAT >> "$1_sharpSAT.csv"
# 
urs_header > "$1_mcTw.csv"
find "$1" -name "*.cnf" | parallel -n 1 -P 4 mcTw >> "$1_mcTw.csv"
#  
# # urs_header > "$1_ADDMC.csv"
# # find "$1" -name "*.cnf" | parallel -n 1 -P 4 addmc >> "$1_ADDMC.csv"
# 
nb_cls_header > "$1_cls.csv"
find "$1" -name "*.cnf" | parallel -n 1 -P 4 nb_cls >> "$1_cls.csv"
 
mc_header > "$1_mc.csv"
find "$1" -name "*.cnf" | parallel -n 1 -P 4 mc >> "$1_mc.csv"
