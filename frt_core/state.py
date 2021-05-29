
# Author: Kirill Leontyev (DC)



class State:

    # Ref:
    #   num_stack:          Stack
    #   aux_stack:          Stack
    #   cfl_stack:          CF_stack
    #   words:              dict<str, frt_core.words.Word>
    #   coder:              frt_encoding.coder.Coder
    #   debugger:           optional<frt_core.debugging.Debugger>
    #   <flags>:            bool; bool; bool
    #   repr_words:         () -> str
    #   __str__:            () -> str

    __slots__ = (
        'num_stack', 'aux_stack', 'cfl_stack', 'words', 'coder', 'debugger',
        'do_disable_gc', 'do_compile_deep', 'do_block_keyboard_interrupt',
        'repr_words', '__str__'
    )

    # Stack = frt_core.stack.Stack
    # CF_stack = frt_core.cf_stack.ControlFlow_stack
    # Coder = frt_encoding.coder.Coder
    # Debugger = frt_core.debugging.Debugger
    # Ref: (
    #   Stack, Stack, CF_stack, Coder, Debugger, bool, bool, bool
    # ) -> none
    def __init__(
            self,
            num_stack, aux_stack, cfl_stack, coder, debugger,
            do_disable_gc, do_compile_deep, do_block_keyboard_interrupt
    ):
        from collections import deque
        from frt_bootstrap.boot_builtins import generate_builtins

        self.num_stack = num_stack
        self.aux_stack = aux_stack
        self.cfl_stack = cfl_stack

        self_words = generate_builtins(self)
        self.words = self_words
        self.coder = coder
        self.debugger = debugger

        self.do_disable_gc = do_disable_gc
        self.do_compile_deep = do_compile_deep
        self.do_block_keyboard_interrupt = do_block_keyboard_interrupt

        g_map = map
        g_max = max
        g_len = len
        g_list = list
        g_range = range
        g_deque = deque
        str_join = str.join
        str_format = str.format
        list_len = list.__len__
        deque_append = deque.append
        self_words_keys = self_words.keys
        self_num_stack_name = num_stack.name
        self_ret_stack_name = aux_stack.name
        self_num_stack_limit = num_stack.limit
        self_ret_stack_limit = aux_stack.limit

        # Ref: () -> str
        def _repr_words():

            sl_words = g_list(self_words_keys())
            cell_width = g_max(g_map(g_len, sl_words)) + 1
            n_cells = 100 // cell_width
            w_len = list_len(sl_words)
            res = g_deque()

            i = 0
            for i in g_range(n_cells, w_len, n_cells):
                deque_append(
                    res, str_format(
                        str_format("{{:{}}}", cell_width) * n_cells, *(sl_words[(i - n_cells):i])
                    )
                )
            else:
                deque_append(
                    res, str_format(
                        str_format("{{:{}}}", cell_width) * (w_len - i), *(sl_words[i:])
                    )
                )

            return str_join("\n", res)

        # Ref: () -> str
        def _stringify():
            return str_format(
                "\tТекущее состояние системы{}",
                str_join("\n", [
                    "\n\n\tСтеки",
                    str_format(
                        "{}:\t\t{}\n\tПредел: {}",
                        self_num_stack_name, num_stack, self_num_stack_limit
                    ),
                    " ---------------------------------------",
                    str_format(
                        "{}:\t\t{}\n\tПредел: {}",
                        self_ret_stack_name, aux_stack, self_ret_stack_limit
                    ),
                    " ---------------------------------------",
                    "Стек плавающей арифметики:\t<в разработке>\n\n\tТекстовый буфер\n<в разработке>",
                    str_format("\n\tТекущий словарь\n{}", self.repr_words())
                ])
            )

        self.repr_words = _repr_words
        self.__str__ = _stringify
