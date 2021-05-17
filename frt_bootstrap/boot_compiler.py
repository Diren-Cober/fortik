
# Author: Kirill Leontyev (DC)



# Tags = frt_bootstrap.boot_optags.get_optags.Tags
# Opcodes = frt_bootstrap.boot_optags.get_optags.Opcodes
# Parsed = iterable<tuple<object, ...>>
# Compiled = iterable<tuple<object, ...>>
# Ref: (Tags, Opcodes, bool, optional<(str) -> str>, optional<int>) ->
# -> union< (Parsed, Tags, Opcodes) -> Compiled, (Parsed, Tags, Opcodes) -> tuple<Compiled, str> >
def get_compiler(_tags, _opcodes, with_debug, get_dbg_msg=None, widest_cell=30):

    from collections import deque

    g_len = len
    g_int = int
    #g_list = list
    g_tuple = tuple
    #g_filter = filter

    int__lt__ = g_int.__lt__
    int__gt__ = g_int.__gt__

    equivalent_to_opcodes = (_tags.push, _tags.call, _tags.clock_p)

    _opcodes_move = _opcodes.move
    #move_or_clock = (_opcodes_move, _opcodes.clock)
    #equivalently_propagated_jumps = (_opcodes_move, _opcodes.check_cycle)

    def propagate_jump_if_possible(compiled_get, compiled_set, delta):
        to, *ta = compiled_get(delta)   # Target's opcode and args.
        if to is _opcodes_move:
            targets_delta = propagate_jump_if_possible(
                compiled_get, compiled_set, *ta
            )
            compiled_set(delta, None)
            return targets_delta
        else:
            return delta

    # Tags = frt_bootstrap.boot_optags.get_optags.Tags
    # Opcodes = frt_bootstrap.boot_optags.get_optags.Opcodes
    # Parsed = iterable<tuple<object, ...>>
    # Compiled = iterable<tuple<object, ...>>
    # Ref: (Parsed, Tags, Opcodes) -> Compiled
    def compile_tagged(parsed, tags, opcodes):

        ot_fork = tags.fork     # ...== opcodes.fork.

        compiled = deque()
        compiled_append = compiled.append
        compiled_extend = compiled.extend

        for act in parsed:
            tag = act[0]

            if tag in equivalent_to_opcodes:
                compiled_append(act)

            elif tag is ot_fork:
                case_t = compile_tagged(act[1], tags, opcodes)
                case_f = compile_tagged(act[2], tags, opcodes)
                case_t_len = g_len(case_t)
                case_f_len = g_len(case_f)
                # Computing gotos...
                if case_t_len:
                    move_t = 1
                    # If we have no 'false' case, we do not need a 'goto' at the end of the 'true' one.
                    move_f = case_t_len + (2 if case_f_len else 1)
                else:
                    move_t = case_f_len + 1
                    move_f = 1
                # Expanding a condition...
                compiled_append( (tag, move_t, move_f) )
                if case_t_len:
                    compiled_extend(case_t)
                    if case_f_len:
                        compiled_append( (opcodes.move, case_f_len + 1) )
                        compiled_extend(case_f)
                elif case_f_len:
                    compiled_extend(case_f)

            elif tag is tags.loop_while:
                body = compile_tagged(act[2], tags, opcodes)
                delta = g_len(body) + 2
                # Expanding a conditional cycle...
                compiled_append(act[1])
                compiled_append( (opcodes.fork, 1, delta) )
                compiled_extend(body)
                compiled_append( (opcodes.move, -delta) )

            elif tag is tags.loop_for:
                body = compile_tagged(act[4], tags, opcodes)
                body_len = g_len(body)
                # Expanding a counter cycle...
                compiled_append( (opcodes.setup_cycle, act[1], act[2], act[3]) )
                # The second is jump value, if the check fails.
                compiled_append( (opcodes.check_cycle, body_len + 2) )
                compiled_extend(body)
                compiled_append( (opcodes.clock, -(body_len + 1)) )

            elif tag is tags.clock_p:
                compiled_append(act)

            else:
                ### !! ###
                compiled_append( (tag, act[1], None) )

        return g_tuple(compiled)


    g_str = str
    n_join = "\n".join
    str_format = str.format

    def set_cell(template):
        return str_format(template, widest_cell)

    # Tags = frt_bootstrap.boot_optags.get_optags.Tags
    # Opcodes = frt_bootstrap.boot_optags.get_optags.Opcodes
    # Parsed = iterable<tuple<object, ...>>
    # Compiled = iterable<tuple<object, ...>>
    # Ref: (Parsed, Tags, Opcodes) -> tuple<Compiled, str>
    def compile_tagged_with_debug(parsed, tags, opcodes):

        ot_fork = tags.fork     # ...== opcodes.fork.

        compiled = deque()
        debug_info = deque()
        compiled_append = compiled.append
        compiled_extend = compiled.extend
        debug_info_append = lambda x: debug_info.append(g_str(x))

        tags_push = tags.push
        tags_call = tags.call

        for act in parsed:
            tag = act[0]

            if tag is tags_push:
                compiled_append(act)
                debug_info_append(
                    str_format(set_cell("{{:{}}}\t{{}}"), get_dbg_msg('push'), act[1])
                )

            elif tag is tags_call:
                compiled_append(act)
                debug_info_append(
                    str_format(set_cell("{{:{}}}\t'{{}}'"), get_dbg_msg('call'), act[2])
                )

            elif tag is ot_fork:
                case_t, dbg_t = compile_tagged_with_debug(act[1], tags, opcodes)
                case_f, dbg_f = compile_tagged_with_debug(act[2], tags, opcodes)
                case_t_len = g_len(case_t)
                case_f_len = g_len(case_f)
                # Computing gotos...
                if case_t_len:
                    move_t = 1
                    # If we have no 'false' case, we do not need a 'goto' at the end of the 'true' one.
                    move_f = case_t_len + (2 if case_f_len else 1)
                else:
                    move_t = case_f_len + 1
                    move_f = 1
                # Expanding a condition...
                compiled_append( (tag, move_t, move_f) )
                debug_info_append(
                    str_format(
                        set_cell("{{:{}}}\t{{}}, {{}}"), get_dbg_msg('fork'), move_t, move_f
                    )
                )
                if case_t_len:
                    compiled_extend(case_t)
                    debug_info_append(dbg_t)
                    if case_f_len:
                        compiled_append( (opcodes.move, case_f_len + 1) )
                        debug_info_append(
                            str_format(
                                set_cell("{{:{}}}\t{{}}"), get_dbg_msg('move'), case_f_len + 1
                            )
                        )
                        compiled_extend(case_f)
                        debug_info_append(dbg_f)
                else:
                    compiled_extend(case_f)
                    debug_info_append(dbg_f)

            elif tag is tags.loop_while:
                body, dbg_b = compile_tagged_with_debug(act[2], tags, opcodes)
                delta = g_len(body) + 2
                condition_call = act[1]
                # Expanding a conditional cycle...
                compiled_append(condition_call)
                debug_info_append(
                    str_format(
                        set_cell("{{:{}}}\t{{}}"), get_dbg_msg('call'), condition_call[1]
                    )
                )
                compiled_append( (opcodes.fork, 1, delta) )
                debug_info_append(
                    str_format(
                        set_cell("{{:{}}}\t{{}}, {{}}"), get_dbg_msg('fork'), 1, delta
                    )
                )
                compiled_extend(body)
                debug_info_append(dbg_b)
                compiled_append( (opcodes.move, -delta) )
                debug_info_append(
                    str_format(
                        set_cell("{{:{}}}\t{{}}"), get_dbg_msg('move'), -delta
                    )
                )

            elif tag is tags.loop_for:
                body, dbg_b = compile_tagged_with_debug(act[4], tags, opcodes)
                delta_out = g_len(body) + 2
                delta_next = - (delta_out - 1)
                start, end, step = act[1], act[2], act[3]
                # Expanding a counter cycle...
                compiled_append(
                    (opcodes.setup_cycle, start, end, step, int__lt__ if start < end else int__gt__)
                )
                debug_info_append(
                    str_format(
                        set_cell("{{:{}}}\t{{}}, {{}}, {{}}"), get_dbg_msg('cycle'), act[1], act[2], act[3]
                    )
                )
                # The second is jump value, if the check fails.
                compiled_append( (opcodes.check_cycle, delta_out) )
                debug_info_append(
                    str_format(
                        set_cell("{{:{}}}\t{{}}"), get_dbg_msg('cycle?'), delta_out
                    )
                )
                compiled_extend(body)
                debug_info_append(dbg_b)
                compiled_append( (opcodes.clock, delta_next) )
                debug_info_append(
                    str_format(
                        set_cell("{{:{}}}\t{{}}"), get_dbg_msg('clck'), delta_next
                    )
                )

            elif tag is tags.clock_p:
                compiled_append(act)
                #debug_info_append(None)     # Processed later...
                debug_info_append(
                    str_format(
                        set_cell("{{:{}}}\t<->"), get_dbg_msg('clck+')
                    )
                )

            else:
                ### !! ###
                compiled_append( (tag, act[1], None) )
                debug_info_append(
                    str_format(
                        set_cell("{{:{}}}\t{{}}, {{}}"), get_dbg_msg('wdef'), act[1], None
                    )
                )

        return g_tuple(compiled), n_join(debug_info)

    return compile_tagged_with_debug if with_debug else compile_tagged
