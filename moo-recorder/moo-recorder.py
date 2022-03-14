from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.algorithm.multiobjective.spea2 import SPEA2
from jmetal.util.observer import VisualizerObserver


from jmetal.operator import SBXCrossover, PolynomialMutation
from jmetal.problem import ZDT1, DTLZ2, ZDT2
from jmetal.util.termination_criterion import StoppingByEvaluations

from jmetal.lab.visualization.plotting import Plot
from jmetal.util.solution import get_non_dominated_solutions
import argparse

POPULATION_SIZE = 100
OFFSPRING_POPULATION_SIZE = 100
MUTATION = lambda problem: PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20)

CROSSOVER = lambda : SBXCrossover(probability=1.0, distribution_index=20)
MAX_EVALUATIONS = 10000

PROBLEMS = {
    "zdt1" :ZDT1,
    "zdt2" :ZDT2,
    "dtlz2" :DTLZ2
}

def create_spea2(problem):
    return SPEA2(
        problem=problem,
        population_size=POPULATION_SIZE,
        offspring_population_size=OFFSPRING_POPULATION_SIZE,
        mutation=MUTATION(problem),
        crossover=CROSSOVER(),
        termination_criterion=StoppingByEvaluations(max_evaluations=MAX_EVALUATIONS)
    )

def create_nsgaii(problem):
    return NSGAII(
        problem=problem,
        population_size=POPULATION_SIZE,
        offspring_population_size=OFFSPRING_POPULATION_SIZE,
        mutation=MUTATION(problem),
        crossover=CROSSOVER(),
        termination_criterion=StoppingByEvaluations(max_evaluations=MAX_EVALUATIONS)
    )

def main_logic(problem_name):
    problem = PROBLEMS[problem_name]()
    algorithms = [ 
        create_spea2(problem),
        create_nsgaii(problem),
    ]
    labels = [
        'SPEA2-{}'.format(problem_name.upper()),
        'NSGAII-{}'.format(problem_name.upper())
    ]
    for algorithm in algorithms:
        algorithm.observable.register(observer=VisualizerObserver(reference_front=problem.reference_front))
        algorithm.run()

    front = [get_non_dominated_solutions(algorithm.get_result()) for algorithm in algorithms]
    plot_front = Plot(title='Pareto front approximation', axis_labels=['x', 'y' ])
    plot_front.plot(front, label=labels)


def main():
    parser = argparse.ArgumentParser(description="Options to show the differnt behaviors of oom algorithms")
    parser.add_argument("--problem", choices=list(PROBLEMS.keys()), required=True)
    args = parser.parse_args()
    main_logic(args.problem)


main()