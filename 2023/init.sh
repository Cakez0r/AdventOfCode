#!/bin/bash

day=$1

mkdir $day
cd $day
touch sample.txt
touch main.py
ln -s ../../aoc.py aoc.py
code .
