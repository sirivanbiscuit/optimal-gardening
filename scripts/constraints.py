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
# - However, it does assert that all cells at the initial state 
#   are neither helped nore hurt. This is probably the correct
#   course of action for now.
def build_init_state():
    s = len(INIT)
    for x in range(s):
        for y in range(s):
            id = INIT[x][y] # full char map
            p_id = id.replace('f','') # fence ids ommitted
            plot_i, plot_u = G[0][x][y], G['u'][x][y]
            if len(p_id): ENC.add_constraint(plot_i.get_prop(p_id))
            if 'f' in id: ENC.add_constraint(plot_u)
            ENC.add_constraint(~plot_i.get_prop('h'))
            ENC.add_constraint(~plot_i.get_prop('k'))
            

# All our general constraints go here
# Make sure you import G as the garden grid from setup.py
def build_garden_theory() -> Encoding:
    
    dictloops = 0
    garden_size = len(G[0])
    # Find how many time points the garden exist for, 
    # subtracting the constant key
    garden_duration = len(G)-1
    # We don't need to evaluate the last time point as that is the end. 
    while dictloops < garden_duration-1:
        for x in G[dictloops]:
            for y in G[dictloops][x]:
                plot = G[dictloops][x][y]
                # Check if there is a plant to the left 
                if x-1 >= 0:
                    targ_plot_i = G[dictloops][x-1][y]
                    targ_plot_next = G[dictloops+1][x-1][y]
                    ENC.add_constraint(plot.tomato & targ_plot_i.peppers >> 
                                       targ_plot_next.helped)
                    ENC.add_constraint(plot.tomato & targ_plot_i.corn >> 
                                       targ_plot_next.harmed) 
                    ENC.add_constraint(plot.beans & targ_plot_i.corn >> 
                                       targ_plot_next.helped)
                    ENC.add_constraint(plot.beans & targ_plot_i.peppers >> 
                                       targ_plot_next.harmed)
                # Check if there is a plant to the right 
                if x+1 <= garden_size:
                    targ_plot_i = G[dictloops][x+1][y]
                    targ_plot_next = G[dictloops+1][x+1][y]
                    ENC.add_constraint(plot.tomato & targ_plot_i.peppers >> 
                                       targ_plot_next.helped)
                    ENC.add_constraint(plot.tomato & targ_plot_i.corn >> 
                                       targ_plot_next.helped) 
                    ENC.add_constraint(plot.beans & targ_plot_i.corn >> 
                                       targ_plot_next.helped)
                    ENC.add_constraint(plot.beans & targ_plot_i.peppers >> 
                                       targ_plot_next.harmed)
                # Check if there is a plant above
                if y-1 >= 0:
                    targ_plot_i = G[dictloops][x][y-1]
                    targ_plot_next = G[dictloops+1][x][y-1]
                    ENC.add_constraint(plot.corn & targ_plot_i.beans >> 
                                       targ_plot_next.helped)
                    ENC.add_constraint(plot.corn & targ_plot_i.tomatoes >> 
                                       targ_plot_next.harmed)
                    ENC.add_constraint(plot.peppers & targ_plot_i.tomatoes >> 
                                       targ_plot_next.helped)
                    ENC.add_constraint(plot.peppers & targ_plot_i.beans >> 
                                       targ_plot_next.harmed)
                # Check if there is a plant below
                if y+1 <= garden_size:
                    targ_plot_i = G[dictloops][x][y+1]
                    targ_plot_next = G[dictloops+1][x][y+1]
                    ENC.add_constraint(plot.corn & targ_plot_i.beans >> 
                                       targ_plot_next.helped)
                    ENC.add_constraint(plot.corn & targ_plot_i.tomatoes >> 
                                       targ_plot_next.harmed)
                    ENC.add_constraint(plot.peppers & targ_plot_i.tomatoes >> 
                                       targ_plot_next.helped)
                    ENC.add_constraint(plot.peppers & targ_plot_i.beans >> 
                                       targ_plot_next.harmed)
        dictloops += 1




    return ENC