# Multi-Objective-Optimization

This repository contains multiple utilities and examples of different capabilities and types of multi objective optimization (MOO)

# Epsilon Constraint

the folder **epsilon-constraint.py** contains an example of utility to solve moo problems using epsilon constraint

## Dependecies

The utility uses the following dependencies

1. glpk - install using 'sudo apt-get install glpk-utils' (on Ubuntu).
2. pyomo - install using 'pip install pyomo'
3. matplotlib - install using 'pip install matplotlib'
4. numpy - install using 'pip install numpy'

## Usage

> usage: epsilon-constraint.py [-h] [--problem PROBLEM]
>
> optional arguments:
> -h, --help show this help message and exit
> --problem PROBLEM Problem to use in order to calculate pareto front

the problem chosen symbolize a file on the ame folder which contains the configuration of the problem.
For Example, use problem1.py
