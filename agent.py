from position import Position
from range import Range
from shape import Shape
from indexed_dictionary import PositionIndexedDictionary
from utilities import range_binary_search


# function to define key for sorting of positions
def positions_time(val):
    return val.get_time()

# sort positions in ascending order by time
def sort_positions(positions: [Position]):
    positions.sort(key=positions_time)
    return positions


# check for collision in 3d space, between agent as defined by array of positions and shape
# and rectangular prism space created by the range variables
def three_dimensional_collision(range_x: Range, range_y: Range, range_time: Range, position_sublist: [Position], shape):
    for i in range(0, len(position_sublist) - 1):
        if shape.is_colliding(position_sublist[i], position_sublist[i + 1], range_x, range_y, range_time):
            return True
    return False


class Agent:

    # define agent pased on array of positiosn and shape
    def __init__(self, positions: [Position], shape: Shape):
        # sort positions into ascending time order, note: this may not be needed if parameter already passes sorted list
        sorted_positions = sort_positions(positions)

        # define start and target positions for agent, start position will stay unchanged
        # but target position may change in time

        self.start_position = sorted_positions[0]
        self.target_position = sorted_positions[-1]
        # REMEMBER TO CHANGE TIME RANGE IF PATH CHANGED
        self.time_range = Range(self.start_position.get_time(), self.target_position.get_time())
        self.shape = shape

        # define positions indexed dictionary. A dictionary where the key is a positions time and the value is the list
        # of quadtree_node parents for that agent in the time range between the key position and the next position. It
        # is important to note that the sorted array used for indexing stores position objects not position's time's.
        self.position_indexed_dictionary = PositionIndexedDictionary(sorted_positions)

    # returns array of sorted position from position indexed dictionary
    def get_positions(self):
        return self.position_indexed_dictionary.get_sorted_positions()

    # add quadtree parent in position indexed dictionary for each index in the index range
    def add_quadtree_parent(self, quadtree_node_parent, index_range: Range):
        if index_range != - 1:
            for index in range(index_range.low_bound, index_range.up_bound + 1):  # need +1 because not inclusive
                self.position_indexed_dictionary.add_tree_for_index(index, quadtree_node_parent)

    # remove quadtree parent in position indexed dictionary by searching for index range of positions in time range
    # and removing the specified quadtree parent for each index in index range
    def remove_quadtree_parent(self, quadtree_node_parent, range_time: Range):
        # chec if only a single index must be found, if so find it
        if range_time.low_bound in self.position_indexed_dictionary.dict:
            if range_time.size() <= self.position_indexed_dictionary.time_step:
                self.position_indexed_dictionary.remove_tree_for_time(range_time.low_bound, quadtree_node_parent)
                return
        # find neccassarry indexes to loop through, and for each index remove the specified quadtree parent
        range_indexes = self.search_positions_in_range(range_time)
        if range_indexes != - 1:
            for index in range(range_indexes.low_bound, range_indexes.up_bound + 1):  # need +1 because not inclusive
                self.position_indexed_dictionary.remove_tree_for_index(index, quadtree_node_parent)

    def get_shape(self):
        return self.shape

    # check if agent is in a quadtree_node
    def is_in(self, quadtree_node):
        range_x = quadtree_node.range_x
        range_y = quadtree_node.range_x
        range_time = quadtree_node.time_range
        # get indexes of common times between agents and quadtree node
        index_range = self.search_positions_in_range(range_time)
        if index_range == -1:
            return False

        # if agent is in quadtree node for these indexes
        # then we can say that for these indexes quadtree node is a quadtree parent
        self.add_quadtree_parent(quadtree_node, index_range)

        if self.get_positions()[index_range.up_bound] == quadtree_node.time_range.up_bound:
            # in case of exact ending on upper position we do not need the next position to check for a collision
            position_sublist = self.get_positions()[index_range.low_bound:index_range.up_bound + 1]
        else:
            # we must add two to upper bound as we want the next position when checking if there is a collision
            position_sublist = self.get_positions()[index_range.low_bound:index_range.up_bound + 2]

        # LIKELY NOT NEEDED
        # # check if only one element index index range size
        # if index_range.size() == 0:
        #     # if so we must add two to upper bound as we want the next position when checking if there is a collision
        #     position_sublist = self.get_positions()[index_range.low_bound:index_range.up_bound + 2]
        # else:
        #     # if there are multiple indexes in range only need to be inclusive for last value
        #     position_sublist = self.get_positions()[index_range.low_bound:index_range.up_bound + 1]

        # check if quadtree takes up entire range of space at that time in which case there is no need to check geometry
        if quadtree_node.root:
            return True
        else:
            # check if agent is colliding in 3d space with quadtree parent
            return three_dimensional_collision(range_x, range_y, range_time, position_sublist, self.get_shape())

    def search_positions_in_range(self, search_time_range):
        # search for indexes of positions in time range with default setting of full array length
        array_length = len(self.get_positions())
        return range_binary_search.recursive_search(0, array_length - 1, search_time_range, self.get_positions())
