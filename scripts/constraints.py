"""
Method class for building the set of contraints the garden
will use during logic execution.
"""
from bauhaus import Encoding
from scripts.encoding import ENC
from scripts.setup import G, INIT
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
            plot_i = G[0][x+1][y+1]
            ENC.add_constraint(~plot_i.get_prop('h'))
            ENC.add_constraint(~plot_i.get_prop('k'))
            if len(id): ENC.add_constraint(plot_i.get_prop(id))
    
    # All cells (incl. rocks)
    for interval in G:
        if interval != 'u':
            for row in G[interval]:
                for plot in row:
                    if plot.x==0 or plot.y==0 or plot.x>s or plot.y>s:
                        ENC.add_constraint(plot.get_prop('R'))
            

# All our general constraints go here
# Make sure you import G as the garden grid from setup.py
def build_garden_theory() -> Encoding:
    
    # PLANT RELATIONSHIPS
    # NEEDS INVERSE IMPLICATIONS SO THERE'S ONLY ONE SOLUTION
    # We don't need to evaluate the last time point as that is the end. 
    for t in range(len(G)-2):
        for x in range(1,len(G[t])-1):
            for y in range(1,len(G[t][x])-1):
                plot = G[t][x][y]
                # Constrains the plant to the left
                targ_plot_i = G[t][x][y-1]
                targ_plot_next = G[t+1][x][y-1]
                ENC.add_constraint((plot.tomatoes & targ_plot_i.peppers & targ_plot_i.alive) >> 
                                   targ_plot_next.helped)
                ENC.add_constraint((plot.tomatoes & targ_plot_i.corn & targ_plot_i.alive) >> 
                                       targ_plot_next.harmed) 
                ENC.add_constraint((plot.beans & targ_plot_i.corn & targ_plot_i.alive) >> 
                                       targ_plot_next.helped)
                ENC.add_constraint((plot.beans & targ_plot_i.peppers & targ_plot_i.alive) >> 
                                       targ_plot_next.harmed)
                ENC.add_constraint((plot.pineTree & ~targ_plot_i.pineTree & ~targ_plot_i.rock & targ_plot_i.alive) >> 
                                       targ_plot_next.harmed)
                #Constrains the plant to the right
                targ_plot_i = G[t][x][y+1]
                targ_plot_next = G[t+1][x][y+1]
                ENC.add_constraint((plot.tomatoes & targ_plot_i.peppers & targ_plot_i.alive) >> 
                                       targ_plot_next.helped)
                ENC.add_constraint((plot.tomatoes & targ_plot_i.corn & targ_plot_i.alive) >> 
                                       targ_plot_next.harmed) 
                ENC.add_constraint((plot.beans & targ_plot_i.corn & targ_plot_i.alive) >> 
                                       targ_plot_next.helped)
                ENC.add_constraint((plot.beans & targ_plot_i.peppers & targ_plot_i.alive) >> 
                                       targ_plot_next.harmed)
                ENC.add_constraint((plot.pineTree & ~targ_plot_i.pineTree & ~targ_plot_i.rock & targ_plot_i.alive) >> 
                                       targ_plot_next.harmed)
                #Constrains the plant above
                targ_plot_i = G[t][x-1][y]
                targ_plot_next = G[t+1][x-1][y]
                ENC.add_constraint((plot.corn & targ_plot_i.beans & targ_plot_i.alive) >> 
                                       targ_plot_next.helped)
                ENC.add_constraint((plot.corn & targ_plot_i.tomatoes & targ_plot_i.alive) >> 
                                       targ_plot_next.harmed)
                ENC.add_constraint((plot.peppers & targ_plot_i.tomatoes & targ_plot_i.alive) >> 
                                       targ_plot_next.helped)
                ENC.add_constraint((plot.peppers & targ_plot_i.beans & targ_plot_i.alive) >> 
                                       targ_plot_next.harmed)
                ENC.add_constraint((plot.pineTree & ~targ_plot_i.pineTree & ~targ_plot_i.rock & targ_plot_i.alive) >> 
                                       targ_plot_next.harmed)
                # Constrains the plant below
                targ_plot_i = G[t][x+1][y]
                targ_plot_next = G[t+1][x+1][y]
                ENC.add_constraint((plot.corn & targ_plot_i.beans & targ_plot_i.alive) >> 
                                       targ_plot_next.helped)
                ENC.add_constraint((plot.corn & targ_plot_i.tomatoes & targ_plot_i.alive) >> 
                                       targ_plot_next.harmed)
                ENC.add_constraint((plot.peppers & targ_plot_i.tomatoes & targ_plot_i.alive) >> 
                                       targ_plot_next.helped)
                ENC.add_constraint((plot.peppers & targ_plot_i.beans & targ_plot_i.alive) >> 
                                       targ_plot_next.harmed)
                ENC.add_constraint((plot.pineTree & ~targ_plot_i.pineTree & ~targ_plot_i.rock & targ_plot_i.alive) >> 
                                       targ_plot_next.harmed)
    
    # PLANT RELATIONSHIPS; INVERSE IMPLICATIONS SO THERE'S ONLY ONE SOLUTION
    # This code applies constraints to the next version of this plot, not to a target plot. 
    # Find how many time points the garden exist for, 
    # subtracting the constant key
    # We don't need to evaluate the last time point as that is the end.
    for t in range(len(G)-2):
        for x in range(1,len(G[t])-1):
            for y in range(1,len(G[t][x])-1):
                plot = G[t][x][y]
                above_plot_i = G[t][x-1][y]
                below_plot_i = G[t][x+1][y]
                left_plot_i = G[t][x][y-1]
                right_plot_i = G[t][x][y+1]
                plot_next = G[t+1][x][y]
                #Inverse constraints for helped
                ENC.add_constraint((((plot.corn & ~left_plot_i.beans & ~right_plot_i.beans) |
                                   (plot.peppers & ~left_plot_i.tomatoes & ~right_plot_i.tomatoes) |
                                   (plot.tomatoes & ~above_plot_i.peppers & ~below_plot_i.peppers) |
                                   (plot.beans & ~above_plot_i.corn & ~below_plot_i.corn))
                                     & plot.alive)
                                   >> 
                                       ~plot_next.helped)
                #Inverse Constraints for hindered
                ENC.add_constraint((((plot.corn & ~left_plot_i.tomatoes & ~right_plot_i.tomatoes) |
                                   (plot.peppers & ~left_plot_i.beans & ~right_plot_i.beans) |
                                   (plot.tomatoes & ~above_plot_i.corn & ~below_plot_i.corn) |
                                   (plot.beans & ~above_plot_i.peppers & ~below_plot_i.peppers)) &
                                   (~right_plot_i.pineTree & ~left_plot_i.pineTree & ~above_plot_i.pineTree & ~below_plot_i.pineTree)
                                    & plot.alive)
                                   >> 
                                       ~plot_next.harmed)


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
                    
                    # Rock settings
                    ENC.add_constraint(
                        plot.rock >> (~plot.corn & ~plot.beans & ~plot.tomatoes & ~plot.peppers & ~plot.pineTree
                        & ~plot.helped & ~plot.harmed & ~plot.alive))
                    
                    # Pine tree settings
                    ENC.add_constraint(plot.pineTree >> (~plot.helped & ~plot.harmed & plot.alive))
                    
                    # Cells must have plants
                    ENC.add_constraint(plot.corn | plot.beans | plot.tomatoes | plot.peppers | plot.rock | plot.pineTree)
                    
                    # helped or not hurt impl. alive
                    ENC.add_constraint(((plot.helped | ~plot.harmed) & ~plot.rock) >> plot.alive)
                    ENC.add_constraint(plot.alive >> ((plot.helped | ~plot.harmed) & ~plot.rock))
    
    
    # PLANT SPREADING
    for t in range(len(G)-2):
        for x in range(1,len(G[t])-1):
            for y in range(1,len(G[t][x])-1):
                
                #array of spreading value in order
                # for example corn: (beans, peppers, tomatoes, dead)
                above = G[t][x-1][y]
                below = G[t][x+1][y]
                left = G[t][x][y-1]
                right = G[t][x][y+1]
                next = G[t+1][x][y]
                plot = G[t][x][y]


                ENC.add_constraint(plot.pineTree >> next.pineTree)
                ENC.add_constraint(plot.rock >> next.rock)

                #Looks at plant in all directions around, if at least one it becomes that plant (in order of priority)
                #Corn
                ENC.add_constraint((plot.corn & plot.alive) >> (next.corn))
                ENC.add_constraint((plot.corn & ~plot.alive & (above.beans | right.beans | left.beans | below.beans)) >> (next.beans & ~next.helped & ~next.harmed))
                ENC.add_constraint((plot.corn & ~plot.alive & (~above.beans & ~right.beans & ~left.beans & ~below.beans) &
                                    (above.peppers | right.peppers | left.peppers | below.peppers)) >> (next.peppers & ~next.helped & ~next.harmed))
                ENC.add_constraint((plot.corn & ~plot.alive & (~above.beans & ~right.beans & ~left.beans & ~below.beans) &
                                   (~above.peppers & ~right.peppers & ~left.peppers & ~below.peppers) &
                                    (above.tomatoes | left.tomatoes | right.tomatoes | below.tomatoes)) >> (next.tomatoes & ~next.helped & ~next.harmed))
                ENC.add_constraint((plot.corn & ~plot.alive & (~above.beans & ~right.beans & ~left.beans & ~below.beans) &
                                   (~above.peppers & ~right.peppers & ~left.peppers & ~below.peppers) &
                                    (~above.tomatoes & ~left.tomatoes & ~right.tomatoes & ~below.tomatoes)) >> (next.corn & ~next.alive))
                
                #Beans
                ENC.add_constraint((plot.beans & plot.alive) >> (next.beans))
                ENC.add_constraint((plot.beans & ~plot.alive & (above.corn | right.corn | left.corn | below.corn)) >> (next.corn & ~next.helped & ~next.harmed))
                ENC.add_constraint((plot.beans & ~plot.alive & (~above.corn & ~right.corn & ~left.corn & ~below.corn) &
                                   (above.tomatoes | left.tomatoes | right.tomatoes | below.tomatoes)) >> (next.tomatoes & ~next.helped & ~next.harmed))                
                ENC.add_constraint((plot.beans & ~plot.alive & (~above.corn & ~right.corn & ~left.corn & ~below.corn) &
                                   (~above.tomatoes & ~left.tomatoes & ~right.tomatoes & ~below.tomatoes) &
                                    (above.peppers | right.peppers | left.peppers | below.peppers)) >> (next.peppers & ~next.helped & ~next.harmed))                
                ENC.add_constraint((plot.beans & ~plot.alive & (~above.corn & ~right.corn & ~left.corn & ~below.corn) &
                                   (~above.tomatoes & ~left.tomatoes & ~right.tomatoes & ~below.tomatoes) &
                                    (~above.peppers & ~right.peppers & ~left.peppers & ~below.peppers)) >> (next.beans & ~next.alive))
                
                #Peppers
                ENC.add_constraint((plot.peppers & plot.alive) >> (next.peppers))
                ENC.add_constraint((plot.peppers & ~plot.alive & (above.tomatoes | left.tomatoes | right.tomatoes | below.tomatoes)) >> (next.tomatoes & ~next.helped & ~next.harmed))
                ENC.add_constraint((plot.peppers & ~plot.alive & (~above.tomatoes & ~left.tomatoes & ~right.tomatoes & ~below.tomatoes) &
                                   (above.corn | right.corn | left.corn | below.corn)) >> (next.corn & ~next.helped & ~next.harmed))  
                ENC.add_constraint((plot.peppers & ~plot.alive & (~above.tomatoes & ~left.tomatoes & ~right.tomatoes & ~below.tomatoes) &
                                    (~above.corn & ~right.corn & ~left.corn & ~below.corn) &
                                    (above.beans | right.beans | left.beans | below.beans)) >> (next.beans & ~next.helped & ~next.harmed)) 
                ENC.add_constraint((plot.peppers & ~plot.alive & (~above.tomatoes & ~left.tomatoes & ~right.tomatoes & ~below.tomatoes) &
                                    (~above.corn & ~right.corn & ~left.corn & ~below.corn) &
                                    (~above.beans & ~right.beans & ~left.beans & ~below.beans)) >> (next.peppers & ~next.alive))
                
                #Tomatoes
                ENC.add_constraint((plot.tomatoes & plot.alive) >> (next.tomatoes))
                ENC.add_constraint((plot.tomatoes & ~plot.alive & (above.peppers | left.peppers | right.peppers | below.peppers)) >> (next.peppers & ~next.helped & ~next.harmed))
                ENC.add_constraint((plot.tomatoes & ~plot.alive & (~above.peppers & ~right.peppers & ~left.peppers & ~below.peppers) &
                                   (above.beans | right.beans | left.beans | below.beans)) >> (next.beans & ~next.helped & ~next.harmed))   
                ENC.add_constraint((plot.tomatoes & ~plot.alive & (~above.peppers & ~right.peppers & ~left.peppers & ~below.peppers) &
                                   (~above.beans & ~right.beans & ~left.beans & ~below.beans) &
                                    (above.corn | right.corn | left.corn | below.corn)) >> (next.corn & ~next.helped & ~next.harmed))   
                ENC.add_constraint((plot.tomatoes & ~plot.alive & (~above.peppers & ~right.peppers & ~left.peppers & ~below.peppers) &
                                   (~above.beans & ~right.beans & ~left.beans & ~below.beans) &
                                    (~above.corn & ~right.corn & ~left.corn & ~below.corn)) >> (next.tomatoes & ~next.alive))

              
    # get initial state
    build_init_state()

    return ENC