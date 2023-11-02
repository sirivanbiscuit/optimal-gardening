"""
Initialization file for objects used across various scripts.
"""
from bauhaus import Encoding
from propositions import GardenPlot

ENC = Encoding()

# DEFAULT GARDEN
# A 3x3 garden with Pine Trees in each corner.
# Non-corners have all Corn plants.
def setup_default() -> list:
    full_garden = []
    default_size = 3
    default_time_length = 10
    default_grid = [
        ["Pine", "Corn", "Pine"],
        ["Corn", "Corn", "Corn"],
        ["Pine", "Corn", "Pine"]
    ]

    for t in range(default_time_length):
        interval_garden = []
        for x in range(default_size):
            row = []
            for y in range(default_size):
                row.append(GardenPlot(x, y, t, default_grid[x][y]))
            interval_garden.append(row)
        full_garden.append(interval_garden)

    return full_garden


# TODO: Make default fence/watering locations for testing