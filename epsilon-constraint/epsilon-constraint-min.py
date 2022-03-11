
from pydoc import describe
from numpy import min_scalar_type
from pyomo.environ import *
import matplotlib.pyplot as plt
from importlib import import_module
import argparse

SOLVER = SolverFactory('glpk')


def create_model(problem):
    prb = import_module(problem)

    model = ConcreteModel()
    variables = []
    for loc in range(prb.NUM_VARS):
        name = "var_{}".format(loc)
        if prb.NON_NEGATIVE_VARS:
            model.add_component(name, Var(within=NonNegativeReals))
        else:
            model.add_component(name, Var())

        variables.append(model.component(name))

    for loc, constraint in enumerate(prb.CONSTRAINTS):
        name = "C_{}".format(loc)
        model.add_component(name, Constraint(expr = constraint(variables)))

    model.f1 = Var()
    model.C_f1 =  Constraint(expr = model.f1 == prb.F1(variables))
    
    model.f2 = Var()
    model.C_f2 = Constraint(expr = model.f2 == prb.F2(variables))

    return model

# max f1 separately
# install glpk solver:  sudo apt-get install glpk-utils
def calculate_min_max(model, func):
    def calcualte_objective(func, sense):
        model.O_func = Objective(expr = func, sense=sense)
        SOLVER.solve(model)
        model.del_component(model.O_func)
        return value(func)
    return {
        "max" : calcualte_objective(func, sense=maximize),
        "min" : calcualte_objective(func, sense=minimize)
    }

def calcualte_pareto_front(model, maximize_func, constraint_func, num_epsilon, min_max):
    pareto_front = {
        "f1" : [],
        "f2" : []
    }
    
    model.O_pareto = Objective(expr = model.component(maximize_func) + model.delta * model.slack, sense=maximize)
    model.C_epsilon = Constraint(expr = model.component(constraint_func) - model.slack == model.e)

    # n = 10
    step = (min_max[constraint_func]["max"] - min_max[constraint_func]["min"]) / num_epsilon
    # steps = list(range(int(f2_min),int(f2_max),step or 1)) + [f2_max]
    i = min_max[constraint_func]["min"]
    # print(steps)
    # print(len(steps))
    while i <= min_max[constraint_func]["max"]:
        model.e = i
        SOLVER.solve(model)
        pareto_front["f1"].append(value(model.f1))
        pareto_front["f2"].append(value(model.f2))
        i += step

    model.del_component(model.O_pareto)
    model.del_component(model.C_epsilon)
    return pareto_front

def create_pareto_front(problem):
    model = create_model(problem)
    min_max  = {
        "f1" : calculate_min_max(model, model.f1),
        "f2" : calculate_min_max(model, model.f2)
    }
    print(min_max)
    print(min_max)
    # apply augmented $\epsilon$-Constraint
    # max   		f1 + delta*s
    # constraint 	f2 - s = e


    model.e = Param(initialize=0, mutable=True)
    model.delta = Param(initialize=0.00001)
    model.slack = Var(within=NonNegativeReals)
    pareto_front_by_f1 = calcualte_pareto_front(model, "f1", "f2", 100, min_max)
    pareto_front_by_f2 = calcualte_pareto_front(model, "f2", "f1", 100, min_max)
    print(len(pareto_front_by_f2["f2"]))

        # print(i, value(model.X1), value(model.X2), value(model.f1), value(model.slack), value(model.f2))

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharex=True, figsize=(10,4))

    f1_min = min(min(pareto_front_by_f1["f1"]), min(pareto_front_by_f2["f1"]))
    f2_min = min(min(pareto_front_by_f1["f2"]), min(pareto_front_by_f2["f2"]))
    f1_max = max(max(pareto_front_by_f1["f1"]), max(pareto_front_by_f2["f1"]))
    f2_max = max(max(pareto_front_by_f1["f2"]), max(pareto_front_by_f2["f2"]))
    print(f1_min)
    print(f1_max)
    print(f2_min)
    print(f2_max)
    print(list(zip(pareto_front_by_f2["f1"], pareto_front_by_f2["f2"])))
    print(list(zip(pareto_front_by_f1["f1"], pareto_front_by_f1["f2"])))
    plot_min = max(min_max["f1"]["min"], min_max["f2"]["min"])

    ax2.plot(pareto_front_by_f2["f1"], pareto_front_by_f2["f2"], 'o-', c='r', label='Pareto optimal front by f2')
    ax2.legend(loc='best')
    ax2.set_xlabel('Objective function F1')
    ax2.set_ylabel('Objective function F2')
    ax2.grid(True)
    fig.tight_layout()

    ax1.plot(pareto_front_by_f1["f1"], pareto_front_by_f1["f2"], 'o-', c='r', label='Pareto optimal front by f1')
    ax1.legend(loc='best')
    ax1.set_xlabel('Objective function F1')
    ax1.set_ylabel('Objective function F2')
    ax1.grid(True)
    fig.tight_layout()
    plt.xlim([f1_min, f1_max])
    plt.ylim([f2_min, f2_max])
    plt.show()


parser = argparse.ArgumentParser()

parser.add_argument("-p", "--problem", default="problem1", help="Problem to use in order to calculate pareto front")
args = parser.parse_args()
create_pareto_front(args.problem)