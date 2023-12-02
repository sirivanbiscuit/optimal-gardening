"""
The primary run script for the logic execution.
"""
from bauhaus.utils import count_solutions, likelihood
from nnf import config
from scripts.constraints import *

# Setup logic
config.sat_backend = "kissat" # fast SAT-solver
    

# Run script
# This doesn't work yet.
if __name__ == "__main__":
    print(0)
    T = build_garden_theory()
    print(1)
    T = T.compile()
    print(2)
    print("\nSatisfiable: %s" % T.satisfiable())
    print(3)
    print("# Solutions: %d" % count_solutions(T))
    print(4)