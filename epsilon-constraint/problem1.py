# Number of variables needed. those will be pased back to the constrainst as a list
NUM_VARS = 2
# The amount of times to iterate with differnt epsilons, with equal sized steps
NUM_EPSILON_ITERATIONS = 100
# Type of problem - Maximiztion or not
MAXIMIZE_PROBLEM = True
# Toggle to choose all variables as non negative.
# In case this is false - and some of them are non neagtive, a constraint is needed.
NON_NEGATIVE_VARS = True
# A list of constraints, each is a function (or a lambda) - which returns the constain as an algebric function

CONSTRAINTS = [
    lambda vars : vars[0] + 3 * vars[1] <= 3,
    lambda vars : vars[1] <= 6,
    lambda vars : 2 * vars[0] - vars[1] <= 6,
    lambda vars : 2 * vars[0] + vars[1] <= 10,
]

# definitions of the two functions to check
F1 = lambda vars : 3 * vars[0] + 3 * vars[1]
F2 = lambda vars : -1 * vars[0] + 4 * vars[1]