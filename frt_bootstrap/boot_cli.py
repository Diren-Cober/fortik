
# Author: Kirill Leontyev (DC)

# Ref: (iterable<str>) -> tuple<bool, str>
def extract_loc_info(args):

    from frt_localization.locale import Locale

    i = 0
    lim = len(args)
    second = None

    while i < lim:
        first = args[i]
        if first in ['-l', '--localization']:
            try:
                second = args[i + 1]
            except IndexError:
                return False, first
            loc_key = first
            del args[i:i + 2]   # Now i is a localization next's index.
            lim -= 2

        else:
            i += 1

    if second and second not in Locale.loc_names:
        return False, loc_key
    else:
        return True, second



# Ref:  Parsed = tuple<int, str, int, str, str, int, bool, bool, bool>
#       Defaults = parsed
#       (list<str>, Defaults, (str) -> str, (str) -> str, str) -> tuple<union<bool, none>, union<Parsed, str>>
def parse_start_args(args, boot_defaults, get_err_msg, get_help_msg):

    i = 0
    lim = args.__len__()

    if i < lim:

        from sys import maxsize as sys_max_size

        from frt_bootstrap.boot_low import (
            reduce_commas, match_stack_cell_types, cell_type_codes, parse_debug_settings, debug_settings_codes
        )
        from frt_encoding.coder import Coder
        # from frt_docs.help import *

        msg_format = get_err_msg('cli_syn').format
        g_int = int

        (
            ns_depth, ns_cell_type,
            rs_depth, rs_cell_type,
            code_page_name,
            debug_code, disable_gc,
            perform_deep_compilation,
            add_interrupt_protection

        ) = boot_defaults
    
        while i < lim:
            arg = args[i]
            try:
                if arg in ('-ns', '--num-stack-size'):
                    try:
                        ns_depth = g_int(args[i + 1])
                    except ValueError:
                        return False, msg_format(get_err_msg('cli_not-int').format(arg))

                    if ns_depth < 1 or ns_depth > sys_max_size:
                        return False, msg_format(get_err_msg('cli_bad-stack-size').format(arg, 'num', sys_max_size))
                    i += 2
            
                elif arg in ('-rs', '--ret-stack-size'):
                    try:
                        rs_depth = g_int(args[i + 1])
                    except ValueError:
                        return False, msg_format(get_err_msg('cli_not-int').format(arg))

                    if rs_depth < 1 or rs_depth > sys_max_size:
                        return False, msg_format(get_err_msg('cli_bad-stack-size').format(arg, 'ret', sys_max_size))
                    i += 2
            
                elif arg in ('-ct', '--stacks-cell-type'):
                    try:
                        ns_cell_type = match_stack_cell_types(args[i + 1])
                    except KeyError:
                        return False, msg_format(get_err_msg('cli_val-err').format(arg, reduce_commas(cell_type_codes)))
                    rs_cell_type = ns_cell_type
                    i += 2

                elif arg in ('-nc', '--num-stack-cell-type'):
                    try:
                        ns_cell_type = match_stack_cell_types(args[i + 1])
                    except KeyError:
                        return False, msg_format(get_err_msg('cli_val-err').format(arg, reduce_commas(cell_type_codes)))
                    i += 2

                elif arg in ('-rc', '--ret-stack-cell-type'):
                    try:
                        rs_cell_type = match_stack_cell_types(args[i + 1])
                    except KeyError:
                        return False, msg_format(get_err_msg('cli_val-err').format(arg, reduce_commas(cell_type_codes)))
                    i += 2

                elif arg in ('-cp', '--code-page'):
                    code_page_name = args[i + 1]
                    if code_page_name not in Coder.cp_names and code_page_name != 'python-built-in':
                        return False, msg_format(get_err_msg('cli_val-err').format(arg, reduce_commas(Coder.cp_names)))
                    i += 2

                elif arg in ('-d', '--debug'):
                    try:
                        debug_code = parse_debug_settings(args[i + 1])
                    except KeyError:
                        return False, msg_format(get_err_msg('cli_dbg-val-err').format(arg, reduce_commas(debug_settings_codes)))
                    i += 2

                elif arg in ('-ngc', '--disable-gc', '--disable-garbage-collection'):
                    disable_gc = True
                    i += 1

                elif arg in ('-pdc', '--perform-deep-compilation'):
                    perform_deep_compilation = True
                    i += 1

                elif arg in ('-aip', '--add-interrupt-protection'):
                    add_interrupt_protection = True
                    i += 1


                elif arg in ('-h', '--help'):
                    reduce_diapason = {
                        ':g'                : ':g',
                        ':general'          : ':g',
                        ':c'                : ':c',
                        ':configuration'    : ':c',
                        ':s'                : ':s',
                        ':syntax'           : ':s',
                        ':d'                : ':d',
                        ':debugging'        : ':d',
                        ':w'                : ':w',
                        ':words'            : ':w',
                        ':e'                : ':e',
                        ':errors'           : ':e'
                    }.__getitem__
                    try:
                        return None, get_help_msg(reduce_diapason(args[i + 1]))
                    except KeyError:
                        return None, get_help_msg(':g')
            
                else:
                    return False, msg_format(get_err_msg('cli_unknown-key').format(arg))
            
            except IndexError:
                if arg in ('-h', '--help'):
                    return None, get_help_msg(':g')
                return False, Exception(msg_format(get_err_msg('cli_no-val').format(arg)))
        
        return (
            True,
            (
                ns_depth, ns_cell_type,
                rs_depth, rs_cell_type,
                code_page_name, debug_code,
                disable_gc,
                perform_deep_compilation,
                add_interrupt_protection
            )
        )

    else:
        return (
            True,
            boot_defaults
        )



# Ref: (str, tuple<int, str, int, str, str, int, bool, bool>, (str) -> none, (int) -> str) ->
# -> tuple< union<none, int>, union<str, frt_core.machine.VM>, optional<iterable<str>> >
def boot_interface(loc_name, defaults, read, write):

    import gc
    from sys import argv

    from frt_localization.locale import load_localization

    startup_args = argv[1:]     # Ignoring the name...
    status = extract_loc_info(startup_args)
    if status[0]:

        if status[1]:
            loc_name = status[1]

        status = load_localization(loc_name)
        if status[0]:

            localization = status[1]
            status = parse_start_args(startup_args, defaults, localization.errs.__getitem__, localization.help.__getitem__)
            if status[0]:

                # Here are results of parsing...
                (
                    ns_size, ns_cell_type, rs_size, rs_cell_type,
                    coder_name, debug_code, do_disable_gc,
                    do_compile_deep, do_block_keyboard_interrupt

                ) = status[1]

                if coder_name == 'python-built-in':
                    from frt_encoding.coder import Coder
                    status = True, Coder.get_python_builtin()
                else:
                    from frt_encoding.coder import load_coder
                    status = load_coder(coder_name)

                if status[0]:

                    coder = status[1]

                    from frt_core.machine import VM

                    vm = VM.from_args(
                        ns_size, ns_cell_type, rs_size, rs_cell_type,
                        coder, debug_code, do_disable_gc, do_compile_deep,
                        do_block_keyboard_interrupt, read, write,
                        localization
                    )

                    if do_disable_gc and gc.isenabled():
                        gc.collect(0)
                        gc.collect(1)
                        gc.collect(2)
                        gc.disable()

                    return 0, vm

                elif status[1]:
                    # The coder's been not found...
                    return 11, coder_name

                else:
                    # The coder's been corrupted...
                    return 12, coder_name

            elif status[0] is None:
                # Help's been requested...
                return None, status[1]

            else:
                # Parsing error has occurred...
                return 10, status[1]

        elif status[1]:
            # Localization has not been found...
            return 8, loc_name

        else:
            # The localization has been corrupted...
            return 9, loc_name

    else:
        # An unknown localization has been requested...
        from frt_localization.locale import Locale
        return 7, status[1], Locale.loc_names
