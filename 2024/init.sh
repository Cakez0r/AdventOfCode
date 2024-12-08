#!/bin/bash

day=$(date +%-d)

mkdir $day
cd $day
touch sample.txt
touch main.py
ln -s ../../aoc.py aoc.py
code .
