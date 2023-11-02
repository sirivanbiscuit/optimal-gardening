"""
Initialization file for objects used across various scripts.

"""
from bauhaus import Encoding
from propositions import tile

ENC = Encoding()

# thing ???
def grid_creation(rowlength, columnlength):

    grid = []
    for i in range (columnlength):
        grid.append(row)
        for j in range (rowlength):
            row = []
            row.append(tile(i,j))

    return grid