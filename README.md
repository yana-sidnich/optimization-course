# Multi-Objective-Optimization

This repository contains multiple utilities and examples of different capabilities and types of multi objective optimization (MOO)

# Epsilon Constraint Utility

the folder **epsilon-constraint** contains a utility to solve MOO problems using epsilon constraint

## Dependencies

The utility uses the following dependencies

1. glpk - install using 'sudo apt-get install glpk-utils' (on Ubuntu).
2. pyomo - install using 'pip install pyomo'
3. matplotlib - install using 'pip install matplotlib'
4. numpy - install using 'pip install numpy'
5. importlib - install using 'pip install importlib'

If any other solver is required - for example a non-linear solver (like ipopt),
install the matching solver (https://ampl.com/products/solvers/open-source/ can be used as a reference), and control the solver configuration as indicated in the utility.

## Usage

Change folder to epsilon-constraint.
Run the utility using the following usage

> usage: epsilon-constraint.py [-h] [--problem PROBLEM]
> optional arguments:
> -h, --help show this help message and exit
> --problem PROBLEM Problem to use in order to calculate pareto front

the problem chosen symbolize a file on the same folder which contains the configuration of the problem.
For Reference and explanation, use problem1.py.

> epsilon-constraint.py --problem problem1

## Output

The output of the problem is the Pareto front of the chosen problem, solved using epsilon constraint.

![epsilon-constraint output example](/epsilon-constraint-example.png)

# Multi-Objective-Optimization NSGA Comparison Recorder

the folder **nsga-comparer** contains a utility to record the solving of MOO problems using nsga2, nsga3 algorithms

## Dependencies

The utility uses the following dependencies

1. pymoo - install using 'pip install pymoo'
2. pyrecorder - install using 'pip install pyrecorder'
3. argparse - install using 'pip install argparse'
4. numpy - install using 'pip install numpy'
5. matplotlib - install using 'pip install matplotlib'

## Usage

Change folder to nsga-comparer.
Run the utility using the following usage

> usage: nsga-comparer.py [-h] [--exporter {screen,recording}] --problem
> {zdt1,zdt2,zdt3,dtlz1,dtlz2,dtlz3,BNH}
> Options to show the different behaviors of moo algorithms
> optional arguments:
> -h, --help show this help message and exit
> --exporter {screen,recording}
> --problem {zdt1,zdt2,zdt3,dtlz1,dtlz2,dtlz3,BNH}

For example:

> nsga-comparer.py --problem zdt1

Using Exporter screen (default) - cause a video of the Pareto front to pop to the screen.
Using Exporter recording - cause a video of the Pareto front to be exported to an mp4 file with the problem name.
The problem can be controlled using the 'problem' parameter.

## Output

Depending on the parameters - a video to the screen or the mp4 file, which comapres the nsga2, and nsga3 algorithms.
nsga2 in green
nsga3 in blue
At the end - two plots (consecutively) to compare the final result will be shown, for example:
![nsga2 output example](/nsga-comparer-nsga2-example.png)
![nsga3 output example](/nsga-comparer-nsga3-example.png)

# Multi-Objective-Optimization Recorder

the folder **moo-recorder** contains a utility to view the solving of MOO problems using nsga2, spea2 algorithms

## Dependencies

The utility uses the following dependencies

1. jmetalpy - install using 'pip install jmetalpy'
2. argparse - install using 'pip install argparse'

## Usage

Change folder to moo-recorder.
Run the utility using the following usage

> usage: moo-recorder.py [-h] --problem {zdt1,zdt2,dtlz2}
>
> Options to show the differnt behaviors of oom algorithms
>
> optional arguments:
> -h, --help show this help message and exit
> --problem {zdt1,zdt2,dtlz2}

For example:

> moo-recorder.py --problem zdt2

A video of the Pareto front steps will pop to the screen.

The problem can be controlled using the 'problem' parameter.

## Output

Two consecutive videos (first spea2, second nsga2) to the screen
At the end - two plots to compare the final result will be shown, for example:
![moo-recorder output example](/moo-recorder-example.png)
