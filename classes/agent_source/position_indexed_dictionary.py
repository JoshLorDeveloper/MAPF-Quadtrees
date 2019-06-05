from classes.simple_objects.position import Position


class PositionIndexedDictionary:

    # elements is a sorted array of positions
    def __init__(self, elements: [Position]):
        # each position is represents the position to the position after it
        self.sorted_positions = elements.copy()
        self.dict = {}
        # initialize last time and time step to show that variables are not yet initialized
        last_time = -1
        self.time_step = -1

        for position in self.sorted_positions:
            # see if there is a constant time step between positions, and calculate it
            if not self.time_step == -2 and last_time >= 0:
                if self.time_step == -1:
                    self.time_step = position.get_time() - last_time
                else:
                    if not self.time_step == position.get_time() - last_time:
                        self.time_step = -2
            # initialize dictionary to coordinate with sorted positions,
            # but key is not position just the time of the position
            last_time = position.get_time()
            self.dict[position.get_time()] = []

    def get_sorted_positions(self):
        return self.sorted_positions

    def add_tree_for_index(self, index, octree_node_parent):
        return self.add_tree_for_time(self.sorted_positions[index].get_time(), octree_node_parent)

    def add_tree_for_position(self, position: Position, octree_node_parent):
        return self.add_tree_for_time(position.get_time(), octree_node_parent)

    def add_tree_for_time(self, time, octree_node_parent):
        # ensure that time is in dictionary and octree_node_parent has not already been added at time
        if time in self.dict and octree_node_parent not in self.dict[time]:
            self.dict[time].append(octree_node_parent)
            return True
        else:
            return False

    def remove_tree_for_index(self, index, octree_node_parent):
        return self.remove_tree_for_time(self.sorted_positions[index].get_time(), octree_node_parent)

    def remove_tree_for_position(self, position: Position, octree_node_parent):
        return self.remove_tree_for_time(position.get_time(), octree_node_parent)

    def remove_tree_for_time(self, time, octree_node_parent):
        # if time and octree node parent exists remove octree_node_parent
        if time in self.dict:
            time_array = self.dict[time]
            if octree_node_parent in time_array:
                time_array.remove(octree_node_parent)
                return True
            else:
                return False
        else:
            return False

    def get_tree_for_position(self, position: Position):
        return self.get_tree_for_time(position.get_time())

    def get_tree_for_time(self, time):
        return self.dict[time]

    def add_item(self, position: Position):
        self.sorted_positions.append(position)
