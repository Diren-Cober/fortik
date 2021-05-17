
# Author: Kirill Leontyev (DC)



class Builtin_word:

    # Ref: (frt_core.machine.VM) -> none
    __slots__ = '__call__'

    # Ref: (() -> none) -> none
    def __init__(self, impl):
        self.__call__ = lambda ignored: impl()



class Builtin_control_word:

    # Ref: (frt_core.machine.VM) -> none
    __slots__ = '__call__'

    # Ref: (() -> none) -> none
    def __init__(self, impl):
        self.__call__ = impl



class Derived_word:

    # Ref:
    #   w_code:         iterable<(frt_core.machine.VM) -> none>     // tuple, in fact.
    #   __call__:       (frt_core.machine.VM) -> none

    __slots__ = ('w_code', '__call__')

    # Ref: (iterable<() -> none>) -> none   // tuple, in fact.
    def __init__(self, code, state):

        self.w_code = code

        state_ret_stack_push = state.ret_stack.push
        state_ret_stack_pop = state.ret_stack.pop
        state_code_stack_push = state.code_stack.append
        state_code_stack_pop = state.code_stack.pop

        # Ref: (frt_core.machine.VM) -> none
        def _call(vm):
            state_ret_stack_push(state.instruction_index + 1)
            state_code_stack_push(state.current_program)
            state.instruction_index = 0
            state.current_program = self.w_code

            vm.execute()

            state.instruction_index = state_ret_stack_pop()
            state.current_program = state_code_stack_pop()

        self.__call__ = _call
