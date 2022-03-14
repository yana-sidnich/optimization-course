from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.moo.moead import MOEAD
from pymoo.factory import get_problem, get_visualization, get_reference_directions
from pymoo.visualization.scatter import Scatter
from pymoo.util.termination.no_termination import NoTermination
from pyrecorder.recorder import Recorder
from pyrecorder.writers.streamer import Streamer
from pyrecorder.writers.video import Video
import numpy as np
import matplotlib.pyplot as plt
import argparse

PROBLEMS = {
    "zdt1"  : { "dimentions" : 2, "use_n_vars" : True},
    "zdt2"  : { "dimentions" : 2, "use_n_vars" : True},
    "zdt3"  : { "dimentions" : 2, "use_n_vars" : True},
    "dtlz1" : { "dimentions" : 3, "use_n_vars" : True},
    "dtlz2" : { "dimentions" : 3, "use_n_vars" : True},
    "dtlz3" : { "dimentions" : 3, "use_n_vars" : True},
    "BNH"   : { "dimentions" : 2, "use_n_vars" : False}
}

EXPORTERS = {
    "screen" : lambda problem: Streamer(sleep=0.1),
    "recording" : lambda problem: Video("{}.mp4".format(problem))
}


REF_DIR_PARTITIONS = 12
PROBLEM_N_VAR = 5
SEED = 1

NSGA2_POP_SIZE = 100
NSGA3_POP_SIZE = 100
MOEAD_NEIGHBORS = 15
MOEAD_MATE_RATE = 0.7
NUM_GERNERATIONS = 200

def calculate(algorithms, problem, gens, exporter, is_3d):

    # let the algorithm object never terminate and let the loop control it
    termination = NoTermination()

    # create an algorithm object that never terminates
    for algorithm in algorithms:
        algorithm["algorithm"].setup(problem, termination=termination)

    # fix the random seed manually
    np.random.seed(SEED)

    with Recorder(exporter) as rec:
        if is_3d:

            fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 12), subplot_kw=dict(projection='3d'))
            ax1.view_init(45,45)
            ax2.view_init(45,45)
        else:
            fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 12))

        # finally record the current visualization to the video
        for i in range(gens):
            for algorithm, ax in zip(algorithms, [ax1, ax2]):
                algorithm["algorithm"].next()
                front = algorithm["algorithm"].pop.get("F")
                ax.clear()
                if not is_3d:
                    ax.scatter(front[:, 0], front[:, 1], color = algorithm["color"], label=algorithm["name"])
                else:
                    ax.scatter(front[:, 0], front[:, 1], front[:, 2], color = algorithm["color"], label=algorithm["name"])

                # sc.do()
            rec.record(fig=fig)


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
    ref_dir = create_ref_dir(PROBLEMS[problem_name]["dimentions"])
    if PROBLEMS[problem_name]["use_n_vars"]:
        problem = get_problem(problem_name, n_var=PROBLEM_N_VAR)
    else:
        problem = get_problem(problem_name)
    algs = [
        { "name" : "nsga2", "algorithm" : nsga2_alg(), "color" : "green"},
        { "name" : "nsga3", "algorithm" : nsga3_alg(ref_dir), "color" : "blue"},
        # { "name" : "moead", "algorithm" : moead_alg(ref_dir), "color" : "red"}
    ]
    is_3d=PROBLEMS[problem_name]["dimentions"] == 3
    calculate(algs, problem, NUM_GERNERATIONS, EXPORTERS[exporter](problem_name), is_3d=is_3d)

  
    vis1 = get_visualization("scatter")
    vis2 = get_visualization("scatter")
    vis1.add(algs[0]["algorithm"].pop.get("F"), color=algs[0]["color"], label=algs[0]["name"])
    vis2.add(algs[1]["algorithm"].pop.get("F"), color=algs[1]["color"], label=algs[1]["name"])

    vis1.show()
    vis2.show()

def main():
    parser = argparse.ArgumentParser(description="Options to show the differnt behaviors of oom algorithms")
    parser.add_argument("--exporter", choices=list(EXPORTERS.keys()), default=list(EXPORTERS.keys())[0])
    parser.add_argument("--problem", choices=list(PROBLEMS.keys()), required=True)
    args = parser.parse_args()
    main_logic(args.problem, args.exporter)


main()