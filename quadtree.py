from quadtree_node import QuadTreeNode
from agent import Agent
from range import Range
from indexed_dictionary import TimeSortedDictionary
from utilities import range_binary_search


class QuadtreeArray:

    # turn on should use deque if less agents are going to be added than times times in modal change
    def __init__(self, range_x, range_y, time_step=0.5, should_use_deque=False):
        self.range_x = range_x
        self.range_y = range_y
        self.start_time = -1
        self.end_time = -1
        self.time_step = time_step
        self.quad_trees = TimeSortedDictionary(time_step,  should_use_deque)

    # used to create new root quadtree node for specified time
    def new_quad_tree_node(self, time):
        # ensure that time is valid before adding quadtree node
        if self.start_time <= time <= self.end_time and (time - self.start_time) % self.time_step == 0:
            return QuadTreeNode(self.range_x, self.range_y, Range(time, time + self.time_step), root=True)
        else:
            print("error creating quadtree, invalid time")

    def add_agent(self, agent: Agent):
        # update quadtree array time-range, and add new quadtree nodes if needed
        self.update_time(agent)
        # must use get ordered times as ordered times may be stored in reverse order
        ordered_times = self.quad_trees.get_ordered_times()
        # get index range of times in which agent should be added to
        index_range = range_binary_search.recursive_search(0, len(ordered_times) - 1, agent.time_range,
                                                           ordered_times)
        # add agent to quadtrees in index range
        for index in range(index_range.low_bound, index_range.up_bound + 1):
            self.quad_trees.dict_index(index).add_agent(agent)

    def add_agents(self, agents: [Agent]):
        # update quadtree array time range, and add new quadtree nodes if needed
        self.update_times(agents)
        # must use get ordered times as ordered times may be stored in reverse order
        ordered_times = self.quad_trees.get_ordered_times()
        for agent in agents:
            # get index range of times in which agent should be added to
            index_range = range_binary_search.recursive_search(0, len(ordered_times) - 1,
                                                               agent.time_range,
                                                               ordered_times)
            # add agent to quadtrees in index range
            for index in range(index_range.low_bound, index_range.up_bound + 1):
                self.quad_trees.dict_index(index).add_agent(agent)

    # so that time range of model can change while model is running
    def update_time(self, agent: Agent):
        self.update_start_time(agent)
        self.update_end_time(agent)

    def update_times(self, agents: [Agent]):
        self.update_start_times(agents)
        self.update_end_times(agents)

    def update_start_time(self, agent: Agent):
        # change start time if new start time is before current start time
        if self.start_time > agent.time_range.low_bound or self.start_time == -1:
            self.start_time = agent.time_range.low_bound
            # if end time is yet to be initialized initialize it
            if self.end_time == -1:
                self.end_time = self.start_time
            # set start time of quadtree adding quadtree nodes if necessary
            self.quad_trees.change_start_time(self.start_time, self.new_quad_tree_node)

    def update_start_times(self, agents: [Agent]):
        # find smallest value among agents of start time added
        min_value = self.start_time
        for agent in agents:
            if agent.time_range.low_bound < min_value or self.start_time == -1:
                min_value = agent.time_range.low_bound
        # after minimum value has been calculated update start time, if that minimum value is before current start time
        if self.start_time > min_value:
            self.start_time = min_value
            if self.end_time == -1:
                self.end_time = self.start_time
            # set start time of quadtree adding quadtree nodes if necessary
            self.quad_trees.change_start_time(self.start_time, self.new_quad_tree_node)

    def update_end_time(self, agent: Agent):
        # change end time if new end time is after current end time
        if self.end_time < agent.time_range.up_bound or self.end_time == -1:
            self.end_time = agent.time_range.up_bound
            # set end time of quadtree adding quadtree nodes if necessary
            self.quad_trees.change_end_time(self.end_time, self.new_quad_tree_node)

    def update_end_times(self, agents: [Agent]):
        # find largest value among agents of end time added
        max_value = self.end_time
        for agent in agents:
            if agent.time_range.high_bound > max_value or self.end_time == -1:
                max_value = agent.time_range.high_bound
        # after maximum value has been calculated update end time, if that maximum value is after current end time
        if self.end_time < max_value:
            self.end_time = max_value
            # set end time of quadtree adding quadtree nodes if necessary
            self.quad_trees.change_end_time(self.end_time, self.new_quad_tree_node)

    def print_modal(self):
        for index, time in enumerate(self.quad_trees.get_ordered_times()):
            print(str(time) + " : " + str(self.quad_trees.dict_index(index).agents))
