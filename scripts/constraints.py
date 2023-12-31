"""
Method class for building the set of contraints the garden
will use during logic execution.
"""
from bauhaus import Encoding, And
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
            # all cells at t0 are alive, and not harmed/hurt
            ENC.add_constraint(~plot_i.get_prop('h'))
            ENC.add_constraint(~plot_i.get_prop('k'))
            # if INIT has a char at (x,y), plant a plant there:
            if len(id): ENC.add_constraint(plot_i.get_prop(id))
    # All cells (incl. rocks)
    for interval in G:
        if interval != 'u':
            for row in G[interval]:
                for plot in row:
                    if plot.x==0 or plot.y==0 or plot.x>s or plot.y>s:
                        # Border cells get Rocks regardless of INIT:
                        ENC.add_constraint(plot.get_prop('R'))
            

# All general constraints go here
# Make sure you import G as the garden grid from setup.py
def build_garden_theory(optimize:bool, opt_full:bool) -> Encoding:
    # PLANT RELATIONSHIPS
    # We don't need to evaluate the last time point as that is the end. 
    for t in range(len(G)-2):
        for x in range(1,len(G[t])-1):
            for y in range(1,len(G[t][x])-1):
                # Get the current "targeted" plant cell
                # We will add possible plant relationships to this particular cell.
                plot = G[t][x][y]
                # Constrains the plant to the left
                # See the wiki doc for plant relationships. 
                targ_plot_i = G[t][x][y-1] # cell to the left of target
                targ_plot_next = G[t+1][x][y-1] # cell to the left, but in the future interval
                ENC.add_constraint((plot.tomatoes & targ_plot_i.peppers & targ_plot_i.alive) >> targ_plot_next.helped)
                ENC.add_constraint((plot.tomatoes & targ_plot_i.corn & targ_plot_i.alive) >> targ_plot_next.harmed) 
                ENC.add_constraint((plot.beans & targ_plot_i.corn & targ_plot_i.alive) >> targ_plot_next.helped)
                ENC.add_constraint((plot.beans & targ_plot_i.peppers & targ_plot_i.alive) >> targ_plot_next.harmed)
                ENC.add_constraint((plot.pineTree & ~targ_plot_i.pineTree 
                                    & ~targ_plot_i.rock & targ_plot_i.alive) >> targ_plot_next.harmed)
                # Constrains the plant to the right
                # Same structure as above, but with different relationsips
                targ_plot_i = G[t][x][y+1]
                targ_plot_next = G[t+1][x][y+1]
                ENC.add_constraint((plot.tomatoes & targ_plot_i.peppers & targ_plot_i.alive) >> targ_plot_next.helped)
                ENC.add_constraint((plot.tomatoes & targ_plot_i.corn & targ_plot_i.alive) >> targ_plot_next.harmed) 
                ENC.add_constraint((plot.beans & targ_plot_i.corn & targ_plot_i.alive) >>  targ_plot_next.helped)
                ENC.add_constraint((plot.beans & targ_plot_i.peppers & targ_plot_i.alive) >> targ_plot_next.harmed)
                ENC.add_constraint((plot.pineTree & ~targ_plot_i.pineTree 
                                    & ~targ_plot_i.rock & targ_plot_i.alive) >> targ_plot_next.harmed)
                # Constrains the plant above
                # Same structure as above, but with different relationsips
                targ_plot_i = G[t][x-1][y]
                targ_plot_next = G[t+1][x-1][y]
                ENC.add_constraint((plot.corn & targ_plot_i.beans & targ_plot_i.alive) >> targ_plot_next.helped)
                ENC.add_constraint((plot.corn & targ_plot_i.tomatoes & targ_plot_i.alive) >> targ_plot_next.harmed)
                ENC.add_constraint((plot.peppers & targ_plot_i.tomatoes & targ_plot_i.alive) >> targ_plot_next.helped)
                ENC.add_constraint((plot.peppers & targ_plot_i.beans & targ_plot_i.alive) >> targ_plot_next.harmed)
                ENC.add_constraint((plot.pineTree & ~targ_plot_i.pineTree 
                                    & ~targ_plot_i.rock & targ_plot_i.alive) >> targ_plot_next.harmed)
                # Constrains the plant below
                # Same structure as above, but with different relationsips
                targ_plot_i = G[t][x+1][y]
                targ_plot_next = G[t+1][x+1][y]
                ENC.add_constraint((plot.corn & targ_plot_i.beans & targ_plot_i.alive) >> targ_plot_next.helped)
                ENC.add_constraint((plot.corn & targ_plot_i.tomatoes & targ_plot_i.alive) >> targ_plot_next.harmed)
                ENC.add_constraint((plot.peppers & targ_plot_i.tomatoes & targ_plot_i.alive) >> targ_plot_next.helped)
                ENC.add_constraint((plot.peppers & targ_plot_i.beans & targ_plot_i.alive) >> targ_plot_next.harmed)
                ENC.add_constraint((plot.pineTree & ~targ_plot_i.pineTree 
                                    & ~targ_plot_i.rock & targ_plot_i.alive) >> targ_plot_next.harmed)
    
    # PLANT RELATIONSHIPS; INVERSE IMPLICATIONS SO THERE'S ONLY ONE SOLUTION
    # This code applies constraints to the next version of this plot, not to a target plot.
    # We don't need to evaluate the last time point as that is the end.
    for t in range(len(G)-2):
        for x in range(1,len(G[t])-1):
            for y in range(1,len(G[t][x])-1):
                # Get cells in various directions
                plot = G[t][x][y]
                above_plot_i = G[t][x-1][y]
                below_plot_i = G[t][x+1][y]
                left_plot_i = G[t][x][y-1]
                right_plot_i = G[t][x][y+1]
                plot_next = G[t+1][x][y]
                # If nothing could possibly be helping it, it's not helped:
                ENC.add_constraint((((plot.corn & ~left_plot_i.beans & ~right_plot_i.beans) |
                                   (plot.peppers & ~left_plot_i.tomatoes & ~right_plot_i.tomatoes) |
                                   (plot.tomatoes & ~above_plot_i.peppers & ~below_plot_i.peppers) |
                                   (plot.beans & ~above_plot_i.corn & ~below_plot_i.corn))
                                    & plot.alive)
                                   >> ~plot_next.helped)
                # It nothing could possibly be hurting it, it's not harmed:
                ENC.add_constraint((((plot.corn & ~left_plot_i.tomatoes & ~right_plot_i.tomatoes) |
                                   (plot.peppers & ~left_plot_i.beans & ~right_plot_i.beans) |
                                   (plot.tomatoes & ~above_plot_i.corn & ~below_plot_i.corn) |
                                   (plot.beans & ~above_plot_i.peppers & ~below_plot_i.peppers)) &
                                   (~right_plot_i.pineTree & ~left_plot_i.pineTree 
                                    & ~above_plot_i.pineTree & ~below_plot_i.pineTree)
                                    & plot.alive)
                                   >> ~plot_next.harmed)

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
                    # Rock defaults
                    ENC.add_constraint(
                        plot.rock >> (~plot.corn & ~plot.beans & ~plot.tomatoes & ~plot.peppers & ~plot.pineTree
                        & ~plot.helped & ~plot.harmed & ~plot.alive))
                    # Pine tree defaults
                    ENC.add_constraint(plot.pineTree >> (~plot.helped & ~plot.harmed & plot.alive))
                    # Cells must have plants
                    ENC.add_constraint(plot.corn | plot.beans | plot.tomatoes | plot.peppers | plot.rock | plot.pineTree)
                    # helped or not hurt IF AND ONLY IF alive (and vice versa)
                    ENC.add_constraint(((plot.helped | ~plot.harmed) & ~plot.rock) >> plot.alive)
                    ENC.add_constraint(plot.alive >> ((plot.helped | ~plot.harmed) & ~plot.rock))
    
    # PLANT SPREADING
    for t in range(len(G)-2):
        for x in range(1,len(G[t])-1):
            for y in range(1,len(G[t][x])-1):
                # Directions
                above = G[t][x-1][y]
                below = G[t][x+1][y]
                left = G[t][x][y-1]
                right = G[t][x][y+1]
                next = G[t+1][x][y]
                plot = G[t][x][y]
                # Trees and rocks cannot be altered
                ENC.add_constraint(plot.pineTree >> next.pineTree)
                ENC.add_constraint(plot.rock >> next.rock)
                # Plants that are alive on a given time interval can't get overrun:
                ENC.add_constraint((plot.corn & plot.alive) >> (next.corn))
                ENC.add_constraint((plot.beans & plot.alive) >> (next.beans))
                ENC.add_constraint((plot.peppers & plot.alive) >> (next.peppers))
                ENC.add_constraint((plot.tomatoes & plot.alive) >> (next.tomatoes))
                # Looks at plant in all directions around, if at least one it becomes that plant (in order of priority)
                # Corn: Likes Beans, Indifferent to Peppers, Hates Tomato
                # Thus, priority goes Beans>Peppers>Tomatoes
                # If nothing can override, then keep the plant itself, and dead.
                ENC.add_constraint((plot.corn & ~plot.alive & (above.beans | right.beans | left.beans | below.beans))
                                   >> (next.beans & ~next.helped & ~next.harmed))
                ENC.add_constraint((plot.corn & ~plot.alive & (~above.beans & ~right.beans & ~left.beans & ~below.beans) &
                                    (above.peppers | right.peppers | left.peppers | below.peppers)) 
                                   >> (next.peppers & ~next.helped & ~next.harmed))
                ENC.add_constraint((plot.corn & ~plot.alive & (~above.beans & ~right.beans & ~left.beans & ~below.beans) &
                                   (~above.peppers & ~right.peppers & ~left.peppers & ~below.peppers) &
                                    (above.tomatoes | left.tomatoes | right.tomatoes | below.tomatoes)) 
                                   >> (next.tomatoes & ~next.helped & ~next.harmed))
                ENC.add_constraint((plot.corn & ~plot.alive & (~above.beans & ~right.beans & ~left.beans & ~below.beans) &
                                   (~above.peppers & ~right.peppers & ~left.peppers & ~below.peppers) &
                                    (~above.tomatoes & ~left.tomatoes & ~right.tomatoes & ~below.tomatoes)) 
                                   >> (next.corn & ~next.alive))
                # Beans: Likes Corn, Indifferent to Tomato, Hates Peppers
                ENC.add_constraint((plot.beans & ~plot.alive & (above.corn | right.corn | left.corn | below.corn)) 
                                   >> (next.corn & ~next.helped & ~next.harmed))
                ENC.add_constraint((plot.beans & ~plot.alive & (~above.corn & ~right.corn & ~left.corn & ~below.corn) &
                                   (above.tomatoes | left.tomatoes | right.tomatoes | below.tomatoes)) 
                                   >> (next.tomatoes & ~next.helped & ~next.harmed))                
                ENC.add_constraint((plot.beans & ~plot.alive & (~above.corn & ~right.corn & ~left.corn & ~below.corn) &
                                   (~above.tomatoes & ~left.tomatoes & ~right.tomatoes & ~below.tomatoes) &
                                    (above.peppers | right.peppers | left.peppers | below.peppers)) 
                                   >> (next.peppers & ~next.helped & ~next.harmed))                
                ENC.add_constraint((plot.beans & ~plot.alive & (~above.corn & ~right.corn & ~left.corn & ~below.corn) &
                                   (~above.tomatoes & ~left.tomatoes & ~right.tomatoes & ~below.tomatoes) &
                                    (~above.peppers & ~right.peppers & ~left.peppers & ~below.peppers)) 
                                   >> (next.beans & ~next.alive))
                # Peppers: Likes Tomato, Indifferent to Corn, Hates Beans
                ENC.add_constraint((plot.peppers & ~plot.alive & (above.tomatoes | left.tomatoes | right.tomatoes | below.tomatoes)) 
                                   >> (next.tomatoes & ~next.helped & ~next.harmed))
                ENC.add_constraint((plot.peppers & ~plot.alive & (~above.tomatoes & ~left.tomatoes & ~right.tomatoes & ~below.tomatoes) &
                                   (above.corn | right.corn | left.corn | below.corn)) 
                                   >> (next.corn & ~next.helped & ~next.harmed))  
                ENC.add_constraint((plot.peppers & ~plot.alive & (~above.tomatoes & ~left.tomatoes & ~right.tomatoes & ~below.tomatoes) &
                                    (~above.corn & ~right.corn & ~left.corn & ~below.corn) &
                                    (above.beans | right.beans | left.beans | below.beans)) 
                                   >> (next.beans & ~next.helped & ~next.harmed)) 
                ENC.add_constraint((plot.peppers & ~plot.alive & (~above.tomatoes & ~left.tomatoes & ~right.tomatoes & ~below.tomatoes) &
                                    (~above.corn & ~right.corn & ~left.corn & ~below.corn) &
                                    (~above.beans & ~right.beans & ~left.beans & ~below.beans)) 
                                   >> (next.peppers & ~next.alive))
                # Tomatoes: Likes Peppers, Indifferent to Beans, Hates Corn
                ENC.add_constraint((plot.tomatoes & ~plot.alive & (above.peppers | left.peppers | right.peppers | below.peppers)) 
                                   >> (next.peppers & ~next.helped & ~next.harmed))
                ENC.add_constraint((plot.tomatoes & ~plot.alive & (~above.peppers & ~right.peppers & ~left.peppers & ~below.peppers) &
                                   (above.beans | right.beans | left.beans | below.beans)) 
                                   >> (next.beans & ~next.helped & ~next.harmed))   
                ENC.add_constraint((plot.tomatoes & ~plot.alive & (~above.peppers & ~right.peppers & ~left.peppers & ~below.peppers) &
                                   (~above.beans & ~right.beans & ~left.beans & ~below.beans) &
                                    (above.corn | right.corn | left.corn | below.corn)) 
                                   >> (next.corn & ~next.helped & ~next.harmed))   
                ENC.add_constraint((plot.tomatoes & ~plot.alive & (~above.peppers & ~right.peppers & ~left.peppers & ~below.peppers) &
                                   (~above.beans & ~right.beans & ~left.beans & ~below.beans) &
                                    (~above.corn & ~right.corn & ~left.corn & ~below.corn)) 
                                   >> (next.tomatoes & ~next.alive))
    
    # OPTIMIZATION (optional)
    if optimize:
        # Immediate optimization (opt_full) means all intervals are the same.
        # - Seeing that t0=t1 would be the simplest, so we will assert that.
        # Non-immediate optimizations means it reaches a point that is
        # optimized. We can only be assured this if the LAST two intervals are
        # the same. Since t(n) >> t(n+1), all future ones are the same too.
        # - Sees that the last two intervals are equal and alive.
        last = len(G)-2 if not opt_full else 1
        sec_last = last-1 if not opt_full else 0
        full_interv = []
        for x in range(1,len(G[last])-1):
            for y in range(1,len(G[last][x])-1):
                plot_sl = G[sec_last][x][y]
                plot_last = G[last][x][y]
                full_interv.append((plot_sl.alive & plot_last.alive) | plot_sl.rock)
        ENC.add_constraint(And(full_interv))
                   
    # Get initial state
    build_init_state()

    # Return theory
    return ENC