
# Author: Leontyev Kirill (DC)



class VM:

    # Ref:
    #   state:          frt_core.state.State
    #   builtins:       dict<str, () -> none>
    #   input:          list<str>
    #   inp_index:      int
    #   output:         deque<() -> none>
    #   parse:          () -> optional<tuple<bool, str>>
    #   execute:        ...
    #   read:           (int) -> str
    #   write:          (str) -> int
    #   reset_stacks:   () -> none
    #   reset_state:    () -> none

    __slots__ = (
        'state', 'builtins', 'input', 'inp_index', 'code', 'localization',
        'parse', 'execute', 'read', 'write', 'reset_stacks', 'reset_state'
    )

    # Ref: (frt_core.state.State, frt_localization.locale.Locale, (int) -> str, (str) -> none) -> VM
    @classmethod
    def from_save(cls, state, localization, read, write):
        self = object.__new__(cls)
        self.state = state
        self.localization = localization

        from frt_bootstrap.boot_builtins import generate_builtins, generate_vm_dependent_builtins
        builtins = generate_builtins(state)
        self.__init__(state, state.num_stack, state.ret_stack, builtins, read, write)
        builtins.update(generate_vm_dependent_builtins(self))

        return self

    # Locale = frt_localization.locale.Locale
    # Ref: (int, str, int, str, Coder, int, bool, bool, bool, (int) -> str, (str) -> none, Locale) -> VM
    @classmethod
    def from_args(
        cls, ns_size, ns_cell_type, rs_size, rs_cell_type,
        coder, debug_code, do_disable_gc, do_compile_deep,
        do_block_keyboard_interrupt, read, write,
        localization
    ):
        self = object.__new__(cls)

        from frt_core.stack import Stack
        from frt_core.cf_stack import ControlFlow_stack
        num_stack = Stack(ns_cell_type, ns_size, 'Стек арифметики')
        ret_stack = Stack(rs_cell_type, rs_size, 'Стек возвратов')
        cfl_stack = ControlFlow_stack('Стек управления')

        from frt_core.debugging import Debugger
        debugger = Debugger(debug_code, write)

        from frt_core.state import State
        state = State(
            num_stack, ret_stack, cfl_stack, coder, debugger,
            do_disable_gc, do_compile_deep, do_block_keyboard_interrupt
        )
        self.state = state
        self.localization = localization

        from frt_bootstrap.boot_builtins import generate_vm_dependent_builtins
        self.__init__(state, num_stack, ret_stack, state.words, read, write)
        state.words.update(generate_vm_dependent_builtins(self))

        return self


    # State = frt_core.state.State
    # Stack = frt_core.stack.Stack
    # Builtins = dict<str, frt_core.words.Builtin_word>
    # Ref: (State, Stack, Stack, Builtins, (int) -> str, (str) -> none) -> none
    def __init__(self, state, num_stack, ret_stack, builtins, read, write):

        from collections import deque

        _input = list()
        self.input = _input
        self.code = deque()

        ns_clear = num_stack.clear
        rs_clear = ret_stack.clear
        st_words_clear = state.words.clear
        st_words_update = state.words.update

        def _reset_stacks():
            ns_clear()
            rs_clear()

        def _reset_state():
            ns_clear()
            rs_clear()
            st_words_clear()
            st_words_update(builtins)

        #self.parse = _parse
        #self.execute = _execute
        self.read = read
        self.write = write
        self.reset_stacks = _reset_stacks
        self.reset_state = _reset_state
