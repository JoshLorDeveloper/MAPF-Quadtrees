

class Position:

    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time

    # use getter and setter methods to prevent error later in development
    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def get_time(self):
        return self.time

    def set_time(self, time):
        self.time = time