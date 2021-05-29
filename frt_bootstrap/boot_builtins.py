
# Author: Kirill Leontyev (DC)

from frt_core.words import Builtin_word



# Ref: (frt_core.state.State) -> dict<str, frt_core.words.Builtin_word>
def generate_builtins(st):

    # Ref: ((any, any) -> any) -> (any, any) -> int
    def wrap_int(func):
        return lambda a, b: int(func(a, b))

    # Ref: ((any, any) -> any) -> (any, any) -> int
    def wrap_bool_int(func):
        return lambda a, b: int(func(bool(a), bool(b)))

    # Ref: ((int, int) -> int, frt_core.state.State) -> () -> none
    def make_n_binop(func, state):
        ns = state.num_stack
        ns_pop = ns.pop
        ns_push = ns.push

        # Ref: () -> none
        def word():
            top = ns_pop()
            ns_push(func(ns_pop(), top))

        return word

    # Ref: ((int, int) -> int, frt_core.state.State) -> () -> none
    def make_r_binop(func, state):
        rs = state.aux_stack
        rs_pop = rs.pop
        rs_push = rs.push

        # Ref: () -> none
        def word():
            top = rs_pop()
            rs_push(func(rs_pop(), top))

        return word

    st_ns = st.num_stack
    st_rs = st.aux_stack

    g_int = int
    g_bool = bool

    g_int__add__ = g_int.__add__
    g_int__sub__ = g_int.__sub__
    g_int__lt__int = wrap_int(g_int.__lt__)
    g_int__gt__int = wrap_int(g_int.__gt__)
    g_int__eq__int = wrap_int(g_int.__eq__)
    g_int__ne__int = wrap_int(g_int.__ne__)

    return {
        '+'     : Builtin_word(make_n_binop(g_int__add__, st)),
        '-'     : Builtin_word(make_n_binop(g_int__sub__, st)),
        '*'     : Builtin_word(make_n_binop(g_int.__mul__, st)),
        '/'     : Builtin_word(make_n_binop(g_int.__floordiv__, st)),
        '%'     : Builtin_word(make_n_binop(g_int.__mod__, st)),
        '-1*'   : Builtin_word(st_ns.negate_top),
        '**'    : Builtin_word(make_n_binop(g_int.__pow__, st)),
        '<<'    : Builtin_word(make_n_binop(g_int.__lshift__, st)),
        '>>'    : Builtin_word(make_n_binop(g_int.__rshift__, st)),
        '!'     : Builtin_word(st_ns.invert_top),
        '&'     : Builtin_word(make_n_binop(g_int.__and__, st)),
        '|'     : Builtin_word(make_n_binop(g_int.__or__, st)),
        '^'     : Builtin_word(make_n_binop(g_int.__xor__, st)),
        '1+'    : Builtin_word(st_ns.increment_top),
        '1-'    : Builtin_word(st_ns.decrement_top),
        '<'     : Builtin_word(make_n_binop(g_int__lt__int, st)),
        '<='    : Builtin_word(make_n_binop(wrap_int(g_int.__le__), st)),
        '>'     : Builtin_word(make_n_binop(g_int__gt__int, st)),
        '>='    : Builtin_word(make_n_binop(wrap_int(g_int.__ge__), st)),
        '=='    : Builtin_word(make_n_binop(g_int__eq__int, st)),
        '!='    : Builtin_word(make_n_binop(g_int__ne__int, st)),

        'ложь'      : Builtin_word(st_ns.push_zero),
        'правда'    : Builtin_word(st_ns.push_one),
        'не'        : Builtin_word(make_n_binop(wrap_bool_int(g_bool.__invert__), st)),
        'и'         : Builtin_word(make_n_binop(wrap_bool_int(g_bool.__and__), st)),
        'или'       : Builtin_word(make_n_binop(wrap_bool_int(g_bool.__or__), st)),
        'либо'      : Builtin_word(make_n_binop(wrap_bool_int(g_bool.__xor__), st)),

        'удвоить'               : Builtin_word(st_ns.dup),
        '?-удвоить'             : Builtin_word(st_ns.if_dup),
        'не-?-удвоить'          : Builtin_word(st_ns.nif_dup),
        '2-удвоить'             : Builtin_word(st_ns.dup_two),
        '3-удвоить'             : Builtin_word(st_ns.dup_three),
        'эн-удвоить'            : Builtin_word(st_ns.n_dup),
        'сбросить'              : Builtin_word(st_ns.drop),
        '?-сбросить'            : Builtin_word(st_ns.if_drop),
        'не-?-сбросить'         : Builtin_word(st_ns.nif_drop),
        '2-сбросить'            : Builtin_word(st_ns.drop_two),
        '3-сбросить'            : Builtin_word(st_ns.drop_three),
        'эн-сбросить'           : Builtin_word(st_ns.n_drop),
        'обменять'              : Builtin_word(st_ns.swap),
        'эн-обменять'           : Builtin_word(st_ns.n_swap),
        '3-провернуть'          : Builtin_word(st_ns.rot),
        'эн-провернуть'         : Builtin_word(st_ns.n_rot),
        'провернуть-полностью'  : Builtin_word(st_ns.rot_whole),
        'достать-первый'        : Builtin_word(st_ns.under),
        'достать-второй'        : Builtin_word(st_ns.under_under),
        'достать-энный'         : Builtin_word(st_ns.pick),
        'вынуть-первый'         : Builtin_word(st_ns.drop_first),
        'вынуть-второй'         : Builtin_word(st_ns.drop_second),
        'вынуть-энный'          : Builtin_word(st_ns.drop_nth),
        'очистить'              : Builtin_word(st_ns.clear),
        'измерить'              : Builtin_word(st_ns.depth),

        'в_+'   : Builtin_word(make_r_binop(g_int__add__, st)),
        'в_-'   : Builtin_word(make_r_binop(g_int__sub__, st)),
        'в_<'   : Builtin_word(make_r_binop(g_int__lt__int, st)),
        'в_>'   : Builtin_word(make_r_binop(g_int__gt__int, st)),
        'в_=='  : Builtin_word(make_r_binop(g_int__eq__int, st)),
        'в_!='  : Builtin_word(make_r_binop(g_int__ne__int, st)),
        'в_1+'  : Builtin_word(st_rs.increment_top),
        'в_1-'  : Builtin_word(st_rs.decrement_top),

        'в_поместить'       : Builtin_word(lambda: st_rs.push(st_ns.pop())),
        'в_вернуть'         : Builtin_word(lambda: st_ns.push(st_rs.pop())),
        'в_удвоить'         : Builtin_word(st_rs.dup),
        'в_?-удвоить'       : Builtin_word(st_rs.if_dup),
        'в_не-?-удвоить'    : Builtin_word(st_rs.nif_dup),
        'в_сбросить'        : Builtin_word(st_rs.drop),
        'в_?-сбросить'      : Builtin_word(st_rs.if_drop),
        'в_не-?-сбросить'   : Builtin_word(st_rs.nif_drop),
        'в_2-обменять'      : Builtin_word(st_rs.swap),
        'в_эн-обменять'     : Builtin_word(st_rs.n_swap),
        'в_3-провернуть'    : Builtin_word(st_rs.rot),
        'в_эн-провернуть'   : Builtin_word(st_rs.n_rot),
        'в_достать-первый'  : Builtin_word(st_rs.under),
        'в_достать-энный'   : Builtin_word(st_rs.pick),
        'в_измерить'        : Builtin_word(st_rs.depth),
    }



# Builtin = frt_core.words.Builtin_word
# Builtin_control = frt_core.words.Builtin_control_word
# Ref: (frt_core.machine.VM) -> dict<str, union<Builtin, Builtin_control>>
def generate_vm_dependent_builtins(vm):

    st = vm.state
    vm_read = vm.read
    vm_write = vm.write
    st_ns_pop = st.num_stack.pop
    st_ns_push = st.num_stack.push
    st_cdr_decode = st.coder.decode
    st_cdr_encode = st.coder.encode

    return {
        'вывести_число'     : Builtin_word(lambda: vm_write(str(st_ns_pop()))),
        'вывести_символ'    : Builtin_word(lambda: vm_write(st_cdr_decode(st_ns_pop()))),
        'вывести_пробел'    : Builtin_word(lambda: vm_write(' ')),
        'вывести_символ_нс' : Builtin_word(lambda: vm_write('\n')),
        'вывести_строку'    : None,     # ...string in machine's memory, according to number on the top of the num stack.
        'вывести_текст'     : None,     # ...compile-time constant.
# счётчик, счётчик+
        'считать_символ'    : Builtin_word(lambda: st_ns_push(st_cdr_encode(vm_read(1)))),
        'считать_строку'    : None,     # ...string from ostream, length described by number on the top of the num stack.
        'считать_текст'     : None,     # ...all readable input.
    }

    # UNDER COMMENT: the words used in parsing, not in execution.
    # The reason: unlike classic Forth, fortik has no compilation mode,
    # .. providing programmer with ability to (re-)define words conditionally;
    # .. maybe, this 'metaprogramming' will be improved in future versions...
    #
    #   ':'             - word_def
    #   ';'             - word_def-limiter
    #   'если'          - fork
    #   'сделать'       - fork-limiter
    #   'пока'          - loop_whl
    #   'повторять'     - loop_whl-limiter
    #   'для'           - loop_for
    #   'с_шагом'       - loop_for-step-tag
    #   'выполнять'     - loop_for-limiter
