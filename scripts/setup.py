"""
This is an initialization file for the garden to be "solved".
To play around with the logic model, this should be the only script
you need to alter. Gardens are "solved" as follows:
- You provide a size, duration, and initial state of the garden.
- The solver in run.py will find a "solution" to all proceeding intervals,
  that is, all the propositions of those intervals. The model comprising
  these propositions will describe every cell of every interval, taking
  into account all garden growth mechanics.
- Each garden should obtain exactly one solution. If there are more, 
  something is wrong with the program.
"""

garden_dur = 3 # Number of time intervals

state_select = 0 # Initial state to use (set below)

# Make some initial states to use. Keep in mind:
# - they must be square
# - the one you use must have the length given above
# - empty cells should have an empty string
# - valid plants: 'C', 'B', 'T', 'P', 'PT', ''
init_states = {
    0: [
        ['P', 'PT', 'C'],
        ['C', 'C', 'P'],
        ['C', 'T', 'C']
    ],
    1: [
        ['PT']
    ],
    2: [],
    3: [
        ['PT', '', ''],
        ['', '', ''],
        ['', '', '']
    ],
    # ... add more!
}


"""
DO NOT CHANGE THE BELOW LINES.
All the model exploration may be done with the values above.
"""
from scripts.garden import create_garden
from scripts.propositions import GardenPlot

if garden_dur < 1:
    raise ValueError("The selected garden duration must be postive")

if state_select not in init_states: 
    raise ValueError("The selected initial config doesn't exist")

valid = GardenPlot.PLANTS + GardenPlot.PLANTS_F
inits = init_states[state_select]
for row in inits:
    for char in row:
        if char not in valid:
            raise ValueError("The selected initial config has invalid plants")

if not len(inits): 
    raise ValueError("The selected initial config must have non-zero area")

prev_l = len(inits[0])
for row in inits[1:]:
    if len(row)!=prev_l: 
        raise ValueError("The selected initial config must be a square")
    prev_l = len(row)
    
# Import these to various files where needed
G = create_garden(len(inits), garden_dur)
INIT = inits