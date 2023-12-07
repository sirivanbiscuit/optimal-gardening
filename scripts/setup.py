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

# SET NUMBER OF TIME INTERVALS:
# If this is higher than 10, except much longer solve-time.
# Your average garden should be around 3x3 with several intervals.
# Typically a garden doesn't do anything interesting after about
# 5 or so intervals.
garden_dur = 4

# Initial state to use (from below)
state_select = 2

# INITIAL STATES
# Make some initial states to use. Keep in mind:
# - they must be square
# - the one you use must have the length given above
# - empty cells should have an empty string
# - valid objects: 'C', 'B', 'T', 'P', 'PT', 'R', ''
init_states = {
    # 0: An empty 2x2 garden. This will have one solution for
    # every possible garden configuration: 
    # (6 objects ^ 4 cells) = 1296 solutions
    # If you select select optimal gardening, there will be one
    # solution for every possible 2x2 OPTIMAL garden (372)
    0: [
        ['',''],
        ['','']
    ],
    # 1: A randomly arranged garden. This can be used as a basic
    # test of the model's capabilities with regard to both
    # plant spreading and relationships. (1 sol, 0 optimal sols)
    1: [
        ['T', 'B', 'PT'],
        ['C', 'C', 'P'],
        ['T', 'P', 'PT']
    ],
    # 2: A garden with pine trees lining the left and right edges.
    # This will have countless non-optimal solutions (don't try to find
    # them, it will take ages), however, due to the placement of trees,
    # there will be a much smaller number of optimal ones, each with a 
    # check-like pattern.
    2: [
        ['PT', '', '', 'PT'], 
        ['PT', '', '', 'PT'], 
        ['PT', '', '', 'PT'], 
        ['PT', '', '', 'PT']
    ],
    # 3: A garden with a particularily problematic setup of pine
    # trees. There will be no optimal gardens here, since there is
    # no possible method of keeping the right edge alive while also
    # helping any plant elsewhere.
    3: [
        ['PT', 'B', 'C', ''], 
        ['P', 'C', 'PT', ''], 
        ['T', 'C', 'PT', ''], 
        ['PT', 'T', 'C', '']
    ]
    # ... add more!
}


"""
DO NOT CHANGE THE BELOW LINES.
All the model exploration may be done with the values above.
"""
from scripts.garden import create_garden
from scripts.propositions import GardenPlot

if garden_dur < 2:
    raise ValueError("The selected garden duration must more than one")

elif garden_dur > 99:
    raise ValueError("The selected garden duration must be less than one hundred")

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
ind = 1
for row in inits[1:]:
    if len(row)!=prev_l or ind==prev_l:
        raise ValueError("The selected initial config must be a square")
    prev_l = len(row)
    ind+=1
    
# Import these to various files where needed
G = create_garden(len(inits), garden_dur)
INIT = inits