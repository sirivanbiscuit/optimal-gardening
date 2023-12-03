"""
The primary run script for the logic execution.
"""
from bauhaus.utils import count_solutions
from nnf import config
from scripts.constraints import *
from scripts.setup import INIT
from scripts.propositions import GardenPlot
import sys

# Setup logic
config.sat_backend = "kissat" # fast SAT-solver

# Output func
# THE -graph ARG IS A W.I.P., use do no args for a list of props
def solution_out(sol: dict):
    trues = []
    for thing in sol:
        if sol[thing]: trues.append(str(thing))
    trues.sort()
    curr = None
    if len(sys.argv)>1: 
        if sys.argv[1]=="-grid":
            deconstr = {}
            pd = GardenPlot.PLANT_D.copy()
            for t in trues:
                if t[-1]==")":
                    if t[1]!=curr:
                        curr=t[1]
                        deconstr[curr]=[
                            ['' for _ in range(len(INIT)+2)] 
                            for _ in range(len(INIT)+2)
                            ]
                    else:
                        r,c = int(t[-5]),int(t[-2])
                        for p_id in pd:
                            if pd[p_id] in t: 
                                deconstr[curr][r][c] = p_id
                                break
            for key in deconstr:
                print(f"\n{key}:")
                for row in deconstr[key]:
                    print(f"\t{row}")     
            return
            
    for t in trues:
        if "Rock" not in t: 
            if t[1]!=curr: 
                curr=t[1]
                print()
                print(f"{curr}\t{t}")
            else:
                print(f"\t{t}")
    print()


# Run script
if __name__ == "__main__":
    print("\nBuilding garden theory...")
    T = build_garden_theory()
    print("Compiling...")
    T = T.compile()
    print("Calculating satisfiability...")
    satisfied = T.satisfiable()
    solution_count = count_solutions(T)
    print(f"\nSatisfiable: {satisfied}\nSolutions: {solution_count}\n")
    print("Collecting model data...")
    sol = T.solve()
    print("\nMODEL DATA:")
    print("- shows all propositions that are true")
    print("- if a proposition isn't here, it's false")
    print("- all coords are form (row, col)")
    solution_out(sol)