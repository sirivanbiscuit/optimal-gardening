
import sys

from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

NUM_NODES = int(sys.argv[1])

# Encoding that will store all of your constraints
E = Encoding()

class Hashable:
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, __value: object) -> bool:
        return hash(self) == hash(__value)

    def __repr__(self):
        return str(self)

# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class Edge(Hashable):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x} -> {self.y})"


@proposition(E)
class Distance(Hashable):

    def __init__(self, x, y, n) -> None:
        self.x = x
        self.y = y
        self.n = n


    def __str__(self) -> str:
        return f"d({self.x}, {self.y}) = {self.n}"


all_edges = []
for n1 in range(NUM_NODES):
    for n2 in range(NUM_NODES):
        all_edges.append(Edge(f'n{n1}', f'n{n2}'))

all_distances = []
for edge in all_edges:
    for d in range(NUM_NODES+1):
        all_distances.append(Distance(edge.x, edge.y, d))


def example_theory():

    # I don't want self loops in my theory
    for node in range(NUM_NODES):
        E.add_constraint(~Edge(f'n{node}', f'n{node}'))

    # A node is distance 0 to itself
    for node in range(NUM_NODES):
        E.add_constraint(Distance(f'n{node}', f'n{node}', 0))

    # Nodes that are connected, have a distance of 1
    for edge in all_edges:
        dprop = Distance(edge.x, edge.y, 1)
        E.add_constraint(edge >> dprop)

    # Get all of the propositions in there
    for edge in all_edges:
        E.add_constraint(edge | ~edge)

    return E


def print_graph(sol):
    print("\tAdjacency List:")
    for n1 in range(NUM_NODES):
        out = f"\t  n{n1}:"
        for n2 in range(NUM_NODES):
            if sol[Edge(f'n{n1}', f'n{n2}')]:
                out += f" n{n2}"
        print(out)

if __name__ == "__main__":

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    # print("   Solution: %s" % T.solve())

    print("    Solution:")
    print_graph(T.solve())

    # print("\nVariable likelihoods:")
    # for v,vn in zip([e1,e2,e3], ["e1", "e2", "e3"]):
    #     # Ensure that you only send these functions NNF formulas
    #     # Literals are compiled to NNF here
    #     print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()