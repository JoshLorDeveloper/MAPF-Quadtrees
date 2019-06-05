class Range:

    THRESHOLD = 5

    def __init__(self, low_bound, up_bound):
        self.low_bound = low_bound
        self.up_bound = up_bound
        if self.low_bound > self.up_bound:
            print("warning range low bound is greater than up bound")

    def contains(self, num):
        # check if range contains number
        if self.low_bound < num < self.up_bound:
            return True
        return False

    def difference(self, num):
        # check if number is contained in the range, above range up bound or below range low bound
        if self.low_bound <= num <= self.up_bound:
            return 0
        elif num > self.up_bound:
            return 1
        elif num < self.low_bound:
            return -1
        return 0

    def contains_range(self, other_range: 'Range'):
        # check if range contains other range
        if self.low_bound < other_range.low_bound < self.up_bound \
                or self.low_bound < other_range.up_bound < self.up_bound:
            return True
        return False

    def split(self, first_second: int):
        # split range in half into two sub ranges either returning the larger sub range or smaller subrange
        if first_second == 1:
            # first
            return Range(self.low_bound, (self.low_bound + self.up_bound)/2)
        else:
            # second
            return Range((self.low_bound + self.up_bound) / 2, self.up_bound)

    def size(self):
        return self.up_bound - self.low_bound
