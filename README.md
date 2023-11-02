# CISC204 G2 Model Project: Optimal Gardening
This is the repository for Group 2's modelling project. This project aims to
model a garden within a grid that houses a variety of plants and structures.
Plants within the garden will either thrive or die based on their surroundings
as well as various other factors. The goal of our modelling procedures will be to 
determine the properties and occurences of an "optimal garden", that is, a garden 
in which all plants are able to thrive.

### File Structure
* `run.py`, `test.py`, and the `documents` folder are in their standard locations.
* The `misc` folder contains temporary templates and interactive scripts (i.e. to 
help visualize a certain garden layout).
* The `scripts` folder contains class/method files used in the logic execution. 
Note that the logic execution itself is done with `run.py`

### How to Run
1. Have Docker installed and running in the background.
2. Go to the project folder and run 
`docker run -it -v "FOLDER PATH HERE":/PROJECT cisc204 /bin/bash`
(Assuming you are on Windows).
3. Run `python3 run.py` in the docker terminal.
