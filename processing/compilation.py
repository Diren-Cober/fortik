
# Author: Leontyev Kirill

from collections import deque



def post_process(compiled):
    i = 0
    lim = len(compiled)
    while i < lim:

        if compiled[i][0] == 'cmpl':
            compiled.pop(i)
            lim -= 1
            continue

        # We need '-1' correction because of state.e auto-incrementation
        #elif compiled[i][0] == 'cond':
            #compiled[i] = ('cond', ('move', compiled[i][1][1] - 1), ('move', compiled[i][2][1] - 1))
        
        i += 1
    return compiled



def cmpl(parsed):
    i = 0
    lim = len(parsed)
    compiled = deque([])
    while i < lim:
        act = parsed[i]
        if act[0] == 'def':
            compiled.append( ('cmpl', 'def-beg') )
            compiled.append( ('def', act[1]) )
            compiled.extend( cmpl(act[2]) )
            compiled.append( ('def', None) )
            compiled.append( ('cmpl', 'def-end') )

        elif act[0] == 'cond':
            case_t = cmpl(act[1])
            case_f = cmpl(act[2])
            # Expanding a condition...
            m_t = 1 if case_t else len(case_f) + 1
            m_f = len(case_t) + 2 if case_t else 1
            if not case_f:  m_f -= 1
            compiled.append( ('cmpl', 'if-beg') )
            compiled.append( ('cond', ('move', m_t), ('move', m_f)) )
            compiled.append( ('call', 'если') )
            compiled.extend(case_t)
            if case_t and case_f:
                compiled.append( ('move', len(case_f) + 1) )
            compiled.extend(case_f)
            compiled.append( ('cmpl', 'if-end') )
        
        elif act[0] == 'cond-loop':
            body = cmpl(act[2])
            delta = len(body)
            # Expanding a pre-conditional cycle...
            compiled.append( ('cmpl', 'cyc-beg') )
            compiled.append(act[1])     # The condition
            compiled.append( ('cond', ('move', 1), ('move', delta + 2)) )
            compiled.append( ('call', 'если') )
            compiled.extend(body)
            compiled.append( ('move', -(delta + 3)) )
            compiled.append( ('cmpl', 'cyc-end') )

        else:
            compiled.append(act)

        i += 1
    return list(compiled)
