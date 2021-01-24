
# Author: Kirill Leontyev (DC)

from stacks.stack_errs import StackOverflowException as Overflow
from stacks.stack_errs import StackUnderflowException as Underflow



class Stack:

    def __init__(self, max_depth, id):
        self.__drive = []
        self.__limit = max_depth
        self.__id = id
    
    @property
    def id(self):
        return self.__id
    
    @property
    def limit(self):
        return self.__limit
    
    def push(self, obj):
        if self.__drive.__len__() < self.limit:
            self.__drive.append(obj)
        else:
            raise Overflow(self.__id)
    
    def pop(self):
        if self.__drive.__len__():
            return self.__drive.pop()
        else:
            raise Underflow(self.__id)

    def depth(self):
        return self.__drive.__len__()
    
    def dup(self):
        if self.__drive.__len__():
            if self.__drive.__len__() < self.limit:
                tmp = self.__drive.pop()
                self.__drive.append(tmp)
                self.__drive.append(tmp)
            else:
                raise Overflow(self.__id)
        else:
            raise Underflow(self.__id)
    
    def swap(self):
        if self.__drive.__len__() > 1:
            self.__drive.append(self.__drive.pop(-2))
        else:
            raise Underflow(self.__id)
    
    def rot(self):
        if self.__drive.__len__() > 1:
            self.__drive = self.__drive[1:] + self.__drive[0]
    
    def clear(self):
        self.__drive = []
    
    def __str__(self):
        return str(self.__drive)