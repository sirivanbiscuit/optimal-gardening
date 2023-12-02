"""
Method class for building the set of contraints the garden
will use during logic execution.
"""
from bauhaus import Encoding, Or
from scripts.encoding import ENC
from scripts.setup import G, INIT, garden_len
from scripts.propositions import *

# Builds the default garden from setup.py
# - This will not automatically set all plants to alive, as the 
#   (h | ~k >> a) constraint will do that anyway.
# - However, it does assert that all cells at the initial state 
#   are neither helped nor hurt. This is probably the correct
#   course of action for now.
def build_init_state():
    # Inner plants
    s = len(INIT)
    for x in range(s):
        for y in range(s):
            id = INIT[x][y] # full char map
            p_id = id.replace('f','') # fence ids ommitted
            plot_i = G[0][x+1][y+1]
            if len(p_id): ENC.add_constraint(plot_i.get_prop(p_id))
    
    # All cells (incl. rocks)
    for interval in G:
        if interval != 'u':
            for row in G[interval]:
                for plot in row:
                    ENC.add_constraint(~plot.get_prop('h'))
                    ENC.add_constraint(~plot.get_prop('k'))
                    if plot.x==0 or plot.y==0 or plot.x>s or plot.y>s:
                        ENC.add_constraint(plot.get_prop('R'))
            

# All our general constraints go here
# Make sure you import G as the garden grid from setup.py
def build_garden_theory() -> Encoding:
    
    # PLANT RELATIONSHIPS
    # NEEDS INVERSE IMPLICATIONS SO THERE'S ONLY ONE SOLUTION
    dictloops = 0
    garden_size = garden_len
    # Find how many time points the garden exist for, 
    # subtracting the constant key
    garden_duration = len(G)-1
    # We don't need to evaluate the last time point as that is the end. 
    while dictloops < garden_duration-1:
        for x in range(1,garden_size):
            for y in range(1,garden_size):
                plot = G[dictloops][x][y]
                # Constrains the plant to the left
                targ_plot_i = G[dictloops][x-1][y]
                targ_plot_next = G[dictloops+1][x-1][y]
                ENC.add_constraint((plot.tomatoes & targ_plot_i.peppers) >> 
                                   targ_plot_next.helped)
                ENC.add_constraint((plot.tomatoes& targ_plot_i.corn) >> 
                                       targ_plot_next.harmed) 
                ENC.add_constraint((plot.beans & targ_plot_i.corn) >> 
                                       targ_plot_next.helped)
                ENC.add_constraint((plot.beans & targ_plot_i.peppers) >> 
                                       targ_plot_next.harmed)
                ENC.add_constraint((plot.pineTree & ~targ_plot_i.pineTree) >> 
                                       targ_plot_next.harmed)
                #Constrains the plant to the left
                targ_plot_i = G[dictloops][x+1][y]
                targ_plot_next = G[dictloops+1][x+1][y]
                ENC.add_constraint((plot.tomatoes & targ_plot_i.peppers) >> 
                                       targ_plot_next.helped)
                ENC.add_constraint((plot.tomatoes & targ_plot_i.corn) >> 
                                       targ_plot_next.helped) 
                ENC.add_constraint((plot.beans & targ_plot_i.corn) >> 
                                       targ_plot_next.helped)
                ENC.add_constraint((plot.beans & targ_plot_i.peppers) >> 
                                       targ_plot_next.harmed)
                ENC.add_constraint((plot.pineTree & ~targ_plot_i.pineTree) >> 
                                       targ_plot_next.harmed)
                #Constrains the plant above
                targ_plot_i = G[dictloops][x][y-1]
                targ_plot_next = G[dictloops+1][x][y-1]
                ENC.add_constraint((plot.corn & targ_plot_i.beans) >> 
                                       targ_plot_next.helped)
                ENC.add_constraint((plot.corn & targ_plot_i.tomatoes) >> 
                                       targ_plot_next.harmed)
                ENC.add_constraint((plot.peppers & targ_plot_i.tomatoes) >> 
                                       targ_plot_next.helped)
                ENC.add_constraint((plot.peppers & targ_plot_i.beans) >> 
                                       targ_plot_next.harmed)
                ENC.add_constraint((plot.pineTree & ~targ_plot_i.pineTree) >> 
                                       targ_plot_next.harmed)
                # Constrains the plant below
                targ_plot_i = G[dictloops][x][y+1]
                targ_plot_next = G[dictloops+1][x][y+1]
                ENC.add_constraint((plot.corn & targ_plot_i.beans) >> 
                                       targ_plot_next.helped)
                ENC.add_constraint((plot.corn & targ_plot_i.tomatoes) >> 
                                       targ_plot_next.harmed)
                ENC.add_constraint((plot.peppers & targ_plot_i.tomatoes) >> 
                                       targ_plot_next.helped)
                ENC.add_constraint((plot.peppers & targ_plot_i.beans) >> 
                                       targ_plot_next.harmed)
                ENC.add_constraint((plot.pineTree & ~targ_plot_i.pineTree) >> 
                                       targ_plot_next.harmed)
        dictloops += 1
    
    # PLANT RELATIONSHIPS; INVERSE IMPLICATIONS SO THERE'S ONLY ONE SOLUTION
    # This code applies constraints to the next version of this plot, not to a target plot. 
    dictloops = 0
    garden_size = garden_len
    # Find how many time points the garden exist for, 
    # subtracting the constant key
    garden_duration = len(G)-1
    # We don't need to evaluate the last time point as that is the end. 
    while dictloops < garden_duration-1:
        for x in range(1,garden_size-1):
            for y in range(1,garden_size-1):
                above_plot_i = G[dictloops][x][y+1]
                below_plot_i = G[dictloops][x][y-1]
                left_plot_i = G[dictloops][x-1][y]
                right_plot_i = G[dictloops][x+1][y]
                plot_next = G[dictloops+1][x][y]
                #Inverse constraints for helped
                ENC.add_constraint(((plot.corn & ~left_plot_i.beans & ~right_plot_i.beans) &
                                   (plot.peppers & ~left_plot_i.tomatoes & ~right_plot_i.tomatoes) &
                                   (plot.tomatoes & ~above_plot_i.peppers & ~below_plot_i.peppers) &
                                   (plot.beans & ~above_plot_i.corn & ~below_plot_i.corn))
                                   >> 
                                       ~plot_next.helped)
                #Inverse Constraints for hindered
                ENC.add_constraint(((plot.corn & ~left_plot_i.tomatoes & ~right_plot_i.tomatoes) &
                                   (plot.peppers & ~left_plot_i.beans & ~right_plot_i.beans) &
                                   (plot.tomatoes & ~above_plot_i.peppers & ~below_plot_i.peppers) &
                                   (plot.beans & ~above_plot_i.corn & ~below_plot_i.corn) &
                                   ~(right_plot_i.pineTree | left_plot_i.pineTree | above_plot_i.pineTree | below_plot_i.pineTree))
                                   >> 
                                       ~plot_next.harmed)
        dictloops+=1

    # SINGLE INTERVAL CONSTRAINTS
    for interval in G:
        if interval != "u":
            for row in G[interval]:
                for plot in row:
                    # One plant per cell
                    ENC.add_constraint(
                        plot.corn >> (~plot.beans & ~plot.tomatoes & ~plot.peppers & ~plot.pineTree & ~plot.rock))
                    ENC.add_constraint(
                        plot.beans >> (~plot.corn & ~plot.tomatoes & ~plot.peppers & ~plot.pineTree & ~plot.rock))
                    ENC.add_constraint(
                        plot.tomatoes >> (~plot.corn & ~plot.beans & ~plot.peppers & ~plot.pineTree & ~plot.rock))
                    ENC.add_constraint(
                        plot.peppers >> (~plot.corn & ~plot.beans & ~plot.tomatoes & ~plot.pineTree & ~plot.rock))
                    ENC.add_constraint(
                        plot.pineTree >> (~plot.corn & ~plot.beans & ~plot.tomatoes & ~plot.peppers & ~plot.rock))
                    
                    # Rock makes everything false
                    ENC.add_constraint(
                        plot.rock >> (~plot.corn & ~plot.beans & ~plot.tomatoes & ~plot.peppers & ~plot.pineTree
                        & ~plot.helped & ~plot.harmed & plot.alive))
                    
                    # helped or not hurt impl. alive
                    ENC.add_constraint((plot.helped | ~plot.harmed) >> plot.alive)
                    ENC.add_constraint(plot.alive >> (plot.helped | ~plot.harmed))
    
    
    # PLANT SPREADING
    for t in range(len(G)-2):
        for x in range(1,len(G[t])-1):
            for y in range(1,len(G[t][x])-1):
                
                #array of spreading value in order
                # for example corn: (beans, peppers, tomatoes, dead)
                above = G[t][x][y+1]
                below = G[t][x][y-1]
                left = G[t][x][x-1]
                right = G[t][x][x+1]
                next = G[t+1][x][y]
                plot = G[t][x][y]

                #Looks at plant in all directions around, if at least one it becomes that plant (in order of priority)
                #Corn
                ENC.add_constraint((plot.corn & ~plot.alive & (above.beans | right.beans | left.beans | below.beans)) >> (next.beans & next.alive))

                ENC.add_constraint((plot.corn & ~plot.alive & (~above.beans & ~right.beans & ~left.beans & ~below.beans) & \
                                    (above.peppers | right.peppers | left.peppers | below.peppers)) >> (next.peppers & next.alive))
                
                ENC.add_constraint((plot.corn & ~plot.alive & (~above.beans & ~right.beans & ~left.beans & ~below.beans) & \
                                   (~above.peppers & ~right.peppers & ~left.peppers & ~below.peppers) & \
                                    (above.tomatoes | left.tomatoes | right.tomatoes | below.tomatoes)) >> (next.tomatoes & next.alive))
                
                ENC.add_constraint((plot.corn & ~plot.alive & (~above.beans & ~right.beans & ~left.beans & ~below.beans) & \
                                   (~above.peppers & ~right.peppers & ~left.peppers & ~below.peppers) & \
                                    (~above.tomatoes & ~left.tomatoes & ~right.tomatoes & ~below.tomatoes)) >> (next.corn & ~next.alive))
                
                #Beans
                ENC.add_constraint((plot.beans & ~plot.alive & (above.corn | right.corn | left.corn | below.corn)) >> (next.corn & next.alive))

                ENC.add_constraint((plot.beans & ~plot.alive & (~above.corn & ~right.corn & ~left.corn & ~below.corn) & \
                                   (above.tomatoes | left.tomatoes | right.tomatoes | below.tomatoes)) >> (next.tomatoes & next.alive))
                
                ENC.add_constraint((plot.beans & ~plot.alive & (~above.corn & ~right.corn & ~left.corn & ~below.corn) & \
                                   (~above.tomatoes & ~left.tomatoes & ~right.tomatoes & ~below.tomatoes) & \
                                    (above.peppers | right.peppers | left.peppers | below.peppers)) >> (next.peppers & next.alive))
                
                ENC.add_constraint((plot.beans & ~plot.alive & (~above.corn & ~right.corn & ~left.corn & ~below.corn) & \
                                   (~above.tomatoes & ~left.tomatoes & ~right.tomatoes & ~below.tomatoes) & \
                                    (~above.peppers & ~right.peppers & ~left.peppers & ~below.peppers)) >> (next.beans & ~next.alive))
                
                #Peppers
                ENC.add_constraint((plot.peppers & ~plot.alive & (above.tomatoes | left.tomatoes | right.tomatoes | below.tomatoes)) >> (next.tomatoes & next.alive))

                ENC.add_constraint((plot.peppers & ~plot.alive & (~above.tomatoes & ~left.tomatoes & ~right.tomatoes & ~below.tomatoes) & \
                                   (above.corn | right.corn | left.corn | below.corn)) >> (next.corn & next.alive))
                
                ENC.add_constraint((plot.peppers & ~plot.alive & (~above.tomatoes & ~left.tomatoes & ~right.tomatoes & ~below.tomatoes) & \
                                    (~above.corn & ~right.corn & ~left.corn & ~below.corn) & \
                                    (above.beans | right.beans | left.beans | below.beans)) >> (next.beans & next.alive))
                
                ENC.add_constraint((plot.peppers & ~plot.alive & (~above.tomatoes & ~left.tomatoes & ~right.tomatoes & ~below.tomatoes) & \
                                    (~above.corn & ~right.corn & ~left.corn & ~below.corn) & \
                                    (~above.beans & ~right.beans & ~left.beans & ~below.beans)) >> (next.peppers & ~next.alive))
                
                #Tomatoes
                ENC.add_constraint((plot.tomatoes & ~plot.alive & (above.peppers | left.peppers | right.peppers | below.peppers)) >> (next.peppers & next.alive))

                ENC.add_constraint((plot.tomatoes & ~plot.alive & (~above.peppers & ~right.peppers & ~left.peppers & ~below.peppers) & \
                                   (above.beans | right.beans | left.beans | below.beans)) >> (next.beans & next.alive))
                
                ENC.add_constraint((plot.tomatoes & ~plot.alive & (~above.peppers & ~right.peppers & ~left.peppers & ~below.peppers) & \
                                   (~above.beans & ~right.beans & ~left.beans & ~below.beans) & \
                                    (above.corn | right.corn | left.corn | below.corn)) >> (next.corn & next.alive))
                
                ENC.add_constraint((plot.tomatoes & ~plot.alive & (~above.peppers & ~right.peppers & ~left.peppers & ~below.peppers) & \
                                   (~above.beans & ~right.beans & ~left.beans & ~below.beans) & \
                                    (~above.corn & ~right.corn & ~left.corn & ~below.corn)) >> (next.tomatoes & ~next.alive))

                    

                


                    

                    
    # get initial state
    build_init_state()

    return ENC