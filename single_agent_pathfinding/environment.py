from classes.simple_objects.position import Position
from classes.simple_objects.range import Range
from classes.simple_objects.shape import Shape


class Obstacle:

    def __init__(self, position: Position, shape: Shape):
        self.position = position
        self.shape = shape


class Environment:

    def __init__(self, range_x: Range, range_y: Range, obstacles: [Obstacle]):
        self.range_x = range_x
        self.range_y = range_y
        self.obstacles = obstacles
