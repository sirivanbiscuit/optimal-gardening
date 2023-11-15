"""
The primary run script for the logic execution.SUS|
"""
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from nnf import config
from scripts.constraints import *

# Setup logic
config.sat_backend = "kissat" # fast SAT-solver
from scripts.setup import ENC # Encoder
    

# Run script
# This doesn't work yet.
if __name__ == "__main__":
    T = build_garden_theory()
    T = T.compile()
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())
    print("   Solution:")
    sol = T.solve()