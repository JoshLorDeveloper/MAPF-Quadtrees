from classes.simple_objects.position import Position
from classes.simple_objects.range import Range
from classes.simple_objects.shape import Shape
from classes.agent_source.agent import Agent
import math


# class for defining creation of obstacles or restricted areas
class ObstacleInitializer:

    def __init__(self, position: Position, shape: Shape):
        self.position = position
        self.shape = shape


# class for defining creation of agents, from start and end position
class AgentInitializer:

    def __init__ (self, start_position:Position, end_position:Position, shape:Shape, max_speed):
        self.start_position = start_position
        # end position should not have a defined time
        self.end_position = end_position
        self.shape = shape
        # max speed is in unites of time step
        self.max_speed = max_speed


# class for defining creation of enviroment that agents will operate in
class Environment:

    def __init__(self, range_x: Range, range_y: Range, time_step, start_time = 0, obstacle_initializers: [ObstacleInitializer] = None,
                 agent_initializers: [AgentInitializer] = None):
        self.range_x = range_x
        self.range_y = range_y
        self.time_step = time_step
        self.start_time = start_time

        if obstacle_initializers is None:
            self.obstacle_initializers = []
        else:
            self.obstacle_initializers = obstacle_initializers

        if agent_initializers is None:
            self.agent_initializers = []
        else:
            self.agent_initializers = agent_initializers

    def get_obstacles(self):
        obstacles = []
        for obstacle_initializer in self.obstacle_initializers:
            obstacle_position = obstacle_initializer.get_position()
            obstacle_position.set_time(-1)
            temp_obstacle = Agent(obstacle_position, obstacle_initializer.shape, is_restricted_area=True)
            obstacles.append(temp_obstacle)

    # get array of agents from agent initializers
    def get_agents(self):
        agents = []
        for agent_initializer in self.agent_initializers:
            agent_positions = self.get_agent_default_positions(agent_initializer)
            temp_agent = Agent(agent_positions, agent_initializer.shape, is_restricted_area=False)
            agents.append(temp_agent)

        return agents

    # get positions in optimal path for agent defined by agent max speed
    def get_agent_default_positions(self, agent_initializer: AgentInitializer):
        delta_x = agent_initializer.end_position.get_x() - agent_initializer.start_position.get_x()
        delta_y = agent_initializer.end_position.get_y() - agent_initializer.start_position.get_y()
        path_angle = math.atan(delta_y/delta_x)

        # get the distance that the agent will move in each time step, to define the distance between its positions
        distance_per_time_step = agent_initializer.max_speed * self.time_step
        distance_x = math.cos(path_angle) * distance_per_time_step
        distance_y = math.sin(path_angle) * distance_per_time_step

        # time for current position
        temp_time = agent_initializer.start_position.get_time()

        # store positions to be returned as agents path
        position_array = []
        # active position defines the next position to be added to array
        active_position = agent_initializer.start_position
        # loop until moved past end position and add all appropriate positions
        while agent_initializer.start_position.get_x() < active_position.get_x() < agent_initializer.end_position.get_x() \
                or agent_initializer.end_position.get_x() < active_position.get_x() < agent_initializer.start_position.get_x():
            position_array.append(active_position)
            # increment time by time_step to get time for the next position
            temp_time = temp_time + self.time_step
            active_position = Position(active_position.get_x() + distance_x, active_position.get_y() + distance_y, temp_time)

        # calculate agent end position time
        last_position = position_array[-1]
        time_to_end_position = ((agent_initializer.end_position.get_x() - last_position.get_x())/distance_x) * self.time_step
        agent_initializer.end_position.set_time(temp_time + time_to_end_position - self.time_step)

        # ensure add last position to array
        position_array.append(agent_initializer.end_position)
        return position_array
