
# Author: Kirill Leontyev (DC)



from sys import argv as args
from sys import exit

from core.state import State

from stacks.stack_errs import StackOverflowException as Overflow
from stacks.stack_errs import StackUnderflowException as Underflow

from help.help import help_general
from help.help import help_syntax

from processing.analysis import parse
from processing.compilation import cmpl
from processing.execution import execute

from coders.dict_coder import Dict_coder
from coders.app.standart_coder import std_coder



# Now there is only the Ru-En custom built-in coder
# You, the person reading this, may add your own: coders/app folder
coder = std_coder



def parse_args(args):
    i = 1   # Ignoring this program's name...
    lim = len(args)
    msg = "Command line arguments' syntax error: "
    
    ns_d = 16
    rs_d = 8
    debug = 0

    while i < lim:
        if  args[i] in ['-h', '--help']:
            help_general()
            exit(0)
        elif args[i] in ['-d', '--debug']:
            debug = 1
        else:
            try:
                if args[i] in ['-n', '--num_st_depth']:
                    i += 1
                    ns_d = int(args[i])
                elif args[i] in ['-r', '--ret_st_depth']:
                    i += 1
                    rs_d = int(args[i])
            except ValueError:
                msg += "'{0}' must be followed by integer value - '{1}' has been given"
                print(msg.format(args[i - 1], args[i]))
                exit(0)
            except IndexError:
                msg += "the {0} key must be followed by a value - none's been given."
                print(msg.format(args[i - 1]))
                exit(0)
        i += 1   
    return ns_d, rs_d, debug

def print_dict(st):
    print('\n\tТекущий словарь:')
    i = 0
    words = list(st.ws.keys())
    lim = len(words)
    while i < lim:
        print(words[i], end='\t\t')
        if not (i % 5) and i:
            print()
        i += 1
    print()



### start: ###
ns_d, rs_d, debug = parse_args(args)

try:
    state = State(ns_d, rs_d, coder, debug)
except ValueError as verr:
    print('\n' + str(verr))
    exit(0)

while True:
    inp = input("\n> ").split()
    #check = len(inp)
    if len(inp) > 0:
        if inp[0] in ['выход', 'выйти']:
            break
        elif inp[0] in ['сброс_стеков', 'сбросить_стеки']:
            state.reset_stacks()
        elif inp[0] in ['сброс_системы', 'сбросить_систему']:
            state.reset_whole()
        elif inp[0] in ['состояние', 'состояние_системы']:
            print('\n' + str(state))
        elif inp[0] in ['слова', 'словарь']:
            print_dict(state)
        else:
            try:
                state.reset_counters()
                print()
                ### ready: ###
                execute(cmpl(parse(inp)), state)
            except TypeError as terr:
                print(terr)
                state.reset_stacks()
            except KeyError as kerr:
                print('Неизвестное слово: ' + str(kerr))
            except ValueError:
                print('Синтаксическая ошибка')
            except Overflow as orr:
                print('Переполнение стека: ' + str(orr))
                state.reset_stacks()
            except Underflow as urr:
                print('Разрушение стека: ' + str(urr))
                state.reset_stacks()

