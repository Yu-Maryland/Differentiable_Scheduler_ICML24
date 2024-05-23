#!/bin/bash

graph="$5"
cmd_parse="python parse_graph_w_attr.py $3 $6 $graph > ./schedulenet_w_attr.py"
time eval "$cmd_parse"

if [ -f ./schedulenet_w_attr.py ]; then
    python ./schedulenet_w_attr.py "$graph" "$1" "$2" "$3" "$4"
else
    echo "schedulenet_w_attr.py was not generated successfully."
fi

