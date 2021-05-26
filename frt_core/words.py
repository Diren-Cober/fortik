
# Author: Kirill Leontyev (DC)



class Builtin_word:

    # Ref: () -> none
    __slots__ = '__call__'

    # Ref: (() -> none) -> none
    def __init__(self, impl):
        self.__call__ = impl.__call__



class VMProxy_word(Builtin_word):
    __slots__ = ()



class Derived_word:

    # Ref:
    #   w_code:         iterable<tuple<object, ...>>
    #   __call__:       () -> none

    __slots__ = ('w_code', '__call__')

    # State = frt_core.state.State
    # Compiled = iterable<tuple<object, ...>>
    # Opcodes = frt_bootstrap.boot_optags.get_optags.Opcodes
    # Ref: (iterable<tuple<object, ...>>, State, (Compiled, Opcodes) -> none) -> none
    def __init__(self, code, execute, opcodes):
        self.w_code = code
        self.__call__ = lambda: execute(code, opcodes)
