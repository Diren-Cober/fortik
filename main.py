
# Author: Kirill Leontyev (DC)

from core.state import State
from stacks.stack_errs import StackOverflowException as Overflow
from stacks.stack_errs import StackUnderflowException as Underflow

from processing.analiysis import parse
from processing.compilation import cmpl
from processing.compilation import post_process
from processing.execution import exec

from coders.dict_coder import Dict_coder
from coders.app.standart_coder import std_coder

from sys import argv as args
from sys import exit



def print_help():
    print('\n\tfortik - tiny Forth-like language\n')
    print('-h | --help\t\t\tto see this')
    print('-d | --debug\t\t\tto see compiled imput and step-by-step execution (turned off by default)')
    print('-n | --num_st_depth   <int>\tto set custom depth for the num stack (the default is 16)')
    print('-r | --ret_st_depth   <int>\tto set custom depth for the ret stack (the default is 8)')



ns_d = 16
rs_d = 8    # However, ret_stack is not in use until counter-cycles are supported
debug = 0

# Now there is only the Ru-En custom built-in coder
# You, the person reading this, may add your own: coders/app folder
coder = std_coder



### start: ###
lim = len(args)
if lim == 2:
    if args[1] in ['-h', '--help']:
        print_help()
        exit(0)
    elif args[1] in ['-d', '--debug']:
        debug = 1
    else:
        print('Program arguments\' syntax error')
        exit(0)
else:
    i = 1   # Ignoring this program name...
    while i < lim:
        try:
            if args[i] in ['-n', '--num_st_depth']:
                ns_d = int(args[i + 1])
                i += 2
            elif args[i] in ['-r', '--ret_st_depth']:
                rs_d = int(args[i + 1])
                i += 2
            elif args[i] in ['-d', '--debug']:
                debug = 1
                i += 1
        except (IndexError, ValueError):
            print('Program arguments\' syntax error')
            exit(0)



try:
    state = State(ns_d, rs_d, coder, debug)
except ValueError as verr:
    print('\n' + str(verr))
    exit(0)

while True:
    inp = input("\n> ").split()
    check = len(inp)
    if check > 0:
        if inp[0] in ['выход', 'выйти']:
            break
        elif inp[0] == 'сброс_стеков':
            state.reset_stacks()
        elif inp[0] == 'сброс_системы':
            state.reset()
        elif inp[0] == 'состояние':
            print('\n' + str(state))
        else:
            try:
                print()
                ops = post_process( cmpl(parse(inp)) )
                exec(ops, state)
            except KeyError as kerr:
                print('Неизвестное слово: ' + str(kerr))
            except ValueError:
                print('Синтаксическая ошибка')
            except Overflow as orr:
                print('Переполнение стека: ' + str(orr))
                state.reset()
            except Underflow as urr:
                print('Разрушение стека: ' + str(urr))
                state.reset_stacks()
