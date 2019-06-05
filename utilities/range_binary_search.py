from range import Range
from position import Position


# Use principles of binary search to find upper and lower indexes of search time range

# gives the indexes of lowbound below search_time_range, and highbound below search_time_range high_bound
# returns -1 if does not exist in time range
def recursive_search(low, high, search_time_range, sorted_array, recursive_call=False):

    # check if this is the first call of recursive call function
    if not recursive_call:
        # check for existence in time range, if not we return that element can not be found
        contains_low_bound_val = get_value(low, sorted_array)

        contains_high_bound_val = get_value(high, sorted_array)

        if search_time_range.up_bound < contains_low_bound_val or search_time_range.low_bound > contains_high_bound_val:
            return -1

    # check if the time of midpoint index of high and low is inside the search time range
    mid_point = (low + high) // 2
    temp_val = get_value(mid_point, sorted_array)
    temp_difference = search_time_range.difference(temp_val)
    if temp_difference == 0:
        # if the mid_point is inside the search time range we must recursively search for the lowbound on the
        # smaller side of the midpoint and the high bound on the larger side of the midpoint
        low = low_bound(low, mid_point, search_time_range.low_bound, sorted_array)
        high = high_bound(mid_point, high, search_time_range.up_bound, sorted_array)
        return Range(low, high)
    elif low >= high:
        # if entire search time range is between two positions we must return the lower of the two positions
        # for both low bound and highbound
        temp_val = get_value(low, sorted_array)
        # ensure that low bound starts at a point that it at or beneath the lowbound of the search time range
        if temp_val <= search_time_range.low_bound:
            return Range(low, low)
        else:
            return Range(low - 1, low - 1)
    elif temp_difference == -1:
        # if the midpoint is below the range search above the midpoint
        return recursive_search(mid_point + 1, high, search_time_range, sorted_array, True)
    elif temp_difference == 1:
        # if the midpoint is above the range search below the midpoint
        return recursive_search(low, mid_point - 1, search_time_range, sorted_array, True)


# so that time range of model can change while model is running
# look for the index equivalent to below or equal to the ranges lowbound
def low_bound(low, high, range_low_bound, sorted_array):
    mid_point = (low + high) // 2
    temp_val = get_value(mid_point, sorted_array)

    # ensure that the returned index is less than or equal to the lowbound
    if low >= high:
        if range_low_bound >= temp_val:
            return mid_point
        else:
            return mid_point - 1
    if range_low_bound == temp_val:
        # if low bound is the exact current midpoint then return current midpoint
        return mid_point
    elif range_low_bound > temp_val:
        # if range lowbound is above the current midpoint look in range above the current midpoint for lowbound
        return low_bound(mid_point + 1, high, range_low_bound, sorted_array)
    elif range_low_bound < temp_val:
        # if range lowbound is below the current midpoint look in range below the current midpoint for lowbound
        return low_bound(low, mid_point - 1, range_low_bound, sorted_array)


# so that time range of model can change while model is running
# look for the index equivalent to below or equal to the ranges upbound
def high_bound(low, high, range_up_bound, sorted_array):
    mid_point = (low + high) // 2
    temp_val = get_value(mid_point, sorted_array)

    # ensure that the returned index is less than or equal to the upbound
    if low >= high:
        if range_up_bound > temp_val:
            return mid_point
        else:
            return mid_point - 1
    if range_up_bound == temp_val:
        # if upbound is the exact current midpoint then return current midpoint
        return mid_point - 1
    elif range_up_bound > temp_val:
        # if range upbound is above the current midpoint look in range above the current midpoint for upbound
        return high_bound(mid_point + 1, high, range_up_bound, sorted_array)
    elif range_up_bound < temp_val:
        # if range upbound is below the current midpoint look in range below the current midpoint for upbound
        return high_bound(low, mid_point - 1, range_up_bound, sorted_array)


def get_value(index, sorted_array):
    # get time value at index, regardless of if sorted array is of positions or directly times
    temp = sorted_array[index]
    if isinstance(temp, Position):
        temp = temp.get_time()
    return temp
