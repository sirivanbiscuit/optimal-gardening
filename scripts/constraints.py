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
    
    dictloops = 0
    garden_size = len(garden[0])
    # A plant that is both helped and harmed remains alive
    while dictloops < garden_size:
        for x in garden[dictloops]:
            for y in garden[dictloops][x]:
                plot = garden[dictloops][x][y]
                if x-1 >= 0:
                    ENC.add_constraint(plot.tomato & garden[dictloops][x-1][y].peppers >> garden[dictloops][x-1][y].helped)
                    ENC.add_constraint(plot.tomato & garden[dictloops][x-1][y].corn >> garden[dictloops][x-1][y].harmed) 
                    ENC.add_constraint(plot.beans & garden[dictloops][x-1][y].corn >> garden[dictloops][x-1][y].helped)
                    ENC.add_constraint(plot.beans & garden[dictloops][x-1][y].peppers >> garden[dictloops][x-1][y].harmed)

                if x+1 <= garden_size:
                    ENC.add_constraint(plot.tomato & garden[dictloops][x+1][y].peppers >> garden[dictloops][x+1][y].helped)
                    ENC.add_constraint(plot.tomato & garden[dictloops][x+1][y].corn >> garden[dictloops][x+1][y].harmed) 
                    ENC.add_constraint(plot.beans & garden[dictloops][x+1][y].corn >> garden[dictloops][x+1][y].helped)
                    ENC.add_constraint(plot.beans & garden[dictloops][x+1][y].peppers >> garden[dictloops][x+1][y].harmed)

                if y-1 >= 0:
                    ENC.add_constraint(plot.corn & garden[dictloops][x][y-1].beans >> garden[dictloops][x][y-1].helped)
                    ENC.add_constraint(plot.corn & garden[dictloops][x][y-1].tomatoes >> garden[dictloops][x][y-1].harmed)
                    ENC.add_constraint(plot.peppers & garden[dictloops][x][y-1].tomatoes >> garden[dictloops][x][y-1].helped)
                    ENC.add_constraint(plot.peppers & garden[dictloops][x][y-1].beans >> garden[dictloops][x][y-1].harmed)

                if y+1 <= garden_size:
                    ENC.add_constraint(plot.corn & garden[dictloops][x][y+1].beans >> garden[dictloops][x][y+1].helped)
                    ENC.add_constraint(plot.corn & garden[dictloops][x][y+1].tomatoes >> garden[dictloops][x][y+1].harmed)
                    ENC.add_constraint(plot.peppers & garden[dictloops][x][y+1].tomatoes >> garden[dictloops][x][y+1].helped)
                    ENC.add_constraint(plot.peppers & garden[dictloops][x][y+1].beans >> garden[dictloops][x][y+1].harmed)
        dictloops += 1

    # TODO: make watering/fencing.
    # - Watered cell >> plant is alive
    # - Fenced cell >> plant is alive

    return ENC