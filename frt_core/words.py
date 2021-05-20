
# Author: Kirill Leontyev (DC)



class Builtin_word:

    # Ref: () -> none
    __slots__ = '__call__'

    # Ref: (() -> none) -> none
    def __init__(self, impl):
        self.__call__ = impl.__call__



class Derived_word:

    # Ref:
    #   w_code:         iterable<tuple<object, ...>>
    #   __call__:       () -> none

    __slots__ = ('w_code', '__call__')

    # State = frt_core.state.State
    # Compiled = iterable<tuple<object, ...>>
    # Opcodes = frt_bootstrap.boot_optags.get_optags.Opcodes
    # Ref: (iterable<tuple<object, ...>>, State, (Compiled, Opcodes) -> none) -> none
    def __init__(self, code, state, execute, opcodes):

        self.w_code = code

        st_ret_stack_push = state.ret_stack.push
        st_ret_stack_pop = state.ret_stack.pop
        st_instruction_index = state.instruction_index

        # Ref: () -> none
        def _call():
            st_ret_stack_push(st_instruction_index + 1)
            state.instruction_index = 0

            execute(code, opcodes)

            state.instruction_index = st_ret_stack_pop()

        self.__call__ = _call
