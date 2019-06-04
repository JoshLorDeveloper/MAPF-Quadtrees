from position import Position
from collections import deque


class TimeSortedDictionary:

    # elements is a sorted array of positions
    # turn on should use deque if more times in modal change than agents are going to be added
    def __init__(self, time_step=0.5, should_use_deque=False):
        self.time_step = time_step
        self.should_use_deque = should_use_deque
        if not self.should_use_deque:
            # list is kept in reverse order as there will be more changes to the front of the list than the rear
            self.ordered_times = []
        else:
            # use deque if more changes to start of array then middle
            self.ordered_times = deque()
        self.dict = {}
        # initialize start and end time to -1 to signify that they have not been det
        self.start_time = -1
        self.end_time = -1

    # return ordered times in ascending order, this requires reversing the list if it is reversed
    def get_ordered_times(self):
        if not self.should_use_deque:
            temp_times = self.ordered_times.copy()
            temp_times.reverse()
            return temp_times
        else:
            return list(self.ordered_times)

    # get dictionary value by index, uses ordered times get by index, and uses that as key in dictionary
    def dict_index(self, index):
        if index >= len(self.ordered_times):
            print("error index greater than ordered times lengths")
            return
        if self.should_use_deque:
            return self.dict[self.ordered_times[index]]
        else:
            dict_key = self.ordered_times[len(self.ordered_times) - 1 - index]
            return self.dict[dict_key]

    # change start time of model creating quadtree nodes if it is before current start, and deleting quadtree nodes if
    # it is after current start
    def change_start_time(self, new_start_time, new_quad_tree_node):
        # in special case of model not having start and end times initialized yet set start and end times are set and
        # first end time at this start time is created
        if self.start_time == -1 and self.end_time == -1:
            self.start_time = new_start_time
            self.end_time = new_start_time
            if self.should_use_deque:
                self.ordered_times.appendleft(new_start_time)
            else:
                self.ordered_times.append(new_start_time)
            self.dict[new_start_time] = new_quad_tree_node(new_start_time)
            return

        # store start time to calculate time changes
        old_start_time = self.start_time
        if new_start_time > self.end_time:
            print("error start time is greater than end time")
            return

        # calculate difference to see how many quadtrees must be created
        diff = self.end_time - new_start_time

        # if difference is multiple of time step then use that start time, otherwise make it multiple on larger side
        if diff % self.time_step == 0:
            self.start_time = new_start_time
        else:
            # recalculate difference
            diff = (((diff // self.time_step) + 1) * self.time_step)
            # calculate new start time from difference
            self.start_time = self.end_time - diff

        # if start time did not change than we don't need to do anything
        if self.start_time == old_start_time:
            return
        # if start time has increased  then we must remove unnecessary quadtrees
        if self.start_time > old_start_time:
            for index in range(0, round((self.start_time - old_start_time)/self.time_step)):
                # remember that ordered times are backwards if not deque
                # and hence must remove from opposite size as is natural
                if self.should_use_deque:
                    self.ordered_times.popleft()
                else:
                    self.ordered_times.pop()
                self.dict.pop(old_start_time + index * self.time_step, None)
        else:
            # if start time decreased then we must add needed quadtrees
            for index in range(1, round((old_start_time - self.start_time)/self.time_step) + 1):
                # remember that ordered times are backwards if not deque
                # and hence must add from opposite size as is natural

                # calculate the time that should be added
                temp_time = old_start_time - index * self.time_step
                if self.should_use_deque:
                    self.ordered_times.appendleft(temp_time)
                else:
                    self.ordered_times.append(temp_time)
                # set dictionary time as well to maintain dictionary
                self.dict[temp_time] = new_quad_tree_node(temp_time)

    # change end time of model creating quadtree nodes if it is after current end, and deleting quadtree nodes if
    # it is before current end
    def change_end_time(self, new_end_time, new_quad_tree_node):
        # store old end time
        old_end_time = self.end_time
        if new_end_time < self.start_time:
            print("error end time is smaller than start time")
            return

        # calculate difference between end time and start time
        diff = new_end_time - self.start_time

        # calculate new difference going towards larger end time, if not already multiple of difference
        if diff % self.time_step == 0:
            self.end_time = new_end_time
        else:
            # recalculate difference
            diff = (((diff // self.time_step) + 1) * self.time_step)
            # calculate new end time from difference
            self.end_time = self.start_time + diff

        # if end time time has decreased then we must remove unnecessary quadtrees
        if self.end_time < old_end_time:
            for index in range(0, round((old_end_time - self.end_time)/self.time_step) + 1):
                # remember that ordered times are backwards if not deque
                # and hence must remove from opposite size as is natural
                if self.should_use_deque:
                    self.ordered_times.pop()
                else:
                    self.ordered_times.pop(0)
                self.dict.pop(old_end_time - index * self.time_step, None)
        else:
            # if end time increased then we must add needed quadtrees
            for index in range(1, round((self.end_time - old_end_time)/self.time_step)):
                # remember that ordered times are backwards if not deque
                # and hence must add from opposite size as is natural
                temp_time = old_end_time + index * self.time_step
                if self.should_use_deque:
                    self.ordered_times.append(temp_time)
                else:
                    self.ordered_times.insert(0, temp_time)
                # set dictionary time as well to maintain dictionary
                self.dict[temp_time] = new_quad_tree_node(temp_time)


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
