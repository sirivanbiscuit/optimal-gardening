from propositions import GardenPlot, Fenced

def create_garden(length: int, duration: int) -> dict:
    """
    Creates a square garden grid of the given length containing 
    all necessary propositions in all available cells.\n
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
    
    # universals
    time_map['u'] = [
        [Fenced(x,y) for y in range(length)] 
            for x in range(length)
    ]
    
    # gardens in each time interval
    for t in range(duration):
        time_map[t] = [
            [GardenPlot(x,y,t) for y in range(length)] 
            for x in range(length)
        ]
        
    return time_map