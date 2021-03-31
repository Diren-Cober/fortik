
# Author: Kirill Leontyev (DC)



from sys import argv as args
from sys import exit

from core.state import State

from stacks.stack_errs import StackOverflowException as Overflow
from stacks.stack_errs import StackUnderflowException as Underflow

from help.help import help_general
from help.help import help_syntax

from typing import Tuple
from typing import List
from typing import Dict
from typing import NoReturn

from processing.analysis import parse
from processing.compilation import cmpl
from processing.execution import execute

from coders.dict_coder import Dict_coder
from coders.app.standart_coder import std_coder



# Now there is only the Ru-En custom built-in coder
# You, the person reading this, may add your own: coders/app folder
coder = std_coder



def parse_args(args: List[str]) -> Tuple[int, int, int]:
    i = 1   # Ignoring this program's name...
    lim = len(args)
    msg = "Command line arguments' syntax error: "

    ns_d = 16       # Default num stack depth.
    rs_d = 8        # Default ret stack depth.
    debug_mode = 0  # Debug mode: 0 - none, 1 - parsing...
    # ...2 - compilation, 3 - execution, 4 - all.

    def parse_args_valerr(key: str, val: str) -> NoReturn:
        msg += "'{0}' key must be followed by integer value - '{1}' has been given."
        print(msg.format(key, val))
        exit(0)
    
    def parse_args_negval(lval: str) -> NoReturn:
        print("The '{0}' value must not be negative.".format())
        exit(0)

    while i < lim:
        try:
            if args[i] in ['-ns', '--num-stack']:
                try:
                    ns_d = int(args[i + 1])
                    if ns_d < 0:
                        parse_args_negval('num stack\'s depth')
                except ValueError:
                    parse_args_valerr(args[i], args[i + 1])
                i += 2
            
            elif args[i] in ['-rs', '--ret-stack']:
                try:
                    rs_d = int(args[i + 1])
                    if rs_d < 0:
                        parse_args_negval('ret stack\'s depth')
                except ValueError:
                    parse_args_valerr(args[i], args[i + 1])
                i += 2
            
            elif args[i] in ['-d', '--debug']:
                try:
                    debug_mode = int(args[i + 1])
                    if debug_mode < 0:
                        parse_args_negval('debug mode')
                    elif debug_mode > 4:
                        debug_mode = 4
                except ValueError:
                    parse_args_valerr(args[i], args[i + 1])
                i += 2
            
            elif args[i] in ['-h', '--help']:
                #   :dbg, :syntax, :general, :dct...
                help_general()
                exit(0)
            
            else:
                msg += "unknown key: '{0}'."
                print(msg.format(args[i]))
                exit(0)
            
        except IndexError:
            msg += "the '{0}' key must be followed by a value - none's been given."
            print(msg.format(args[i - 1]))
            exit(0)
        
    return ns_d, rs_d, debug_mode



def print_dict(st: State):
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

