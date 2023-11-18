"""
This file contains (or should contain) all the proposition classes that will be
used in the logic execution to represent various elements and features of the
garden being modelled.
"""
from bauhaus import proposition, constraint
from setup import ENC


# Everything in this file should be a child of this.
# Well-raised children of Hashables stay out of the hood:
class PropBase:
    """
    A basic Hashable class for making propositions.\n
    You should make all propositions extend this 
    so that comparisons work properly.
    """
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, __value: object) -> bool:
        return hash(self) == hash(__value)

    def __repr__(self):
        return str(self)


# Use this class as a parent to plant types, since they all
# have more or less the same details, just different names:
class Plant(PropBase):
    """
    Parent class for building specific plant propositions.
    """
    def __init__(self, type, x, y, t):
        self.type = type
        self.x, self.y, self.t = x, y, t

    def __str__(self) -> str:
        return f"t{self.t}: {self.type} at {(self.x, self.y)}"


"""
Use instances of these as your plant variables.
This makes sure plant type strings are consistent across the code.
"""

@proposition(ENC)
class Corn(Plant):
    def __init__(self, x, y, t): super().__init__("Corn", x, y, t)

@proposition(ENC)
class Beans(Plant):
    def __init__(self, x, y, t): super().__init__("Beans", x, y, t)

@proposition(ENC)   
class Tomatoes(Plant):
    def __init__(self, x, y, t): super().__init__("Tomatoes", x, y, t)
    
@proposition(ENC)
class Peppers(Plant):
    def __init__(self, x, y, t): super().__init__("Peppers", x, y, t)
   
@proposition(ENC) 
class PineTree(Plant):
    def __init__(self, x, y, t): super().__init__("Pine Tree", x, y, t)


"""
All classes below describe the state of plants in cells.
Keep note that certain ones of these aren't time-based (i.e. fencing).
If a proposition has usage limits, annotate the class @constraint.
"""

# Fenced f(x,y)
@constraint.at_most_one(ENC)
@proposition(ENC)
class Fenced(PropBase):
    """
    Represents the proposition f(x,y) that is whether or not
    there is a fence around the cell at position (x,y).
    """
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self) -> str:
        return f"{(self.x, self.y)} has fence"


# Helped h(x,y,t)
@proposition(ENC)
class Helped(PropBase):
    """
    Represents the proposition h(x,y,t) that is whether or not
    the plant in the cell at (x,y) at time t is being helped.
    """
    def __init__(self, x, y, t):
        self.x, self.y, self.t = x, y, t

    def __str__(self) -> str:
        return f"t{self.t}: {(self.x, self.y)} helped"


# Harmed k(x,y,t)
@proposition(ENC)
class Harmed(PropBase):
    """
    Represents the proposition k(x,y,t) that is whether or not
    the plant in the cell at (x,y) at time t is being harmed.
    """
    def __init__(self, x, y, t):
        self.x, self.y, self.t = x, y, t

    def __str__(self) -> str:
        return f"t{self.t}: {(self.x, self.y)} harmed"


# Alive a(x,y,t)
@proposition(ENC)
class Alive(PropBase):
    """
    Represents the proposition a(x,y,t) that is whether or not
    the plant in the cell at (x,y) at time t is alive.
    """
    def __init__(self, x, y, t):
        self.x, self.y, self.t = x, y, t

    def __str__(self) -> str:
        return f"t{self.t}: {(self.x, self.y)} alive"


# A structure for encapsulating the entirety of a certain cell:
class GardenPlot():
    """
    Represents the entire data structure of a particular cell
    at (x,y) at time interval t.\n
    This class should be thought of more as an array, as it 
    obtains no methods, and rather just stores all cell data 
    in one convenient location.
    """
    def __init__(self, x, y, t):
        self.x, self.y, self.t = x, y, t
        self.corn = Corn(x, y, t)
        self.beans = Beans(x, y, t)
        self.tomatoes = Tomatoes(x, y, t)
        self.peppers = Peppers(x, y, t)
        self.pineTree = PineTree(x, y, t)
        self.helped = Helped(x, y, t)
        self.harmed = Harmed(x, y, t)
        self.alive = Alive(x, y, t)