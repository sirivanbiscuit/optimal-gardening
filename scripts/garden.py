from scripts.propositions import GardenPlot

def create_garden(length: int, duration: int) -> dict:
    """
    Creates a square garden grid of the given length containing 
    all necessary propositions in all available cells.\n
    This grid will be forcibly surrounded on all sides by rocks
    to make constraints easier. Thus, the actual array length will
    be length+2.\n
    A dictionary will be formed containing a map of all gardens for
    each relevant time interval.\n
    The dictionary will also contain a key "u" containing an array
    similiar in size to the garden but containing only propositions
    universal to all time intervals.

    Args:
        length (int): the length of the square garden grid.
        duration (int): the number of time intervals.
    """
    time_map = {}
    total_len = length+2
    
    # universals
    time_map['u'] = [] # this is unused, but kept to keep the code working
    
    # gardens in each time interval
    for t in range(duration):
        time_map[t] = []
        for x in range(total_len):
            row = []
            for y in range(total_len):
                row.append(GardenPlot(x,y,t))
            time_map[t].append(row)
        
    return time_map