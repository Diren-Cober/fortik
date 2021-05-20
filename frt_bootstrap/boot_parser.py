
# Author: Kirill Leontyev



# Tags = frt_bootstrap.boot_optags.get_optags.Tags
# Words = dict<str, () -> none>
# Parsed = iterable<tuple<object, ...>>
# Ref: (bool, optional<(str) -> str>) -> (iterable<str>, int, int, Tags, Words) ->
# -> union< tuple<bool, union<Parsed, str>>, tuple<bool, union<tuple<Parsed, str>, str> >
def get_parser(with_debug=False, get_dbg_msg=None):

    g_int = int
    g_tuple = tuple

    # semi-interval = tuple<int, int>
    # Ref: (iterable<str>, int, int) -> tuple< union<semi-interval, none>, union<semi-interval, none> >
    def analyze_condition(tokens_index, i, end):

        try:
            i_t = tokens_index('то', i, end)
        except ValueError:
            i_t = None
        try:
            i_f = tokens_index('иначе', i, end)
        except ValueError:
            i_f = None

        if i_t and i_f:
            if i_t < i_f:
                c_t = (i, i_t)          # [), semi-interval
                c_f = (i_t + 1, i_f)    # [)
                j = i_f + 1
            else:
                c_f = (i, i_f)          # [)
                c_t = (i_f + 1, i_t)    # [)
                j = i_t + 1
        elif i_t:
            c_t = (i, i_t)      # [)
            c_f = (i_t, i_t)    # [)
            j = i_t + 1
        elif i_f:
            c_t = (i, i)    # [)
            c_f = (i, i_f)  # [)
            j = i_f + 1
        else:
            c_t = (i, end)      # [)
            c_f = (end, end)    # [)
            j = end

        if j != end:
            raise ValueError

        return c_t, c_f


    # Tags = frt_bootstrap.boot_optags.get_optags.Tags
    # Words = dict<str, () -> none>
    # Parsed = iterable<tuple<object, ...>>
    # Ref: (iterable<str>, int, int, Tags, Words) -> tuple<bool, union<Parsed, str>>
    def parse(tokens, i, end, tags, words):

        parsed = []
        defined = []
        parsed_append = parsed.append

        tokens_index = tokens.index

        # The most frequently used tags.
        tags_push = tags.push
        tags_call = tags.call

        while i < end:
            token = tokens[i]

            try:
                parsed_append( (tags_push, g_int(token)) )
                i += 1

            except ValueError:
                if token == ':':
                    if i + 2 >= end:
                        # word def can not be less than three tokens
                        return False, "too little def"

                    try:
                        end_of_def = tokens_index(';', i, end)
                    except ValueError:
                        # no limiter
                        return False, "no ;"

                    status = parse(tokens, i + 2, end_of_def, tags, words)
                    if status[0]:
                        i += 1
                        #____________________________a_word_________its_def____#
                        parsed_append( (tags.define, tokens[i], status[1]) )
                    else:
                        # err in word def
                        return False, status[1]

                    defined.append(tokens[i])
                    i = end_of_def + 1

                elif token == 'если':
                    try:
                        end_of_if = tokens_index('сделать', i, end)
                    except ValueError:
                        # no limiter
                        return False, ""

                    try:
                        case_t, case_f = analyze_condition(tokens_index, i + 1, end_of_if)
                    except ValueError:
                        # additional useless words
                        return False, ""

                    status_t = parse(tokens, *case_t, tags, words)
                    if status_t[0]:
                        status_f = parse(tokens, *case_f, tags, words)
                        if status_t[0]:
                            #__________________________if_true______if_false_____#
                            parsed_append( (tags.fork, status_t[1], status_f[1]) )
                        else:
                            # err in case_f
                            return False, ""
                    else:
                        # err in case_t
                        return False, ""

                    i = end_of_if + 1

                elif token == 'пока':
                    act = parsed.pop()
                    if act[0] != tags_call:
                        # must be a word's call
                        return False, ""

                    try:
                        end_of_while = tokens_index('повторять', i, end)
                    except ValueError:
                        # no limiter
                        return False, ""

                    status = parse(tokens, i + 1, end_of_while, tags, words)
                    if status[0]:
                        #____________________________the_cond_the_body___#
                        parsed_append( (tags.loop_while, act, status[1]) )
                    else:
                        # err in while body
                        return False, ""

                    i = end_of_while + 1

                elif token == 'для':
                    t2, *oth_2 = parsed.pop()
                    t1, *oth_1 = parsed.pop()
                    if t1 != tags_push or t2 != tags_push:
                        # both must be push
                        return False, ""

                    try:
                        end_of_for = tokens_index('выполнять', i, end)
                    except ValueError:
                        # no limiter
                        return False, "нет границы"

                    try:
                        step_word_index = tokens_index('с_шагом', i, end)
                        if step_word_index == i + 2:
                            try:
                                step = g_int(tokens[i + 1])
                            except ValueError:
                                # step must be integer
                                return False, "нецелый шаг"
                        else:
                            # for loop error
                            return False, "с шагом"
                    except ValueError:
                        step_word_index = i
                        step = 1

                    status = parse(tokens, step_word_index + 1, end_of_for, tags, words)
                    if status[0]:
                        parsed_append( (tags.loop_for, *oth_1, *oth_2, step, status[1]) )
                    else:
                        # err in for body
                        return False, status[1]

                    i = end_of_for + 1

                elif token == 'счётчик+':
                    parsed_append((tags.clock_p,))
                    i += 1

                else:
                    try:
                        parsed_append( (tags_call, words[token]) )
                    except KeyError:
                        if token in defined:
                            parsed_append( (tags_call, None, token) )
                        else:
                            # unknown word
                            return False, ""

                    i += 1

        return True, g_tuple(parsed)


    g_str = str
    str_join = str.join
    str_format = g_str.format

    # Tags = frt_bootstrap.boot_optags.get_optags.Tags
    # Words = dict<str, () -> none>
    # Parsed = iterable<tuple<object, ...>>
    # Ref: (iterable<str>, int, int, Tags, Words, optional<int>) -> tuple<bool, union<tuple<Parsed, str>, str>>
    def parse_with_debug(tokens, i, end, tags, words, nesting=0):

        parsed = []
        defined = []
        debug_info = []
        parsed_append = parsed.append
        debug_info_pop = debug_info.pop
        debug_info_append = debug_info.append

        tokens_index = tokens.index

        # The most frequently used tags.
        tags_push = tags.push
        tags_call = tags.call

        post_indent = "\n" + "\t" * nesting
        pre_indent = post_indent + "\t"

        while i < end:
            token = tokens[i]

            try:
                parsed_append( (tags_push, g_int(token)) )
                debug_info_append( str_format("({}, {})", get_dbg_msg('push'), token) )
                i += 1

            except ValueError:
                if token == ':':
                    if i + 2 >= end:
                        # word def can not be less than three tokens
                        return False, "too little def"

                    try:
                        end_of_def = tokens_index(';', i, end)
                    except ValueError:
                        # no limiter
                        return False, "no ;"

                    status = parse_with_debug(tokens, i + 2, end_of_def, tags, words, nesting=(nesting + 1))
                    if status[0]:
                        name = tokens[i + 1]
                        #___________________________a_word_its_def____#
                        parsed_append( (tags.define, name, status[1]) )
                        debug_info_append(
                            str_format(
                                "({}, '{}', {{{}{}{}}})",
                                get_dbg_msg('wdef'), name, pre_indent, status[2] , post_indent
                            )
                        )
                    else:
                        # err in word def
                        return False, status[1]

                    defined.append(name)
                    i = end_of_def + 1

                elif token == 'если':
                    try:
                        end_of_if = tokens_index('сделать', i, end)
                    except ValueError:
                        # no limiter
                        return False, ""

                    try:
                        case_t, case_f = analyze_condition(tokens_index, i + 1, end_of_if)
                    except ValueError:
                        # additional useless words
                        return False, ""

                    status_t = parse_with_debug(tokens, *case_t, tags, words, nesting=(nesting + 1))
                    if status_t[0]:
                        status_f = parse_with_debug(tokens, *case_f, tags, words, nesting=(nesting + 1))
                        if status_t[0]:
                            #__________________________if_true______if_false_____#
                            parsed_append( (tags.fork, status_t[1], status_f[1]) )
                            debug_info_append(
                                str_format(
                                    "({2}, {{{0}{3}{1}}}, {{{0}{4}{1}}})", pre_indent, post_indent,
                                    get_dbg_msg('fork'), status_t[2], status_f[2]
                                )
                            )
                        else:
                            # err in case_f
                            return False, ""
                    else:
                        # err in case_t
                        return False, ""
                    i = end_of_if + 1

                elif token == 'пока':
                    act = parsed.pop()
                    if act[0] != tags_call:
                        # must be a word's call
                        return False, ""

                    try:
                        end_of_while = tokens_index('повторять', i, end)
                    except ValueError:
                        # no limiter
                        return False, ""

                    status = parse_with_debug(tokens, i + 1, end_of_while, tags, words, nesting=(nesting + 1))
                    if status[0]:
                        #____________________________the_cond_the_body___#
                        parsed_append( (tags.loop_while, act, status[1]) )
                        debug_info_append(
                            str_format(
                                "({}, {}, {{{}{}{}}})",
                                get_dbg_msg('lwhl'), debug_info.pop(), pre_indent, status[2], post_indent
                            )
                        )
                    else:
                        # err in while body
                        return False, ""

                elif token == 'для':
                    t2, *oth_2 = parsed.pop()
                    t1, *oth_1 = parsed.pop()
                    debug_info_pop()
                    debug_info_pop()
                    if t1 != tags_push or t2 != tags_push:
                        # both must be push
                        return False, ""

                    try:
                        end_of_for = tokens_index('выполнять', i, end)
                    except ValueError:
                        # no limiter
                        return False, "нет границы"

                    try:
                        step_word_index = tokens_index('с_шагом', i, end)
                        if step_word_index == i + 2:
                            try:
                                step = g_int(tokens[i + 1])
                            except ValueError:
                                # step must be integer
                                return False, "нецелый шаг"
                        else:
                            # for loop error
                            return False, "с шагом"
                    except ValueError:
                        step_word_index = i
                        step = 1

                    status = parse_with_debug(tokens, step_word_index + 1, end_of_for, tags, words, nesting=(nesting + 1))
                    if status[0]:
                        parsed_append( (tags.loop_for, *oth_1, *oth_2, step, status[1]) )
                        debug_info_append(
                            str_format(
                                "({}, {}, {}, {}, {{{}{}{}}})", get_dbg_msg('lfor'),
                                *oth_1, *oth_2, step, pre_indent, status[2], post_indent
                            )
                        )
                    else:
                        # err in for body
                        return False, status[1]

                    i = end_of_for + 1

                elif token == 'счётчик+':
                    parsed_append((tags.clock_p,))
                    debug_info_append( str_format("({})", get_dbg_msg('clck+')) )
                    i += 1

                else:
                    try:
                        parsed_append( (tags_call, None if token in defined else words[token], token) )
                    except KeyError:
                        # unknown word
                        return False, ""

                    debug_info_append(str_format("({}, '{}')", get_dbg_msg('call'), token))
                    i += 1

        return True, g_tuple(parsed), str_join(post_indent, debug_info)

    return parse_with_debug if with_debug else parse
