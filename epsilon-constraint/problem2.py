# Number of variables needed. those will be pased back to the constrainst as a list
NUM_VARS = 2
# Toggle to choose all variables as non negative.
# In case this is false - and some of them are non neagtive, a constraint is needed.
NON_NEGATIVE_VARS = True

MAXIMIZE_PROBLEM = True

# A list of constraints, each is a function (or a lambda) - which returns the constain as an algebric function
NUM_EPSILON_ITERATIONS = 100

CONSTRAINTS = [
    lambda vars : vars[0] <= 20,
    lambda vars : vars[1] <= 40,
    lambda vars : 5 * vars[0] + 4 * vars[1] <= 200,
]

# defenitions of the two functions to check
F1 = lambda vars : vars[0]
F2 = lambda vars : 3 * vars[0] + 4 * vars[1]