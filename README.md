# Multi-Objective-Optimization

This repository contains multiple utilities and examples of different capabilities and types of multi objective optimization (MOO)

# Epsilon Constraint Utility

the folder **epsilon-constraint.py** contains a utility to solve MOO problems using epsilon constraint

## Dependecies

The utility uses the following dependencies

1. glpk - install using 'sudo apt-get install glpk-utils' (on Ubuntu).
2. pyomo - install using 'pip install pyomo'
3. matplotlib - install using 'pip install matplotlib'
4. numpy - install using 'pip install numpy'

If any other solver is required - for example a non-linear solver (like ipopt),
install the matching solver (https://ampl.com/products/solvers/open-source/ can be used as a reference), and control the solver configuration as indicated in the utility.

## Usage

Change folder to epsilon-constraint.
Run the utility using the following usage

> usage: epsilon-constraint.py [-h] [--problem PROBLEM]
>
> optional arguments:
> -h, --help show this help message and exit
> --problem PROBLEM Problem to use in order to calculate pareto front

the problem chosen symbolize a file on the ame folder which contains the configuration of the problem.
For Reference and explanation, use problem1.py.

> epsilon-constraint.py --problem problem1

## Output

The output of the problem is the pareto front of the chosen problem, solved using epsilon constraint.

![problem1 output example](/epsilon-constraint-example.png)

# Multi-Objective-Optimization Problem Recorder

the folder **epsilon-constraint.py** contains a utility to record the solving of solve MOO problems using multiple algorithms

## Dependecies

The utility uses the following dependencies

1. pymoo - install using 'pip install pymoo'
2. pyrecorder - install using 'pip install pyrecorder'

## Usage

Change folder to moo-recorder.
Run the utility using the following usage

> usage: moo-recorder.py [-h] [--exporter {screen,recording}] --problem
> {zdt1,zdt2,zdt3,dtlz1,dtlz2,dtlz3,BNH}
>
> Options to show the differnt behaviors of oom algorithms
>
> optional arguments:
> -h, --help show this help message and exit
> --exporter {screen,recording}
> --problem {zdt1,zdt2,zdt3,dtlz1,dtlz2,dtlz3,BNH}

the problem chosen symbolize a file on the ame folder which contains the configuration of the problem.
For Reference and explanation, use problem1.py.

> epsilon-constraint.py --problem problem1

## Output

The output of the problem is the pareto front of the chosen problem, solved using epsilon constraint.

![problem1 output example](/epsilon-constraint-example.png)
