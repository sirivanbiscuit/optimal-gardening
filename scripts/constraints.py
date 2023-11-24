"""
Method class for building the set of contraints the garden
will use during logic execution.
"""
from bauhaus import Encoding, constraint
from encoding import ENC
from setup import G, INIT
from propositions import *

# Builds the default garden from setup.py
# - This will not automatically set all plants to alive, as the 
#   (h | ~k >> a) constraint will do that anyway.
def build_init_state():
    s = len(INIT)
    for x in range(s):
        for y in range(s):
            id = INIT[x][y] # full char map
            p_id = id.replace('f','') # fence ids ommitted
            plot_i, plot_u = G[0][x][y], G['u'][x][y]
            if len(p_id): ENC.add_constraint(plot_i.get_prop(p_id))
            if 'f' in id: ENC.add_constraint(plot_u)
            

def build_garden_theory() -> Encoding:
    # TODO: completed constraint list
    # Some constraints will be more difficult to
    # implement. They will be done at a later date.

    # MAKE SURE THAT INTERVAL STATES ARE MATERIALLY IMPLIED SOLELY
    # FROM THE PREVIOUS INTERVAL STATE (except for interval 0)
    
    dictloops = 0
    # Since the garden is square, we need to find the length of one side
    garden_size = len(G[0])
    
    #Find how many time points the garden exist for, subtracting the constant key
    garden_duration = len(G)-1

    # We don't need to evaluate the last time point as that is the end. 
    while dictloops < garden_duration-1:
        for x in garden[dictloops]:
            for y in garden[dictloops][x]:
                plot = garden[dictloops][x][y]
                # Check if there is a plant to the left 
                if x-1 >= 0:
                    ENC.add_constraint(plot.tomato & garden[dictloops][x-1][y].peppers >> garden[dictloops+1][x-1][y].helped)
                    ENC.add_constraint(plot.tomato & garden[dictloops][x-1][y].corn >> garden[dictloops+1][x-1][y].harmed) 
                    ENC.add_constraint(plot.beans & garden[dictloops][x-1][y].corn >> garden[dictloops+1][x-1][y].helped)
                    ENC.add_constraint(plot.beans & garden[dictloops][x-1][y].peppers >> garden[dictloops+1][x-1][y].harmed)
                # Check if there is a plant to the right 
                if x+1 <= garden_size:
                    ENC.add_constraint(plot.tomato & garden[dictloops][x+1][y].peppers >> garden[dictloops+1][x+1][y].helped)
                    ENC.add_constraint(plot.tomato & garden[dictloops][x+1][y].corn >> garden[dictloops+1][x+1][y].harmed) 
                    ENC.add_constraint(plot.beans & garden[dictloops][x+1][y].corn >> garden[dictloops+1][x+1][y].helped)
                    ENC.add_constraint(plot.beans & garden[dictloops][x+1][y].peppers >> garden[dictloops+1][x+1][y].harmed)
                # Check if there is a plant above
                if y-1 >= 0:
                    ENC.add_constraint(plot.corn & garden[dictloops][x][y-1].beans >> garden[dictloops+1][x][y-1].helped)
                    ENC.add_constraint(plot.corn & garden[dictloops][x][y-1].tomatoes >> garden[dictloops+1][x][y-1].harmed)
                    ENC.add_constraint(plot.peppers & garden[dictloops][x][y-1].tomatoes >> garden[dictloops+1][x][y-1].helped)
                    ENC.add_constraint(plot.peppers & garden[dictloops][x][y-1].beans >> garden[dictloops+1][x][y-1].harmed)
                # Check if there is a plant below
                if y+1 <= garden_size:
                    ENC.add_constraint(plot.corn & garden[dictloops][x][y+1].beans >> garden[dictloops+1][x][y+1].helped)
                    ENC.add_constraint(plot.corn & garden[dictloops][x][y+1].tomatoes >> garden[dictloops+1][x][y+1].harmed)
                    ENC.add_constraint(plot.peppers & garden[dictloops][x][y+1].tomatoes >> garden[dictloops+1][x][y+1].helped)
                    ENC.add_constraint(plot.peppers & garden[dictloops][x][y+1].beans >> garden[dictloops+1][x][y+1].harmed)
        dictloops += 1

    # TODO: make watering/fencing.
    # - Watered cell >> plant is alive
    # - Fenced cell >> plant is alive

    return ENC