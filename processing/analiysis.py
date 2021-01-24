
# Author: Kirill Leontyev (DC)
# Based on Peter Sovietov's idea

from collections import deque



def extract(tokens, i, end_mark):
    j = tokens.index(end_mark)
    seq = tokens[i:j]
    return seq, j + 1

def analize_cond(body):
    i_t = body.index('то') if 'то' in body else None
    i_f = body.index('иначе') if 'иначе' in body else None
    c_t = c_f = None
    j = 0
    if i_t and i_f:
        if i_t < i_f:
            c_t, j = extract(body, j, 'то')
            c_f, j = extract(body, j, 'иначе')
        else:
            c_f, j = extract(body, j, 'иначе')
            c_t, j = extract(body, j, 'то')
    elif i_t:
        c_t, j = extract(body, j, 'то')
    elif i_f:
        c_f, j = extract(body, j, 'иначе')
    else:
        c_t = body
        j = len(body)
    if j != len(body): raise ValueError
    return c_t, c_f



def parse(tokens):
    parsed = deque([])
    i = 0
    lim = len(tokens)
    while i < lim:
        token = tokens[i]
        try:
            parsed.append( ('push', int(token)) )
            i += 1
        except ValueError:
            if token == ':':
                try:
                    name = tokens[i + 1]
                    i += 2
                    dfntn, i = extract(tokens, i, ';')
                    ###___________________a_word___its_def___###
                    parsed.append( ('word', name, parse(dfntn)) )
                except ValueError:
                    print('Определение слова не может содержать вложенных определений и должно завершаться \';\'')
                    raise ValueError

            elif token == 'если':
                try:
                    body, i = extract(tokens, i + 1, 'сделать')
                except ValueError:
                    print('Тело условия должно завершаться словом \'сделать\'')
                    raise ValueError
                try:
                    case_t, case_f = analize_cond(body)
                    ###_____________________if_true{some code || next op}____if_false{some code || next op}_###
                    parsed.append( ('fork', parse(case_t) if case_t else [], parse(case_f) if case_f else []) )
                except ValueError:
                    print('При полной записи истинная ветвь условия завершается словом \'то\', а ложная - \'иначе\'')
                    raise ValueError
                
            elif token == 'пока':
                if parsed[-1][0] != 'call':
                    print('Условие цикла должно быть словом')
                    raise ValueError
                try:
                    body, i = extract(tokens, i + 1, 'повторять')
                    ###_________________________the_condition__the_body___###
                    parsed.append( ('cond-loop', parsed.pop(), parse(body)) )
                except ValueError:
                    print('Тело цикла должно завершаться словом \'повторять\'')
                    raise ValueError

            else:
                parsed.append( ('call', token) )
                i += 1

    return list(parsed)
