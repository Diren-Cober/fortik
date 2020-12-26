
# Author: DC

import sys

from analysis import parse, translate
from dictionary import words



stack = []
defs = {}

while True:
    code, d = translate( parse(input("> ").split()) )
    defs.update(d)
    for symb in code:
        if symb.isdigit():
            stack.append( int(symb) )
        elif symb == 'exit':
            sys.exit()
        elif symb == 'words':
            print( words.keys(), defs.keys(), sep='\n' )
        elif symb in words.keys():
            words[ symb ]( stack )
        elif symb in defs.keys():
            for i in defs[ symb ]:
                if i.isdigit():
                    stack.append( int(i) )
                else:
                    words[i]( stack )
        else:
            print( 'Err: unknown symbol' + str(symb) )
            stack = []
            defs = {}
