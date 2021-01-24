
# Author: Peter Sovietov
# Modified: Kirill Leontyev (DC)



def print_dict(st):
    print('\tТекущий словарь')
    for name in st.ws.keys():
        print(name, end=' ')
    print()

def n_binop_arithm(func):
    def word(st):
        top = st.ns.pop()
        st.ns.push(func(st.ns.pop(), top))
    return word

def r_binop_arithm(func):
    def word(st):
        top = st.rs.pop()
        st.rs.push(func(st.rs.pop(), top))
    return word

def fork(st):
    cond = st.ns.pop()
    case_f = st.ps.pop()
    case_t = st.ps.pop()
    act = case_t if cond else case_f
    if st.dg:   print("fork\top {0}:\taddr={1}: \t\t{2}".format(st.opc, st.i, act))
    # If it is 'move' op
    if type(act) == type( ('move', 0) ):
        st.i += act[1]
    # If it is inside of a word
    else:
        act(st)



system_dictionary = {

    ############### To list all words known at the moment
    'слова':    lambda state: print_dict(state),

    ':':    None,
    ';':    None,

    ############### Numeric stack arithmetics
    '+':    n_binop_arithm( lambda a, b: a + b ),
    '-':    n_binop_arithm( lambda a, b: a - b ),
    '*':    n_binop_arithm( lambda a, b: a * b ),
    '/':    n_binop_arithm( lambda a, b: a // b ),
    '%':    n_binop_arithm( lambda a, b: a % b ),
    '<':    n_binop_arithm( lambda a, b: int(a < b) ),
    '>':    n_binop_arithm( lambda a, b: int(a > b) ),
    '1+':   lambda state: state.ns.push(state.ns.pop() + 1),        # numeric increment
    '1-':   lambda state: state.ns.push(state.ns.pop() - 1),        # numeric decrement
    
    'нуль':     lambda state: state.ns.push(0),                     # false
    'правда':   lambda state: state.ns.push(1),                     # true

    ############### Numeric stack non-arithmetic ops
    'двойник':      lambda state: state.ns.dup(),                   # dup
    'выброс':       lambda state: state.ns.pop(),                   # drop
    'обмен':        lambda state: state.ns.swap(),                  # swap
    'поворот':      lambda state: state.ns.rot(),                   # rot
    'глубина':      lambda state: state.ns.push(state.ns.depth()),  # depth

    ############### Return stack arithmetics
    'в+':   r_binop_arithm( lambda a, b: a + b ),
    'в-':   r_binop_arithm( lambda a, b: a - b ),
    'в<':   r_binop_arithm( lambda a, b: int(a < b) ),
    'в>':   r_binop_arithm( lambda a, b: int(a > b) ),
    'в1+':  lambda state: state.rs.push(state.rs.pop() + 1),        # ret-stack increment
    'в1-':  lambda state: state.rs.push(state.rs.pop() - 1),        # ret-stack decrement

    ############### Return stack non-arithmetic ops
    'в_поместить':  lambda state: state.rs.push(state.ns.pop()),    # // pushing into ret stack from num stack
    'в_вернуть':    lambda state: state.ns.push(state.rs.pop()),    # // popping from ret stack to num stack
    'в_двойник':    lambda state: state.rs.dup(),                   # rdup
    'в_выброс':     lambda state: state.rs.pop(),                   # rdrop
    'в_обмен':      lambda state: state.rs.swap(),                  # rswap
    'в_поворот':    lambda state: state.rs.rot(),                   # rrot
    'в_глубина':    lambda state: state.rs.push(state.rs.depth),    # rdepth

    ############### Base I/O
    '.':            lambda state: print(state.ns.pop()),
    '."':           None,
    'символ':       lambda state: print(state.decode(state.ns.pop())),  # emit
    'новая_строка': lambda state: print('\n'),                          # cr

    ############### Base controls
    'если':         lambda state: fork(state),
    'пока':         None
}
