
# Author: Peter Sovietov
# Modified: Kirill Leontyev (DC)



# Binary stack arithmetic operations' generators.
def int_wrap(func):
    return lambda a, b: int(func(a, b))

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

    ### These words are used only in parsing - there is no modes like in classic Forth.
    ':' :   None,
    ';' :   None,

    ############### Numeric stack arithmetics
    '+' :   n_binop_arithm( int.__add__ ),
    '-' :   n_binop_arithm( int.__sub__ ),
    '*' :   n_binop_arithm( int.__mul__ ),
    '/' :   n_binop_arithm( int.__floordiv__ ),
    '%' :   n_binop_arithm( int.__mod__ ),
    '**':   n_binop_arithm( int.__pow__ ),
    '<<':   n_binop_arithm( int.__lshift__ ),
    '>>':   n_binop_arithm( int.__rshift__ ),
    '!' :   lambda state: state.ns.invert_top(),
    '&' :   n_binop_arithm( int.__and__ ),
    '|' :   n_binop_arithm( int.__or__ ),
    '^' :   n_binop_arithm( int.__xor__ ),
    '1+':   lambda state: state.ns.increment_top(),         # numeric increment
    '1-':   lambda state: state.ns.decrement_top(),         # numeric decrement
    '<' :   n_binop_arithm( int_wrap(int.__lt__) ),
    '<=':   n_binop_arithm( int_wrap(int.__le__) ),
    '>' :   n_binop_arithm( int_wrap(int.__gt__) ),
    '>=':   n_binop_arithm( int_wrap(int.__ge__) ),
    '=' :   n_binop_arithm( int_wrap(int.__eq__) ),
    '!=':   n_binop_arithm( int_wrap(int.__ne__) ),
    
    'ложь'  :   lambda state: state.ns.push(0),             # false
    'правда':   lambda state: state.ns.push(1),             # true
    '&&'    :   n_binop_arithm( int.__mul__ ),              # logic and
    '||'    :   n_binop_arithm( int.__or__ ),               # logic or
    '^^'    :   n_binop_arithm( int_wrap(int.__ne__) ),     # logic xor

    ############### Numeric stack non-arithmetic ops
    'двойник'   :       lambda state: state.ns.dup(),                   # dup
    'выброс'    :       lambda state: state.ns.pop(),                   # drop
    'обмен'     :       lambda state: state.ns.swap(),                  # swap
    'оборот'    :       lambda state: state.ns.rot(),                   # rot
    'глубина'   :       lambda state: state.ns.push(state.ns.depth()),  # depth

    ############### Return stack arithmetics
    'в+'    :   r_binop_arithm( int.__add__ ),
    'в-'    :   r_binop_arithm( int.__sub__ ),
    'в<'    :   r_binop_arithm( int_wrap(int.__lt__) ),
    'в>'    :   r_binop_arithm( int_wrap(int.__gt__) ),
    'в='    :   r_binop_arithm( int_wrap(int.__eq__) ),
    'в!='   :   r_binop_arithm( int_wrap(int.__ne__) ),
    'в1+'   :   lambda state: state.rs.increment_top(),         # ret-stack increment
    'в1-'   :   lambda state: state.rs.decrement_top(),         # ret-stack decrement

    ############### Return stack non-arithmetic ops
    'в_поместить'   :   lambda state: state.rs.push(state.ns.pop()),    # // pushing into ret stack from num stack
    'в_вернуть'     :   lambda state: state.ns.push(state.rs.pop()),    # // popping from ret stack to num stack
    'в_двойник'     :   lambda state: state.rs.dup(),                   # rdup
    'в_выброс'      :   lambda state: state.rs.pop(),                   # rdrop
    'в_обмен'       :   lambda state: state.rs.swap(),                  # rswap
    'в_поворот'     :   lambda state: state.rs.rot(),                   # rrot
    'в_глубина'     :   lambda state: state.rs.push(state.rs.depth),    # rdepth

    ############### Base I/O
    '.'             :   lambda state: print(state.ns.pop()),
    '."'            :   None,
    'символ'        :   lambda state: print(state.decode(state.ns.pop())),  # emit
    'новая_строка'  :   lambda state: print('\n'),                          # cr

    ############### Base controls
    'если':         lambda state: fork(state),
    'пока':         None
}
