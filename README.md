# CISC204 G2 Model Project: Optimal Gardening
This is the repository for Group 2's modelling project. This project aims to be a
rudimentary gardening simulator which uses logical constraints and models to 
display a virtual garden across multiple time intervals. 
* Note: the most up-to-date version of this project is in `main`. Make sure you are there.

### How to Build a Garden
* `setup.py` contains a handful of initialization code to help the user set up a garden.
There are a variety of examples already in the file. Gardens must be a square grid, and must contain
some amount of the valid plants listed. The user must also set the number of time intervals
they wish the garden to progress over.

### Garden Progression
* At any given time, a plant in the garden is either alive or dead. All plants may be helpful
or harmful to a nearby plant. If a plant is harmed by others nearby, it will die on the next
time interval unless another helps it.
* There are four primary plant types, plus pine trees. Each plant type has a unique set of
plants that it may help or harm, as well as a direction in which these effects will be carried
out. For example, a Corn plant will help a Bean plant that is above or below it. Figure 1 below
outlines the relationships between all plants.
* If a plant dies, living plants nearby may spread into its cell, overriding it. A plant created
by spreading will remain alive for at least one time interval before being potentially harmed by
others around it. If there are multiple plants surrounding a dead one, the plant
with the _best_ relationship with the dead one will override it. Plants may not override themselves.
For example, if a dead Pepper plant is adjacent to a Tomato plant, Pepper plant, and Bean Plant, the
cell will be overridden by a Tomato plant on the next time interval.

#### Figure 1: Basic Plant Relationships
![image](https://github.com/sirivanbiscuit/optimal-gardening/assets/89672212/2287ea8e-c0a0-4011-b44d-f470220130a8)

### Solving a Garden
* Running `run.py` in docker will allow the user to "solve" a garden. A "solution" to a garden setup
will be all possible subsequent gardens of future time intervals, given a certain initial configuration
in `setup.py`. There is an option to print the solution as a series of visual grid representations, or as a list
of propositions.
* **Optimal Gardens** are solutions to a garden setup in which, after some amount of time intervals, all
plants in all cells in the garden will stay alive indefinitely.
* **Immediate Optimal Gardens** are solutions to a setup in which all plants across _all_ time intervals will
be alive. The user may indicate, after running `run.py`, whether they want to solve for optimal, immediate, or
non-optimal gardens.

### File Structure
* `run.py` and the `documents` folder are in their standard locations.
* The `documents/final` folder also contains a PDF of a gardening wiki doc for this project. This may be
used as a guide to get better explanations of the constraints and features of the virtual garden.
* The `scripts` folder contains class/method files used in the logic execution. 
Note that the logic execution itself is done with `run.py`

### How to Run
1. Have Docker installed and running in the background.
2. Go to the project folder and run 
`docker run -it -v "FOLDER PATH HERE":/PROJECT cisc204 /bin/bash`
(Assuming you are on Windows).
3. Run `python3 run.py` in the docker terminal.
