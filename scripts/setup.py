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

garden_len = 1 # Length of the garden
garden_dur = 1 # Number of time intervals

state_select = 1 # Initial state to use (set below)

# Make some initial states to use. Keep in mind:
# - they must be square
# - the one you use must have the length given above
# - empty cells should have an empty string
# - valid plants: 'C', 'B', 'T', 'P', 'PT', ''
# - put an 'f' after a plant to fence it, ex. 'Tf'
init_states = {
    0: [
        ['P', 'C', 'C'],
        ['C', 'C', 'P'],
        ['C', 'T', 'C']
    ],
    1: [
        ['PT']
    ],
    2: []
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
char_map, valid_map, row_l = init_states[state_select], True, 0
for row in char_map:
    row_l += 1
    if len(row)!=garden_len: valid_map = False
    for char in row:
        if char not in valid: valid_map = False
if row_l!=garden_len: valid_map = False

if not valid_map:
    raise ValueError("The selected initial config is invalid")
    
    
# Import these to various files where needed
G = create_garden(garden_len, garden_dur)
INIT = init_states[state_select]