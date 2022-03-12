# Number of variables needed. those will be pased back to the constrainst as a list
NUM_VARS = 2
# Toggle to choose all variables as non negative.
# In case this is false - and some of them are non neagtive, a constraint is needed.
NON_NEGATIVE_VARS = True

MAXIMIZE_PROBLEM = False

# A list of constraints, each is a function (or a lambda) - which returns the constain as an algebric function
NUM_EPSILON_ITERATIONS = 100
def c1(x1,x2):
    return (x1 - 5)*(x1 - 5) + x2*x2 <= 25
def c2(x1,x2):
    return (x1 - 8) * (x1 - 8) + (x2 + 3)*(x2 + 3) >= 7.7

    
CONSTRAINTS = [
    lambda vars : vars[0] <= 5,
    lambda vars : vars[0] >= 0,
    lambda vars : vars[1] <= 3,
    lambda vars : vars[1] >= 0,
    lambda vars : c1(vars[0], vars[1]),
    lambda vars : c2(vars[0], vars[1]),
]

def f1(x1,x2):
    return 4 * x1*x1 + 4 * x2*x2
def f2(x1,x2):
    return (x1 - 5) * (x1 - 5) + (x2 - 5)*(x2 - 5)



# defenitions of the two functions to check
F1 = lambda vars : f1(vars[0], vars[1])
F2 = lambda vars : f2(vars[0], vars[1])