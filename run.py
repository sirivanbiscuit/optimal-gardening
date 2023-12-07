"""
The primary run script for the logic execution.
"""
from bauhaus.utils import count_solutions
from nnf import config
from scripts.constraints import *
from scripts.setup import INIT
from scripts.propositions import GardenPlot

# Setup logic
config.sat_backend = "kissat" # fast SAT-solver

# Outputs the solution into something more readable.
# - If grid is set to True, it will print a coloured grid
#   showing the various plants at the positions over time.
# - Otherwise, it will simply make a list of all propositions
#   set to T in the model, excluding rocks.
# This isn't commented well, since it has nothing to do with
# the actual logic funtions. It is just a visualizer tool.
def solution_out(sol:dict, grid:bool):
    trues = {}
    for true in sol:
        if sol[true]:
            interv = str(true)[1:3].replace(":","")
            if interv in trues: trues[interv].append(true)
            else: trues[interv] = [true]
    # Print out a visual grid-solution
    if grid:
        ALIV = '\033[92m'
        NORM = '\033[0m'
        g_l = len(INIT)+2
        pd = GardenPlot.PLANT_VIS.copy()
        for interv in range(len(trues)):
            print(f"\nt{interv}:")
            g_grid = [["*" for _ in range(g_l)] for _ in range(g_l)]
            for t in trues[f'{interv}']:
                for char in pd:
                    if t.__class__.__name__==pd[char]: 
                        g_grid[t.x][t.y] = char
            for t_a in trues[f'{interv}']:
                if t_a.__class__.__name__=="Alive":
                    g_grid[t_a.x][t_a.y] = ALIV+g_grid[t_a.x][t_a.y]+NORM
            for row in g_grid:
                row_str = "\t"
                for cell in row: row_str+=f"{cell} "
                print(row_str)
    # Print out a raw list of true props
    else:
        print("- shows all propositions that are true")
        print("- if a proposition isn't here, it's false")
        print("- all coords are form (row, col)")
        for interv in range(len(trues)):
            print(f"\nt{interv}:")
            true_strs = []
            for t in trues[f'{interv}']:
                if t.__class__.__name__!="Rock": 
                    true_strs.append(str(t)[4:].strip())
            true_strs.sort()
            for string in true_strs:
                print(f"\t{string}")
    print('\n')


# RUN SCRIPT
if __name__ == "__main__":
    # Asks the user if they want a grid output or a list output
    grid = input("Show grid? (y/n) ")=='y'
    # Optimal garden seeks solutions that reach some state in
    # which all plants will remain alive forever
    opt = input("Find optimal gardens? (y/n) ")=='y'
    # IMMEDIATE optimal gardens have all plants live forever right
    # from the beginning. That is, t0=t1=t2... and so on.
    opt_f = input("Immediate optimization? (y/n) ")=='y' if opt else False
    # The below code prints a status report followed by
    # the user's desired output. This may make from seconds to
    # minutes depending on how "empty" the user makes their initial 
    # state in setup.py (since there is one solution for every 
    # POSSIBLE garden within the bounds of the initial state).
    print("\nBuilding garden theory...")
    T = build_garden_theory(opt, opt_f)
    print("Compiling...")
    T = T.compile()
    print("Calculating satisfiability...")
    satisfied = T.satisfiable()
    solution_count = count_solutions(T)
    print(f"\nSatisfiable: {satisfied}")
    print(f"Solutions: {solution_count}\n")
    adj = "fully " if opt_f else ""
    if opt: print(f"You can grow {solution_count} {adj}optimal gardens from the given configuration.\n")
    # If at least one solution is found, print out one
    if satisfied:
        sol = T.solve()
        print("\nMODEL DATA:")
        solution_out(sol, grid)
        # The user may look at other solutions to an initial state without
        # having to re-run the entire progam. This shouldn't take long as 
        # the theory has already been compiled above:
        if solution_count>1:
            while input("There is more than one solution to this garden. Find another? (y/n) ")=='y':
                new_sol = sol
                print("Collecting model data...")
                while sol==new_sol: new_sol = T.solve()
                print("\nMODEL DATA:")
                solution_out(new_sol, grid)
        print("\n")     
    # This will only show up if the user tries to find an "optimal garden"
    # within a configuration that can't have any. If the user only wants to
    # look at a completed garden's evolution over time, there will be 1 solution.   
    else:
        print("(no solutions to display)\n\n")