
import numpy as np
from pyomo.environ import *
import matplotlib.pyplot as plt
from importlib import import_module
import argparse

# SOLVER = SolverFactory('glpk')

SOLVER = SolverFactory('ipopt', executable='ipopt')

PROBLEM_TYPE_ON_MAXIMIZE = {
    True : {
        "sense" : maximize,
        "constraint" : lambda func, eps : func >= eps
    },
    False : {
        "sense" : minimize,
        "constraint" : lambda func, eps : func <= eps
    }
}
# SOLVER = SolverFactory('glpk')

def create_model():

    model = ConcreteModel()
    variables = []
    for loc in range(PROBLEM.NUM_VARS):
        name = "var_{}".format(loc)
        if PROBLEM.NON_NEGATIVE_VARS:
            model.add_component(name, Var(within=NonNegativeReals))
        else:
            model.add_component(name, Var())

        variables.append(model.component(name))

    for loc, constraint in enumerate(PROBLEM.CONSTRAINTS):
        name = "C_{}".format(loc)
        model.add_component(name, Constraint(expr = constraint(variables)))

    model.f1 = Var()
    model.C_f1 = Constraint(expr = model.f1 == PROBLEM.F1(variables))
    
    model.f2 = Var()
    model.C_f2 = Constraint(expr = model.f2 == PROBLEM.F2(variables))

    return model

def calculate_min_max(model):
    def calcualte_objective(func1, func2):
        model.O_func = Objective(expr = func1, sense=maximize)
        SOLVER.solve(model)
        model.del_component(model.O_func)
        return value(func1), value(func2)
    
    values = {"f1" : {}, "f2" : {}}
    vals = calcualte_objective(model.f1, model.f2)
    values["f1"]["max"] = vals[0]
    values["f2"]["min"] = vals[1]

    vals = calcualte_objective(model.f2, model.f1)
    values["f2"]["max"] = vals[0]
    values["f1"]["min"] = vals[1]

    return values


def calcualte_pareto_front(model, maximize_func, constraint_func, num_epsilon, min_max):
    pareto_front = {
        "f1" : [],
        "f2" : [],
        "x1" : [],
        "x2" : [],
    }
    # calculating using augmented epsilon-constraint
    
    model.O_pareto = Objective(expr = model.component(maximize_func), sense=PROBLEM_TYPE_ON_MAXIMIZE[PROBLEM.MAXIMIZE_PROBLEM]["sense"])
    model.C_epsilon = Constraint(expr = PROBLEM_TYPE_ON_MAXIMIZE[PROBLEM.MAXIMIZE_PROBLEM]["constraint"](model.component(constraint_func), model.e))
    f_min = min_max[constraint_func]["min"]
    f_max = min_max[constraint_func]["max"]
    step = (f_max - f_min) / num_epsilon
    steps = list(np.arange(f_min, f_max, step)) + [f_max]

    for step in steps:
        model.e = step
        SOLVER.solve(model)
        pareto_front["f1"].append(value(model.f1))
        pareto_front["f2"].append(value(model.f2))
        pareto_front["x1"].append(value(model.var_0))
        pareto_front["x2"].append(value(model.var_1))

    model.del_component(model.O_pareto)
    model.del_component(model.C_epsilon)
    return pareto_front

def update_plot(ax, func, pareto):
    ax.plot(pareto["f1"], pareto["f2"], 'o-', c='r', label='Pareto optimal front by {}'.format(func))
    ax.legend(loc='best')
    ax.set_xlabel('Objective function F1')
    ax.set_ylabel('Objective function F2')
    ax.grid(True)

def create_pareto_front():
    model = create_model()
    min_max  = calculate_min_max(model)
    
    print(min_max)
    model.e = Param(initialize=0, mutable=True)
    # model.delta = Param(initialize=0.00001)
    # model.slack = Var(within=NonNegativeReals)
    num_iterations = PROBLEM.NUM_EPSILON_ITERATIONS if hasattr(PROBLEM, 'NUM_EPSILON_ITERATIONS') else 100

    pareto_front_by_f1 = calcualte_pareto_front(model, "f1", "f2", num_iterations, min_max)
    pareto_front_by_f2 = calcualte_pareto_front(model, "f2", "f1", num_iterations, min_max)
    print(pareto_front_by_f1)
    pf1 = pareto_front_by_f1
    for i in range(len(pf1["x1"])):
        print("x1 :{}, x2 : {}, f1 : {}, f2 : {}".format(pf1["x1"][i],pf1["x2"][i],pf1["f1"][i],pf1["f2"][i]))

    f1_min = min(min(pareto_front_by_f1["f1"]), min(pareto_front_by_f2["f1"]))
    f2_min = min(min(pareto_front_by_f1["f2"]), min(pareto_front_by_f2["f2"]))
    f1_max = max(max(pareto_front_by_f1["f1"]), max(pareto_front_by_f2["f1"]))
    f2_max = max(max(pareto_front_by_f1["f2"]), max(pareto_front_by_f2["f2"]))

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharex=True, figsize=(10,4))
    
    update_plot(ax1, "f1", pareto_front_by_f1)
    update_plot(ax2, "f2", pareto_front_by_f2)
   
    fig.tight_layout()
    plt.xlim([f1_min, f1_max])
    plt.ylim([f2_min, f2_max])
    plt.show()


parser = argparse.ArgumentParser()

parser.add_argument("--problem", default="problem1", help="Problem to use in order to calculate pareto front")
args = parser.parse_args()
PROBLEM = import_module(args.problem)

create_pareto_front()