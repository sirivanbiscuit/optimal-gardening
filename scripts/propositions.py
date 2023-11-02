"""
This file contains (or should contain) all the proposition classes that will be
used in the logic execution to represent various elements and features of the
garden being modelled.
"""
from bauhaus import proposition
from setup import ENC

# This is a basic Hashable class
# Make all propositions extend it so that comparisons work proper
class PropBase:
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, __value: object) -> bool:
        return hash(self) == hash(__value)

    def __repr__(self):
        return str(self)
    

# TODO: Some of these classes below are very similar.
# We may want a child of PropBase that has their commonalities. 

# Trees and basic plants 
# (the type is a string such as "Corn", etc)
@proposition(ENC)
class Plant(PropBase):
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f"{self.type} at {(self.x, self.y)}"
    

# If the cell (x,y) is to be watered at time t
@proposition(ENC)
class Watered(PropBase):
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t
    
    def __str__(self) -> str:
        return f"{self.t}: {(self.x, self.y)} watered"


# If the cell (x,y) has a fence around it
@proposition(ENC)
class Fenced(PropBase):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f"{(self.x, self.y)} has fence"
    

# If the plant in a cell (x,y) 
# is being helped by its neighbour(s) at time t
@proposition(ENC)
class Helped(PropBase):
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t
    
    def __str__(self) -> str:
        return f"{self.t}: {(self.x, self.y)} helped"


# If the plant in a cell (x,y) 
# is being harmed by its neighbour(s) at time t
@proposition(ENC)
class Harmed(PropBase):
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t
    
    def __str__(self) -> str:
        return f"{self.t}: {(self.x, self.y)} harmed"


# If the plant in a cell (x,y) is alive at time t
@proposition(ENC)
class Alive(PropBase):
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t
    
    def __str__(self) -> str:
        return f"{self.t}: {(self.x, self.y)} alive"


# Plant Cell class
# Note this does NOT use logic libraries (i.e. bauhaus).
# It makes organizing cell features easier, as opposed to a big array.
class GardenPlot():
    def __init__(self, x, y, t, plant_type):
        self.x = x
        self.y = y
        self.plant = Plant(plant_type, x, y)
        self.watered = Watered(x, y, t)
        self.fenced = Fenced(x, y)
        self.helped = Helped(x, y, t)
        self.harmed = Harmed(x, y, t)
        self.alive = Alive(x, y, t)