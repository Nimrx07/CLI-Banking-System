#!/bin/bash

for DAY in {0..6}; do
    echo "===== Day $DAY ====="
    bash daily.sh $DAY
done
