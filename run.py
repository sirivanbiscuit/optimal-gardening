from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from nnf import config
from scripts.propositions import Plant

# Setup logic
config.sat_backend = "kissat" # fast SAT-solver
from scripts.setup import ENC # Encoder

# Setup propositions
Pine = Plant("Pine")
Bean = Plant("Bean")   
Tomato = Plant("Tomato")
Corn = Plant("Corn")
Peppers = Plant("Peppers")
Empty = Plant("Empty")
#Alive = BasicPropositions("Alive")
#Harmed = BasicPropositions("Harmed")


# this could be moved somewhere else
def example_theory():
    # Add custom constraints by creating formulas with the variables you created. 
    ENC.add_constraint((Pine & Bean) >> Harmed)
    # Implication
    ENC.add_constraint(Empty >> ~Alive)
    # Negate a formula
    ENC.add_constraint(~(x & y))

    return ENC


if __name__ == "__main__":

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    #T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    #print("\nSatisfiable: %s" % T.satisfiable())
    #print("# Solutions: %d" % count_solutions(T))
    #print("   Solution: %s" % T.solve())

    #print("\nVariable likelihoods:")
    #for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
    #    print(" %s: %.2f" % (vn, likelihood(T, v)))
    #print()

    #grid = grid_creation(4,4)