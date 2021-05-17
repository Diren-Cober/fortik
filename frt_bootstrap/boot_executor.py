
# Author: Kirill Leontyev (DC)


# State = frt_core.state.State
# Compiled = iterable<tuple<object, ...>>
# Opcodes = frt_bootstrap.boot_optags.get_optags.Opcodes
# Ref:
def get_executor(state):

    g_len = len

    st_ns_pop = state.num_stack.pop
    st_ns_push = state.num_stack.push
    st_cfl_push = state.cfl_stack.push
    st_cfl_drop = state.cfl_stack.drop
    st_cfl_clock = state.cfl_stack.clock
    st_cfl_compare = state.cfl_stack.compare
    st_cfl_clock_plus = state.cfl_stack.clock_plus

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
                others[0](state)
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
                i += others[0]

            else:
                #define
                pass

        pass


    # Compiled = iterable<tuple<object, ...>>
    # State = frt_core.state.State
    # Opcodes = frt_bootstrap.boot_optags.get_optags.Opcodes
    # Ref:
    def execute_with_debug(compiled, st, opcodes):
        pass


    return execute
