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

# Output func
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


# Run script
if __name__ == "__main__":
    grid = input("Show grid? (y/n) ")=='y'
    opt = input("Find optimal gardens? (y/n) ")=='y'
    opt_f = input("Immeadiate optimization? (y/n) ")=='y' if opt else False
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
    if satisfied:
        sol = T.solve()
        print("\nMODEL DATA:")
        solution_out(sol, grid)
        if solution_count>1:
            while input("There is more than one solution to this garden. Find another? (y/n) ")=='y':
                new_sol = sol
                print("Collecting model data...")
                while sol==new_sol: new_sol = T.solve()
                print("\nMODEL DATA:")
                solution_out(new_sol, grid)
        print("\n")        
    else:
        print("(no solutions to display)\n\n")