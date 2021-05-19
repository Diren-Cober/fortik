
# Author: Kirill Leontyev (DC)

from array import array



class Stack_overflow(Exception):
    pass

class Stack_underflow(Exception):
    pass



# Attention: logic of this class' methods may be not obvious.
# The class uses statically typed array of fixed length, array's end considered to be stack's bottom.
# Normally self.__nfree is the top element index [0..self.__limit); when self.__nfree == self.__limit,
# .. the stack is empty.
# High used trick: self.__nfree attribute is cached in self__nfree variable, due to int class immutability,
# .. self__nfree still holds the old value after incrementation or decrementation of self.__nfree,
# .. so, self__nfree may point to either just freed, or under-current-top cell.

class Stack:

    # Ref:  __drive:    array<i*>, * = {8|16|32|64}
    #       __nfree:    int
    #       limit:      int
    #       name:       str

    __slots__ = ('__drive', '__nfree', 'limit', 'name', '__str__')

    # Ref: (str, int, str) -> none
    def __init__(self, type_tag, max_depth, name):
        self.__drive = array(type_tag)
        self.__drive.extend([0 for _ in range(max_depth)])
        self.__nfree = max_depth
        self.limit = max_depth
        self.name = name

        g_list = list
        list_str = g_list.__str__
        left_bound = max_depth - 1
        self__drive = self.__drive

        # Time benefit of optimization below confirmed with use of 'timeit'.

        # Ref: () -> str
        def _stringify():
            return list_str(g_list(self__drive[left_bound:self.__nfree + (-1):-1]))

        self.__str__ = _stringify


    # Ref: (int) -> optional<overflow>
    def push(self, val):

        if self.__nfree:
            self.__nfree -= 1
            self.__drive[self.__nfree] = val
        else:
            raise Stack_overflow(self.name)

    # Ref: () -> optional<underflow>
    def pop(self):
        self__nfree = self.__nfree
        if self__nfree < self.limit:
            self.__nfree += 1
            return self.__drive[self__nfree]
        else:
            raise Stack_underflow(self.name)


    # Built-in words' implementations...

    # Ref: () -> optional<overflow>
    def depth(self):
        self__nfree = self.__nfree
        if self__nfree:
            self.__nfree -= 1
            self.__drive[self.__nfree] = self.limit - self__nfree
        else:
            raise Stack_overflow(self.name)

    # Ref: () -> optional<union<underflow, overflow>>
    def dup(self):
        self__nfree = self.__nfree
        if self__nfree:
            if self__nfree < self.limit:
                self.__nfree -= 1
                self.__drive[self.__nfree] = self.__drive[self__nfree]
            else:
                raise Stack_underflow(self.name)
        else:
            raise Stack_overflow(self.name)

    # Ref: () -> optional<union<underflow, overflow>>
    def if_dup(self):
        self__nfree = self.__nfree
        if self__nfree < self.limit:
            top = self.__drive[self__nfree]
            if top:
                if self__nfree:
                    self.__nfree -= 1
                    self.__drive[self.__nfree] = top
                else:
                    raise Stack_overflow(self.name)
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<union<underflow, overflow>>
    def nif_dup(self):
        self__nfree = self.__nfree
        if self__nfree < self.limit:
            top = self.__drive[self__nfree]
            if not top:
                if self__nfree:
                    self.__nfree -= 1
                    self.__drive[self.__nfree] = top
                else:
                    raise Stack_overflow(self.name)
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<union<underflow, overflow>>
    def dup_two(self):
        self__nfree = self.__nfree
        if self__nfree:
            if self__nfree < self.limit - 1:
                self__drive = self.__drive
                self.__nfree -= 2
                self__drive[self__nfree - 1] = self__drive[self__nfree + 1]
                self__drive[self.__nfree] = self__drive[self__nfree]
            else:
                raise Stack_underflow(self.name)
        else:
            raise Stack_overflow(self.name)

    # Ref: () -> optional<union<underflow, overflow>>
    def dup_three(self):
        self__nfree = self.__nfree
        if self__nfree:
            if self__nfree < self.limit - 2:
                self__drive = self.__drive
                self.__nfree -= 3
                self__drive[self__nfree - 1] = self__drive[self__nfree + 2]
                self__drive[self__nfree - 2] = self__drive[self__nfree + 1]
                self__drive[self.__nfree] = self__drive[self__nfree]
            else:
                raise Stack_underflow(self.name)
        else:
            raise Stack_overflow(self.name)

    # Ref: () -> optional<union<underflow, overflow, runtime_error>>
    def n_dup(self):
        self__nfree = self.__nfree
        if self__nfree < self.limit:
            self__drive = self.__drive
            n = self__drive[self__nfree]
            self.__nfree += 1
            if n > 0:
                if self__nfree > n:
                    self__nfree_pn = self__nfree + n
                    for i in range(n):
                        self__drive[self__nfree - i] = self__drive[self__nfree_pn - i]
                    self.__nfree -= n
                else:
                    raise Stack_overflow(self.name)
            else:
                raise RuntimeError(self.name)
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<underflow>
    def drop(self):
        if self.__nfree < self.limit:
            self.__nfree += 1
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<underflow>
    def if_drop(self):
        if self.__nfree < self.limit:
            if self.__drive[self.__nfree]:
                self.__nfree += 1
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<underflow>
    def nif_drop(self):
        if self.__nfree < self.limit:
            if not self.__drive[self.__nfree]:
                self.__nfree += 1
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<underflow>
    def drop_two(self):
        if self.__nfree < self.limit - 1:
            # We just forget about values written in 'dropped' cells.
            # They will be overwritten later...
            self.__nfree += 2
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<underflow>
    def drop_three(self):
        if self.__nfree < self.limit - 2:
            self.__nfree += 3
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<union<underflow, runtime_error>>
    def n_drop(self):
        self__nfree = self.__nfree
        if self__nfree < self.limit:
            n = self.__drive[self__nfree]
            self.__nfree += 1
            if n > 0:
                if self__nfree < self.limit - n:
                    self.__nfree += n
                else:
                    Stack_underflow(self.name)
            else:
                raise RuntimeError(self.name)
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<underflow>
    def swap(self):
        self__nfree = self.__nfree
        if self__nfree < self.limit - 1:
            self__drive = self.__drive
            self__nfree_p1 = self__nfree + 1
            self__drive[self__nfree_p1], self__drive[self__nfree] = self__drive[self__nfree], self__drive[self__nfree_p1]
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<union<underflow, runtime_error>>
    def n_swap(self):
        self__nfree = self.__nfree
        if self__nfree < self.limit:
            self__drive = self.__drive
            n = self.__drive[self__nfree]
            self.__nfree += 1
            if n > 0:
                n2 = n * 2
                if self__nfree < self.limit - n2:
                    self__nfree = self.__nfree
                    self__nfree_pn = self__nfree + n
                    for i in range(n):
                        il = self__nfree + i
                        ir = self__nfree_pn + i
                        self__drive[ir], self__drive[il] = self__drive[il], self__drive[ir]
            else:
                raise RuntimeError(self.name)
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<underflow>
    def rot(self):
        self__nfree = self.__nfree
        self__nfree_p2 = self__nfree + 2
        if self__nfree_p2 < self.limit:
            self__drive = self.__drive
            third = self__drive[self__nfree_p2]
            self__drive[self__nfree_p2] = self__drive[self__nfree + 1]
            self__drive[self__nfree + 1] = self__drive[self__nfree]
            self__drive[self__nfree] = third
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<union<underflow, runtime_error>>
    def n_rot(self):
        self__nfree = self.__nfree
        if self__nfree < self.limit:
            self__drive = self.__drive
            n = self__drive[self__nfree]
            self.__nfree += 1
            if n > 0:
                if n < self.limit - self__nfree:
                    n_th = self__drive[self__nfree + n]
                    for i in range(self__nfree + n, self.__nfree, -1):
                        self__drive[i] = self__drive[i - 1]
                    self__drive[self.__nfree] = n_th
                else:
                    raise Stack_underflow(self.name)
            else:
                raise RuntimeError(self.name)
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<underflow>
    def rot_whole(self):
        self__nfree = self.__nfree
        if self__nfree < self.limit:
            self__drive = self.__drive
            tmp = self__drive[-1]
            for i in range(self.limit - 1, self__nfree, -1):
                self__drive[i] = self__drive[i - 1]
            self__drive[self__nfree] = tmp
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<union<underflow, overflow>>
    def under(self):
        self__nfree = self.__nfree
        if self__nfree < self.limit - 1:
            if self__nfree:
                self.__nfree -= 1
                self.__drive[self.__nfree] = self.__drive[self__nfree + 1]
            else:
                raise Stack_overflow(self.name)
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<union<underflow, overflow>>
    def under_under(self):
        self__nfree = self.__nfree
        if self__nfree < self.limit - 2:
            if self__nfree:
                self.__nfree -= 1
                self.__drive[self.__nfree] = self.__drive[self__nfree + 2]
            else:
                raise Stack_overflow(self.name)
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<union<underflow, runtime_error>>
    def pick(self):
        self__nfree = self.__nfree
        if self__nfree < self.limit:
            self__drive = self.__drive
            n = self__drive[self__nfree]
            self.__nfree += 1
            if n > 0:
                if n < self.limit - self.__nfree:
                    self.__nfree -= 1
                    self__drive[self__nfree] = self__drive[self.__nfree + n]
                else:
                    raise Stack_underflow(self.name)
            else:
                raise RuntimeError(self.name)
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<underflow>
    def drop_first(self):
        self__nfree = self.__nfree
        if self__nfree < self.limit - 1:
            self.__nfree += 1
            self.__drive[self.__nfree] = self.__drive[self__nfree]
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<underflow>
    def drop_second(self):
        self__nfree = self.__nfree
        if self__nfree < self.limit - 2:
            self__drive = self.__drive
            self.__nfree += 2
            self__drive[self.__nfree] = self__drive[self__nfree + 1]
            self__drive[self__nfree + 1] = self__drive[self__nfree]
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> optional<union<underflow, runtime_error>>
    def drop_nth(self):
        self__nfree = self.__nfree
        if self.__nfree < self.limit:
            self__drive = self.__drive
            n = self__drive[self__nfree]
            self.__nfree += 1
            if n > 0:
                if n < self.limit - self.__nfree:
                    for i in range(self__nfree + n, self__nfree, -1):
                        self__drive[i + 1] = self__drive[i]
                    self.__nfree += 1
                else:
                    raise Stack_underflow(self.name)
            else:
                raise RuntimeError(self.name)
        else:
            raise Stack_underflow(self.name)

    # Ref: () -> none
    def invert_top(self):
        self.__drive[self.__nfree] = ~self.__drive[self.__nfree]

    # Ref: () -> none
    def negate_top(self):
        self.__drive[self.__nfree] *= -1

    # Ref: () -> none
    def increment_top(self):
        self.__drive[self.__nfree] += 1

    # Ref: () -> none
    def decrement_top(self):
        self.__drive[self.__nfree] -= 1

    # Ref: () -> optional<overflow>
    def push_one(self):
        if self.__nfree:
            self.__nfree -= 1
            self.__drive[self.__nfree] = 1
        else:
            raise Stack_overflow(self.name)

    # Ref: () -> optional<overflow>
    def push_zero(self):
        if self.__nfree:
            self.__nfree -= 1
            self.__drive[self.__nfree] = 0
        else:
            raise Stack_overflow(self.name)


    # Ref: () -> none
    def clear(self):
        self.__nfree = self.limit
