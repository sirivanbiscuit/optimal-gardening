"""
Method class for building the set of contraints the garden
will use during logic execution.
"""
from bauhaus import Encoding, constraint
from setup import ENC, setup_default, full_garden
from propositions import *

def build_garden_theory() -> Encoding:
    # TODO: completed constraint list
    # Some constraints will be more difficult to
    # implement. They will be done at a later date.

    # MAKE SURE THAT INTERVAL STATES ARE MATERIALLY IMPLIED SOLELY
    # FROM THE PREVIOUS INTERVAL STATE (except for interval 0)

    garden = setup_default() # default garden, could be changed later
    
    # A plant that is both helped and harmed remains alive
    for t in garden:
        for x in garden[t]:
            for y in garden[t][x]:
                plot = garden[t][x][y]
                ENC.add_constraint(plot.helped & ~plot.harmed >> plot.alive)

    # TODO: add plant relationships.
    # - Corn and Beans help each other if not fenced
    # - Tomatoes and Peppers help each other if not fenced
    # - Corn and Tomatoes harm each other if not fenced
    # - Beans and Peppers harm each other if not fenced
    # - Pine Trees harm every plant but themselves if not fenced

    # TODO: make watering/fencing.
    # - Watered cell >> plant is alive
    # - Fenced cell >> plant is alive

    return ENC