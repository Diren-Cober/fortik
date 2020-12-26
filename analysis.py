
# Author: Peter Sovietov
# Modified: DC

##(0)# Throws ValueError.
def parse( tokens ):
    intercode = []
    while tokens:
        token = tokens.pop(0)
        if token.isdigit():
            intercode.append( ('num', token) )
        elif token == ':':
            delta = tokens.index(';')  ##(0)#
            intercode.append( ('def', tokens[0 : delta]) )
            del tokens[ : delta + 1 ]
        else:
            intercode.append( ('call', token) )
    return intercode



def translate( intercode ):
    compiled = []
    definitions = {}
    for op in intercode:
        if op[0] == 'num':
            compiled.append( op[1] )
        elif op[0] == 'def':
            defined = define( op[1] )
            if defined[0]:
                definitions[ defined[0] ] = defined[1]
        else:
            compiled.append( str(op[1]) )
    return ( compiled, definitions )


##(1)# Throws ValueError
def define( article ):
    if len(article) > 0:
        word = str( article.pop(0) )
        code = translate( parse(article) )[0]  ##(1)#
        return ( word, code )
    else:
        return ( None, None )

