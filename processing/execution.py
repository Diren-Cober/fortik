
# Author: Kirill Leontyev



def exec(ops, st):
    st.i = 0
    lim = len(ops)
    if st.dg:   print("\n\tcompiled:\n\t{}".format(str(ops)), end='\n\n')
    while st.i < lim:

        op = ops[st.i]
        st.i_unlck()
        if st.dg:   print("\top {0}:\t{1}".format(st.i, op))

        if op[0] == 'num':
            st.ns.push(op[1])
    
        elif op[0] == 'call':
            st.ws[op[1]](st)    # st.i may become locked
    
        elif op[0] == 'cond':
            st.ps.push(op[1])
            st.ps.push(op[2])
    
        elif op[0] == 'move':
            st.i += op[1]   # Becomes locked

        st.i += 1
    return
