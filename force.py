from vector import Vector


class Force:

    def __init__(self, priority, distance_vector: Vector):
        # priority over other forces, will generally be the same value for most forces
        self.priority = priority
        # vector with direction and magnitude
        self.distance_vector = distance_vector
