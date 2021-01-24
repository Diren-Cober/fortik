
# Author: Kirill Leontyev

from processing.compilation import compose



# Base: the idea of a Turing Machine
def execute(ops, st):
    st.i = 0
    lim = len(ops)
    if st.dg:   print("\n\tcompiled:\n\t{}".format(str(ops)), end='\n\n')
    while st.i < lim:

        op = ops[st.i]
        st.i_unlck()
        if st.dg:   print("\top {0}:\taddr={1}: \t\t{2}".format(st.opc, st.i, op))

        if op[0] == 'push':
            st.ns.push(op[1])
        elif op[0] == 'call':
            st.ws[op[1]](st)    # st.i may become locked

        elif op[0] == 'fork':
            st.ps.push(op[1])
            st.ps.push(op[2])

        elif op[0] == 'move':
            st.i += op[1]   # Becomes locked

        elif op[0] == 'word':
            st.ws[op[1]] = compose(op[2])

        st.i += 1
    return
