from classes.quadtree_source.quadtree import QuadtreeArray
from classes.simple_objects.position import Position
from classes.simple_objects.shape import Shape
from classes.agent_source.agent import Agent
from classes.simple_objects.range import Range
from setup.environment_setup import Environment


# MAIN FILE. RUN PROJECT FROM THIS FILE.

class CTSP:

    # initialize CTSP with range of space
    def __init__(self, environment: Environment):
        self.range_x = environment.range_x
        self.range_y = environment.range_y
        self.time_step = environment.time_step
        self.quadtree = QuadtreeArray(self.range_x, self.range_y, self.time_step)
        # CHANGE WHEN FINISHED WITH ENVIRONMENT POSITION AGENT CREATION
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

