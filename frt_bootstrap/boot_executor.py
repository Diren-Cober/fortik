
# Author: Kirill Leontyev (DC)


# State = frt_core.state.State
# Compiled = iterable<tuple<object, ...>>
# Opcodes = frt_bootstrap.boot_optags.get_optags.Opcodes
# Ref:
def get_executor(state, with_debug=False, get_dbg_msg=None, wides_cell=30):

    from frt_core.cf_stack import Stack_underflow
    from frt_core.words import Derived_word

    g_len = len

    st_ns_pop = state.num_stack.pop
    st_ns_push = state.num_stack.push
    st_cfl_push = state.cfl_stack.push
    st_cfl_drop = state.cfl_stack.drop
    st_cfl_clock = state.cfl_stack.clock
    st_cfl_compare = state.cfl_stack.compare
    st_cfl_clock_plus = state.cfl_stack.clock_plus
    st_words__getitem__ = state.words.__getitem__
    st_words__setitem__ = state.words.__setitem__

    # Compiled = iterable<tuple<object, ...>>
    # Opcodes = frt_bootstrap.boot_optags.get_optags.Opcodes
    # Ref:
    def execute(compiled, opcodes):

        i = 0
        lim = g_len(compiled)

        compiled_get = compiled.__getitem__

        while i < lim:
            tag, *others = compiled_get(i)

            if tag is opcodes.push:
                st_ns_push(*others)
                i += 1

            elif tag is opcodes.call:
                callable_word = others[0]
                if callable_word:
                    callable_word()
                else:
                    execute(st_words__getitem__(others[1]), opcodes)
                i += 1

            elif tag is opcodes.move:
                i += others[0]

            elif tag is opcodes.fork:
                i += others[0] if st_ns_pop() else others[1]

            elif tag is opcodes.setup_cycle:
                st_cfl_push(*others)
                i += 1

            elif tag is opcodes.check_cycle:
                if st_cfl_compare():
                    i += 1
                else:
                    st_cfl_drop()
                    i += others[0]

            elif tag is opcodes.clock:
                st_cfl_clock()
                i += others[0]

            elif tag is opcodes.clock_p:
                st_cfl_clock_plus(st_ns_pop())
                while i < lim:
                    tag, *others = compiled_get(i)
                    if tag is opcodes.clock:
                        i += others[0]
                        break
                    i += 1
                else:
                    raise RuntimeError("Unable to modify counter without any cycle.")

            else:
                name, body = others
                st_words__setitem__(name, Derived_word(body, state, execute, opcodes))
                i += 1


    str_format = str.format

    fill_debug_message = str_format("addr={{:05}}\top={{:{}}}\t{{}}", wides_cell).format
    fill_additional_message = str_format("-------------\n\tinfo: {{}}\n-------------", wides_cell).format

    # Compiled = iterable<tuple<object, ...>>
    # Opcodes = frt_bootstrap.boot_optags.get_optags.Opcodes
    # Ref:
    def execute_with_debug(compiled, opcodes):

        i = 0
        lim = g_len(compiled)

        compiled_get = compiled.__getitem__

        while i < lim:
            tag, *others = compiled_get(i)

            if tag is opcodes.push:
                st_ns_push(*others)
                print(fill_debug_message(i, get_dbg_msg('push'), *others))
                i += 1

            elif tag is opcodes.call:
                callable_word, name = others
                print(fill_debug_message(i, get_dbg_msg('call'), str_format("'{}'", name)))
                if callable_word:
                    print(get_dbg_msg('output'), end='')
                    callable_word()
                    print('.\n')
                else:
                    print(fill_additional_message(get_dbg_msg('>word').format(name)))
                    execute_with_debug(st_words__getitem__(name), opcodes)
                    print(fill_additional_message(get_dbg_msg('word>').format(name)))
                i += 1

            elif tag is opcodes.move:
                delta, = others
                print(fill_debug_message(i, get_dbg_msg('move'), delta))
                i += delta

            elif tag is opcodes.fork:
                delta = others[0] if st_ns_pop() else others[1]
                print(fill_debug_message(i, get_dbg_msg('fork'), delta))
                i += delta

            elif tag is opcodes.setup_cycle:
                st_cfl_push(*others)
                print(fill_debug_message(i, get_dbg_msg('cycle'), str_format("{}, {}, {}", *others)))
                i += 1

            elif tag is opcodes.check_cycle:
                print(fill_debug_message(i, get_dbg_msg('cycle?'), *others))
                if st_cfl_compare():
                    print(fill_additional_message(get_dbg_msg('cycle>')))
                    i += 1
                else:
                    st_cfl_drop()
                    print(fill_additional_message(get_dbg_msg('cycle!')))
                    i += others[0]

            elif tag is opcodes.clock:
                st_cfl_clock()
                delta, = others
                print(fill_debug_message(i, get_dbg_msg('clck'), delta))
                i += delta

            elif tag is opcodes.clock_p:
                delta = st_ns_pop()
                try:
                    st_cfl_clock_plus(delta)
                except Stack_underflow:
                    raise RuntimeError("Unable to modify counter without any cycle.")

                print(fill_debug_message(i, get_dbg_msg('clck+'), delta))
                while i < lim:
                    tag, *others = compiled_get(i)
                    if tag is opcodes.clock:
                        i += others[0]
                        break
                    i += 1
                else:
                    raise RuntimeError("Unable to modify counter without any cycle in local scope.")

            else:
                name, body = others
                st_words__setitem__(name, Derived_word(body, state, execute_with_debug, opcodes))
                print(fill_debug_message(i, get_dbg_msg('wdef'), str_format("'{}'", name)))
                i += 1


    return execute_with_debug if with_debug else execute
