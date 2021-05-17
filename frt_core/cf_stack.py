
# Author: Kirill Leontyev (DC)

from collections import deque

from frt_core.stack import Stack_underflow



# Some of this class' methods are defined with use of experimental optimization: folding closure.
# The idea is to cache globals, drive's and their methods and to link them as closures.
#
# The speedup is confirmed with use of 'timeit'.

class ControlFlow_stack:

    # Ref:  drive:      deque
    #       name:       str
    #       push:       (int, int, int, (int, int) -> int) -> optional<overflow>
    #       drop:       () -> optional<underflow>
    #       __str__:    () -> str

    __slots__ = ('drive', 'name', 'push', 'drop', '__str__')

    # Ref: (int, str) -> none
    def __init__(self, name):
        self.drive = deque()
        self.name = name

        self_drive_append = self.drive.append
        self_drive_pop = self.drive.pop

        g_list = list
        list_str = list.__str__

        # Ref: (int, int, int, (int, int) -> int) -> optional<overflow>
        def _push(start, lim, step, act):
            self_drive_append( [start, lim, step, act] )

        # Ref: () -> optional<underflow>
        def _drop():
            try:
                self_drive_pop()
            except IndexError:
                raise Stack_underflow(name)

        # Ref: () -> str
        def _stringify():
            return list_str(g_list(self.drive))

        self.push = _push
        self.drop = _drop
        self.__str__ = _stringify

    # Ref: () -> none
    def clock(self):
        try:
            upper_cell = self.drive[-1]
            upper_cell[0] += upper_cell[2]
        except IndexError:
            raise Stack_underflow(self.name)

    # Ref: (int) -> none
    def clock_plus(self, val):
        try:
            upper_cell = self.drive[-1]
            upper_cell[0] += val
        except IndexError:
            raise Stack_underflow(self.name)

    # Ref: () -> bool
    def compare(self):
        try:
            upper_cell = self.drive[-1]
            return upper_cell[3](upper_cell[0], upper_cell[1])
        except IndexError:
            raise Stack_underflow(self.name)
