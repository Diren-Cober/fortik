
# Author: Leontyev Kirill

from collections import deque



def compose(acts):
    def word(state):
        for act in acts:
            act(state)
    return word

def push(num):
    def word(st):
        st.ns.push(num)
    return word

def push_proc(act):
    def word(st):
        st.ps.push(act)
    return word
    
def call(name):
    def word(st):
        st.ws[name](st)
    return word

def collapse(acts):
    collapsed = deque([])
    for act in acts:

        if act[0] == 'push':
            collapsed.append( push(act[1]) )
        
        elif act[0] == 'call':
            collapsed.append( call(act[1]) )

        elif act[0] == 'fork':
            collapsed.append(push_proc( compose(collapse(act[1])) ))    # case_t -> word -> st.prc_stack
            collapsed.append(push_proc( compose(collapse(act[2])) ))    # case_f -> word -> st.prc_stack
            collapsed.append( call('если') )

    return list(collapsed)



# Compiles parsed input into a list of opcodes (<type>, <arg1>[, <arg2>])
# <type> = {'push'||'fork'||'move'||'call'||'word'}
# Note1: <type>=='fork' - two alternatives are pushed into procedure stack
# Note2: <type>=='move' - it is a kind of 'goto' =)
# Note3: <type>=='word' - <arg1>=new_word's_name, <arg2>=its_definition 
def cmpl(parsed):
    compiled = deque([])
    for act in parsed:

        if act[0] == 'word':
            compiled.append( ('word', act[1], collapse(act[2])) )

        elif act[0] == 'fork':
            case_t = cmpl(act[1])
            case_f = cmpl(act[2])
            # Expanding a condition...
            m_t = 1 if case_t else len(case_f) + 1  # There is not less than one case
            m_f = len(case_t) + 2 if case_t else 1
            if not case_f:  m_f -= 1    # -= ('move', X) between case_t and case_f
            compiled.append( ('fork', ('move', m_t), ('move', m_f)) )
            compiled.append( ('call', 'если') )
            if case_t:              compiled.extend(case_t)
            if case_t and case_f:   compiled.append( ('move', len(case_f) + 1) )
            if case_f:              compiled.extend(case_f)
        
        elif act[0] == 'cond-loop':
            body = cmpl(act[2])
            delta = len(body)
            # Expanding a pre-conditional cycle...
            compiled.append(act[1])     # The condition
            compiled.append( ('fork', ('move', 1), ('move', delta + 2)) )
            compiled.append( ('call', 'если') )
            compiled.extend(body)
            compiled.append( ('move', -(delta + 3)) )

        else:
            compiled.append(act)

    return list(compiled)
