
# Author: Kirill Leontyev (DC)

from stacks.stack import Stack
from stacks.pipe_stack import PipeStack
from core.dictionary import system_dictionary

from collections import deque
import sys



class State:

    @staticmethod
    def __cond_init_stack(val: int, stack_id: str):
        if val < 0 or val > sys.maxsize:
            raise ValueError('Недопустимая величина для размера стека \'' + stack_id + '\': ' + str(val))
        else:
            return Stack(val, stack_id)

    def __init__(self, max_num_stack_depth: int, max_nested_calls: int, coder, debug: int):
        self.__debug = debug
        self.__i = 0
        if debug:   self.__opc = 0  # ops counter
        self.__i_free = True

        self.__num_stack = State.__cond_init_stack( max_num_stack_depth, 'Стек арифметики' )
        self.__ret_stack = State.__cond_init_stack( max_nested_calls, 'Стек возвратов' )
        self.__prc_stack = PipeStack('Стек ветвлений')

        self.__words = {}
        self.__words.update(system_dictionary)

        self.__coder = coder
        self.__text_buff = deque([])
    

    @property
    def ns(self):
        return self.__num_stack
    
    @property
    def rs(self):
        return self.__ret_stack
    
    @property
    def ps(self):
        return self.__prc_stack
    
    @property
    def ws(self):
        return self.__words
    
    @property
    def tb(self):
        return self.__text_buff
    
    @property
    def dg(self):
        return self.__debug
    
    @property
    def i(self):
        return self.__i
    
    @i.setter
    def i(self, num: int):
        if num < 0:
            raise TypeError('Системная ошибка: смещение за нулевую инструкцию')
        elif self.__i_free:
            self.__i = num
            self.__i_free = False
    
    def i_unlck(self):
        self.__i_free = True
    
    @property
    def opc(self):
        if self.__debug:
            tmp = self.__opc
            self.__opc += 1
            return tmp

    def encode(self, symb: str):
        return self.__coder.encode(symb)
    
    def decode(self, code: int):
        return self.__coder.decode(code)
    
    def reset_counters(self):
        self.__i = 0
        self.__i_free = True
        if self.__debug:    self.__opc = 0
    
    def reset_stacks(self):
        self.__num_stack.clear()
        self.__ret_stack.clear()
        self.__prc_stack.clear()
    
    def reset_whole(self):
        self.__num_stack.clear()
        self.__ret_stack.clear()
        self.__prc_stack.clear()
        self.__words.clear()
        self.__words.update(system_dictionary)
        self.__text_buff.clear()
        self.__i = 0
        self.__i_free = True
        self.__opc = 0
    
    def __str__(self):
        res = "\tТекущее состояние системы"
        res += "\n\n\tСтеки"
        res += "\nСтек арифметики: {}".format(self.__num_stack)
        res += "\n\tПредел: {}".format(self.__num_stack.limit)
        res += "\n -------------------------"
        res += "\nСтек возвратов: {}".format(self.__ret_stack)
        res += "\n\tПредел: {}".format(self.__ret_stack.limit)
        res += "\n -------------------------"
        res += "\nДоступ к стеку ветвлений закрыт"
        res += "\n\n\tТекстовый буфер"
        res += "\nСредства работы с текстовым буфером в разработке"
        res += "\n\n\tТекущй словарь\n{}".format(list(self.__words.keys()))
        return res
