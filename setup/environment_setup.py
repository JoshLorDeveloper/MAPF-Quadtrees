from classes.simple_objects.position import Position
from classes.simple_objects.range import Range
from classes.simple_objects.shape import Shape
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

    # create optimal path defined by agent max speed
    def get_agent_default_paths(self, agent_initializer: AgentInitializer):
        delta_x = agent_initializer.end_position.get_x() - agent_initializer.start_position.get_x()
        delta_y = agent_initializer.end_position.get_y() - agent_initializer.start_position.get_y()
        path_angle = math.atan(delta_y/delta_x)

        distance_per_time_step = agent_initializer.max_speed * self.time_step

        position_array = [agent_initializer.start_position]
        # active position defines the last position added to position array
        active_position = agent_initializer.start_position
        while agent_initializer.start_position.get_x() < active_position.get_x() < agent_initializer.end_position.get_x() \
                or agent_initializer.end_position.get_x() < active_position.get_x() < agent_initializer.start_position.get_x():
            distance_x = math.cos(path_angle)*distance_per_time_step
            distance_y = math.sin(path_angle)*distance_per_time_step
            new_position = Position(active_position.get_x() + distance_x, active_position.get_y() + distance_y, -1)
            position_array.append(new_position)
            active_position = new_position
