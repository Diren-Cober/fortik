
# Author: Kirill Leontyev (DC)

from collections import deque
from stacks.stack_errs import StackUnderflowException as Underflow



class PipeStack:

    def __init__(self, id):
        self.__drive = deque([])
        self.__id = id
    
    @property
    def id(self):
        return self.__id
    
    def push(self, obj):
        self.__drive.append(obj)
    
    def pop(self):
        if self.__drive.__len__():
            return self.__drive.pop()
        else:
            raise Underflow(self.__id)
    
    def clear(self):
        self.__drive.clear()