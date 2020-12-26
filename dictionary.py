
# Author: Peter Sovietov
# Modified: DC



def binop( func ):
    def word( stack ):
        tmp = stack.pop()
        stack.append( func(stack.pop(), tmp) )
    return word

def dup( stack ):
    stack.append( stack[-1] )

def drop( stack ):
    stack.pop()

def swap( stack ):
    stack[-2 : ] = stack[-1 : -2 : -1]

def depth( stack ):
    stack.append( len(stack) )

def dot( stack ):
    print( stack.pop() )

def emit( stack ):
    print( chr(stack.pop()), end="" )

def cr( stack ):
    stack.append(10)
    emit( stack )

def cond( stack ):
    if stack.pop():
        words[ str(stack.pop()) ]( stack )

def ifel( stack ):
    cond = stack.pop()
    a = stack.pop()
    b = stack.pop()
    if cond:
        a( stack )
    else:
        b( stack )



base = {
    '+': binop( lambda a, b: a + b ),
    '-': binop( lambda a, b: a - b ),
    '*': binop( lambda a, b: a * b ),
    '/': binop( lambda a, b: a // b ),
    '<': binop( lambda a, b: int(a < b) ),
    'dup': dup,
    'drop': drop,
    'swap': swap,
    'depth': depth,
    '.': dot,
    'emit': emit,
    'cr': cr,
    'if': cond,
    'ifel': ifel
}

words = base
