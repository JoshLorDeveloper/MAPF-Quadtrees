from classes.simple_objects.position import Position
from classes.simple_objects.range import Range
import math

class Shape:

    def __init__(self, degree_lengths):
        # each index of degree_lengths represents the length at degree --> index/len(degree_lengths) * 360
        self.degree_lengths = degree_lengths


    # implement
    def is_colliding(self, position1: Position, position2: Position, range_x: Range, range_y:Range, range_time:Range):
        return True

    # implement <-- use linear approximation from closest 2 degree lengths
    def is_colliding_shape(self, position1: Position, position2: Position, other_shape: 'Shape',
                           other_position1: Position, other_position2: Position):
        return True

    # implement <-- use linear approximation from closest 2 degree lengths
    # position 1 and position 2 are the positions moved between in the time difference
    def get_colliding_distance_vector(self, position1: Position, position2: Position, other_shape: 'Shape',
                           other_position1: Position, other_position2: Position):
        # get the angle between
        angle = math.tan(abs(position1.get_y() - position2.get_y())/abs(position1.get_x() - position2.get_x()))
        return 0
