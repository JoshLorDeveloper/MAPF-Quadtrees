from classes.quadtree import QuadtreeArray
from classes.functionless.position import Position
from classes.shape import Shape
from classes.agent import Agent
from classes.range import Range


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

