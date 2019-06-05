from classes.functionless.position import Position
from classes.range import Range


class Shape:

    def __init__(self, shape_vertices):
        self.shape_vertices = shape_vertices

    # implement
    def is_colliding(self, position1: Position, position2: Position, range_x: Range, range_y:Range, range_time:Range):
        return True

    # implement
    def is_colliding_shape(self, position1: Position, position2: Position, other_shape: 'Shape',
                           other_position1: Position, other_position2: Position):
        return True
