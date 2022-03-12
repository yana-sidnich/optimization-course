from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.moo.moead import MOEAD
from pymoo.factory import get_problem, get_visualization, get_reference_directions
from pymoo.visualization.scatter import Scatter
from pymoo.util.termination.no_termination import NoTermination
from pyrecorder.recorder import Recorder
from pyrecorder.writers.streamer import Streamer
from pyrecorder.writers.video import Video


import argparse
import numpy as np

PROBLEMS = {
    "zdt1"  : 2,
    "zdt2"  : 2,
    "zdt3"  : 2,
    "dtlz1" : 3,
    "dtlz2" : 3,
    "dtlz3" : 3,
}

EXPORTERS = {
    "screen" : lambda problem: Streamer(sleep=0.1),
    "recording" : lambda problem: Video("{}.mp4".format(problem))
}

COLORS = ["green", "blue", "red"]

REF_DIR_PARTITIONS = 12
PROBLEM_N_VAR = 5
SEED = 1

NSGA2_POP_SIZE = 100
NSGA3_POP_SIZE = 100
MOEAD_NEIGHBORS = 15
MOEAD_MATE_RATE = 0.7
NUM_GERNERATIONS = 60

def calculate(algorithms, problem, gens, exporter):

    # let the algorithm object never terminate and let the loop control it
    termination = NoTermination()

    # create an algorithm object that never terminates
    for algorithm in algorithms:
        algorithm["algorithm"].setup(problem, termination=termination)

    # fix the random seed manually
    np.random.seed(SEED)

    with Recorder(exporter) as rec:

    # for each algorithm object in the history

        # finally record the current visualization to the video
        for i in range(gens):
            sc = Scatter(title=("Gen %s" % i))
            sc.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
            for algorithm, color in zip(algorithms, COLORS):
                algorithm["algorithm"].next()
                sc.add(algorithm["algorithm"].pop.get("F"), color = color, label=algorithm["name"])
                sc.do()
            rec.record()


def nsga2_alg(pop_size=100):

    return NSGA2(pop_size=pop_size)

def nsga3_alg(ref_dirs, pop_size=100):
    return NSGA3(pop_size=pop_size , ref_dirs=ref_dirs)


def moead_alg(ref_dirs, n_neighbors=MOEAD_NEIGHBORS,prob_neighbor_mating=MOEAD_MATE_RATE):
    return MOEAD(
        ref_dirs,
        n_neighbors=n_neighbors,
        prob_neighbor_mating=prob_neighbor_mating,
    )
def create_ref_dir(dimentions=2, partitions=REF_DIR_PARTITIONS):
    return get_reference_directions("das-dennis", dimentions, n_partitions=partitions)


def main_logic(problem_name, exporter):
    ref_dir = create_ref_dir(PROBLEMS[problem_name])
    problem = get_problem(problem_name, n_var=PROBLEM_N_VAR)
    algs = [
        { "name" : "nsga2", "algorithm" : nsga2_alg()},
        { "name" : "nsga3", "algorithm" : nsga3_alg(ref_dir)},
        { "name" : "moead", "algorithm" : moead_alg(ref_dir)}
    ]
    calculate(algs, problem, NUM_GERNERATIONS, EXPORTERS[exporter](problem_name))
    results = [alg["algorithm"].result() for alg in algs]

    vis = get_visualization("scatter")
    for alg, color in zip(algs, COLORS):

        vis.add(alg["algorithm"].result().F, color=color, label=alg["name"])


    vis.show()

def main():
    parser = argparse.ArgumentParser(description="Options to show the differnt behaviors of oom algorithms")
    parser.add_argument("--exporter", choices=list(EXPORTERS.keys()), default=list(EXPORTERS.keys())[0])
    parser.add_argument("--problem", choices=list(PROBLEMS.keys()), required=True)
    args = parser.parse_args()
    main_logic(args.problem, args.exporter)


main()