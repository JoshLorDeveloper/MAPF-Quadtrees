from quadtree import QuadtreeArray
from position import Position
from shape import Shape
from agent import Agent
from range import Range
import Visualization.main


# MAIN FILE. RUN PROJECT FROM THIS FILE.

class CTSP:

    # initialize CTSP with range of space
    def __init__(self, range_x: Range, range_y: Range):
        self.range_x = range_x
        self.range_y = range_y
        self.quadtree = QuadtreeArray(range_x, range_y)
        self.agents = []

    def add_agent(self, agent: Agent):
        self.agents.append(agent)
        self.quadtree.add_agent(agent)

    # create new agent from position array and shape
    def add_agent_from_positions(self, positions_parameter: [Position], shape: Shape):
        agent = Agent(positions_parameter, shape)
        self.add_agent(agent)

    def get_agents(self):
        return self.agents

    def print_modal(self):
        self.quadtree.print_modal()


side_distance = 5
# array of positions of vertices for shape in order of x0, y0, x1, y1... where 0,0 is the center of the shape
shape_vertices = [-1 * side_distance,
                  -1 * side_distance,
                  side_distance,
                  -1 * side_distance,
                  side_distance,
                  side_distance,
                  -1 * side_distance,
                  side_distance]

# initialize model
model = CTSP(Range(0, 400), Range(0, 400))

# initialize arrays of positions for different agents
positions = []
for i in range(60, 20 - 1, -1):
    positions.append(Position(i + 300, i + 200, 80 - i))
model.add_agent_from_positions(positions, Shape(shape_vertices))

positions = []
for i in range(30, 50 + 1):
    positions.append(Position(i, i, i))
model.add_agent_from_positions(positions, Shape(shape_vertices))

positions = []
for i in range(10, 70 + 1):
    positions.append(Position(i, i + 100, i))
model.add_agent_from_positions(positions, Shape(shape_vertices))

# print out basic model information
model.print_modal()

# visualize model
Visualization.main.run_model(model, show_start=True, show_destination=True)
