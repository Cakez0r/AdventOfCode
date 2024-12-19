#!/bin/bash

day=${1:-$(date +%-d)}

mkdir -p "$day"
cd "$day" || exit

touch sample.txt

touch main.py

ln -s ../../aoc.py aoc.py

code .