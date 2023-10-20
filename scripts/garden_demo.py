"""
This is a functional script for playing around with the 'optimal garden'
mechanics that this project will be trying to model. Build the garden
below and execute this file to find out more about it.

Valid plants are:
P -> pine tree
t -> tomatoes
p -> peppers
b -> beans
c -> corn

Happy gardening!!!
"""

# Build a garden out of chars from above:
GARDEN = [
    ['P', 't', 'P'],
    ['t', 'p', 't'],
    ['P', 't', 'P']
]


"""
These below print your results. Dont change them, or else the demo will not 
function properly. Only mess with the GARDEN grid above.
"""

# Does plant 1 help plant 2 grow?
def helps(plant_1: chr, plant_2: chr) -> bool:
    if plant_1=='t': return plant_2=='p'
    elif plant_1=='p': return plant_2=='t'
    elif plant_1=='b': return plant_2=='c'
    elif plant_1=='c': return plant_2=='b'
    else: return False


# Does plant 1 kill plant 2?
def kills(plant_1: chr, plant_2: chr) -> bool:
    if plant_1=='P': return plant_2!='P'
    elif plant_1=='t': return plant_2=='c' or plant_2=='t'
    elif plant_1=='c': return plant_2=='t' or plant_2=='c'
    elif plant_1=='b': return plant_2=='p' or plant_2=='b'
    elif plant_1=='p': return plant_2=='b' or plant_2=='p'
    else: return False

# Main
if __name__ == "__main__":
    # Epic gardening calculations...
    vecs = [[1,0], [-1,0], [0,1], [0,-1]]
    alive = []
    for x in range(0, len(GARDEN)):
        alive += [[]]
        for y in range(0, len(GARDEN[x])):
            alive[x] += 'a'
            adjs = []
            for vec in vecs:
                try: adjs += [GARDEN[x+vec[0]][y+vec[1]]]
                except IndexError: continue
            for plant in adjs:
                if kills(plant,GARDEN[x][y]): 
                    alive[x][y] = 'd'
                if helps(plant,GARDEN[x][y]):
                    alive[x][y]='a'
                    break

    # Your results!
    print("\nYour Garden:")
    opt = True
    for x in range(0, len(GARDEN)):
        row = ""
        for y in range(0, len(GARDEN[x])):
            row += GARDEN[x][y]+"("+alive[x][y]+")\t"
            if alive[x][y]=='d': opt=False
        print(row)
    print("Your garden is"+(" " if opt else " NOT ")+"an optimal garden.\n")
