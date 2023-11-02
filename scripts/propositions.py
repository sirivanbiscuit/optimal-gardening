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


# Plant
@proposition(ENC)
class Plant(PropBase):

    # Might alter to not def the x,y here, get it defined when added to the tile function or smth
    def __init__(self):
        # self.x = x
        # self.y = y
        self.type = self
    def __repr__(self):
        return f"{self.x}, {self.y}"
    def type(self):
        return self.type
    

# Helped
@proposition(ENC)
class helped(PropBase):
    def __init__(self, x, y):
        self.x = x
        self.y = y


# class is just for grouping all data onto one slot that can be accessed with the just the xy value
# could just as easily give the same stuff with a list or something, I just thought of this first
@proposition(ENC)
class tile(PropBase):
    def __init__ (self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"{self.x}, {self.y}"

        # Others that need to go in here
    def setplant (self, plant):
        self.plant_type = Plant.type(plant)
    
    #def set
    def isHelped (self, boolean_help):
        self.is_helped = boolean_help

    def isHarmed (self, boolean_harmed):
        self.is_harmed = boolean_harmed

    def isAlive (self, is_alive):
        self.is_alive = is_alive


        #self.iswatered = watered
        #self.isfenced = fenced

    def get_plant(self):
        return self.plant_type
    
    def get_adjacent(self):
        adjacents = []

        # probably not alowed based on what he said today, not sure though
        row_adjacent = grid(x,y+1)
        column_adjacent = grid(x+1,y)
        adjacents.append(row_adjacent)
        adjacents.append(column_adjacent)