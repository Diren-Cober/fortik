
# Author: Kirill Leontyev (DC)



# Ref: () -> (iterable<str>) -> str
def get_commas_reducer():
    from functools import reduce
    return lambda iterable: reduce('{}, {}'.format, iterable)

reduce_commas = get_commas_reducer()
del get_commas_reducer



# A hack: we cache ref to sep.join's argument and mutate it instead of multiple allocation
# .. of small iterables (we also reduce implicit deallocation work).
# This hack is in even higher use in frt_localization.locale and frt_encoding.coder modules.
#
# Ref: (str) -> tuple<bool, optional<str>>
def check_if_any_system_files_are_missing(location):

    from os.path import sep, exists

    losses = []
    missing = False

    losses_append = losses.append
    sep_join = sep.join
    g_exists = exists

    sep_join_arg = [sep_join( (location, 'frt_bootstrap') ), 'boot_builtins.py']
    sep_join_arg_set = sep_join_arg.__setitem__
    if not g_exists(sep_join(sep_join_arg)):
        missing = True
        losses_append('frt_bootstrap/boot_builtins.py')

    sep_join_arg_set(1, 'boot_cli.py')
    if not g_exists(sep_join(sep_join_arg)):
        missing = True
        losses_append('frt_bootstrap/boot_cli.py')

    sep_join_arg_set(1, 'boot_compiler.py')
    if not g_exists(sep_join(sep_join_arg)):
        missing = True
        losses_append('frt_bootstrap/boot_compiler.py')

    sep_join_arg_set(1, 'boot_executor.py')
    if not g_exists(sep_join(sep_join_arg)):
        missing = True
        losses_append('frt_bootstrap/boot_executor.py')

    sep_join_arg_set(1, 'boot_optags.py')
    if not g_exists(sep_join(sep_join_arg)):
        missing = True
        losses_append('frt_bootstrap/boot_optags.py')

    sep_join_arg_set(1, 'boot_parser.py')
    if not g_exists(sep_join(sep_join_arg)):
        missing = True
        losses_append('frt_bootstrap/boot_parser.py')

    sep_join_arg_set(1, 'boot_starter.py')
    if not g_exists(sep_join(sep_join_arg)):
        missing = True
        losses_append('frt_bootstrap/boot_starter.py')


    frt_core = sep_join([location, 'frt_core'])
    if g_exists(frt_core):

        sep_join_arg_set(0, frt_core)
        sep_join_arg_set(1, 'cf_stack.py')
        if not g_exists(sep_join(sep_join_arg)):
            missing = True
            losses_append('frt_core/cf_stack.py')

        sep_join_arg_set(1, 'machine.py')
        if not g_exists(sep_join(sep_join_arg)):
            missing = True
            losses_append('frt_core/machine.py')

        sep_join_arg_set(1, 'settings.py')
        if not g_exists(sep_join(sep_join_arg)):
            missing = True
            losses_append('frt_core/settings.py')

        sep_join_arg_set(1, 'stack.py')
        if not g_exists(sep_join(sep_join_arg)):
            missing = True
            losses_append('frt_core/stack.py')

        sep_join_arg_set(1, 'state.py')
        if not g_exists(sep_join(sep_join_arg)):
            missing = True
            losses_append('frt_core/stata.py')

        sep_join_arg_set(1, 'words.py')
        if not g_exists(sep_join(sep_join_arg)):
            missing = True
            losses_append('frt_core/words.py')

    else:
        missing = True
        losses_append('frt_core')


    frt_encoding = sep_join([location, 'frt_encoding'])
    if g_exists(frt_encoding):

        sep_join_arg_set(0, frt_encoding)
        sep_join_arg_set(1, 'coder.py')
        if not g_exists(sep_join(sep_join_arg)):
            missing = True
            losses_append('frt_encoding/coder.py')

        sep_join_arg_set(1, 'code_pages')
        if not g_exists(sep_join(sep_join_arg)):
            missing = True
            losses_append('frt_encoding/code_pages')

    else:
        missing = True
        losses_append('frt_encoding')


    frt_localization = sep_join([location, 'frt_localization'])
    if g_exists(frt_localization):

        sep_join_arg_set(0, frt_localization)
        sep_join_arg_set(1, 'locale.py')
        if not g_exists(sep_join(sep_join_arg)):
            missing = True
            losses_append('frt_localization/locale.py')

        sep_join_arg_set(1, 'localizations')
        if not g_exists(sep_join(sep_join_arg)):
            missing = True
            losses_append('frt_localization/localizations')

    else:
        missing = True
        losses_append('frt_localization')


    return (
        True, tuple(losses)
    ) if missing else (False,)



# (*): used in frt_bootstrap/boot_cli.py, but defined here
# .. to make possible future changes easier.
cell_type_codes = ('i8', 'i16', 'i32', 'i64')

# Ref: (str) -> str
match_stack_cell_types = {
    'i8'    : 'b',
    'i16'   : 'h',
    'i32'   : 'i',
    'i64'   : 'q'
}.__getitem__



# (*).
debug_settings_codes = (
    'p', 'parsing', 'c', 'compilation', 'e', 'execution'
)

# Ref: () -> (str) -> int
def get_debug_settings_parser():

    str_len = str.__len__
    str_split = str.split
    str_starts_with = str.startswith

    # Ref: (str) -> list<str>
    def split_debug_val(val):
        return str_split(val, '+')

    match_dbg_setting = {
        'p'             : 0x00000001,
        'parsing'       : 0x00000001,
        'c'             : 0x00000002,
        'compilation'   : 0x00000002,
        'e'             : 0x00000004,
        'execution'     : 0x00000004
    }.__getitem__

    match_dbg_aliases = {
        'all'   : 0x00000007,
        'ce'    : 0x00000006,
        'none'  : 0x00000000
    }.__getitem__

    def parse_dbg_settings(val):
        dbg = 0x00000000
        if str_starts_with(val, '{') and str_len(val) > 4:
            for v in split_debug_val(val[1:-1]):
                dbg |= match_dbg_setting(v)
        else:
            return match_dbg_aliases(val)

        return dbg

    return parse_dbg_settings

parse_debug_settings = get_debug_settings_parser()
del get_debug_settings_parser



# IMPORTANT!!!
# This function parses boot.config (if exists) silently.
# If an error is occurred, the parameter just has 'builtin' value.
#
# Ref: (str) -> tuple<int, str, int, str, str, str, int, bool, bool, bool>
def get_boot_defaults(location):

    from sys import maxsize as sys_max_size
    from os.path import sep, exists

    boot_conf_path = sep.join([location, 'frt_bootstrap', 'boot.config'])

    ns_d = 32
    ns_c = 'q'
    rs_d = 16
    rs_c = 'q'
    codr = 'builtin'
    locn = 'eng'
    dbgc = 0x00000000
    nogc = False
    dcmp = False
    aipr = False

    if exists(boot_conf_path):

        g_int = int
        list_len = list.__len__
        str_split = str.split
        str_index = str.index
        match_sct = match_stack_cell_types

        # Parsing boot.config...
        with open(boot_conf_path) as boot_conf:
            for line in boot_conf:

                try:
                    # Excluding comments if exists.
                    line = line[:str_index(line, '#')]
                except ValueError:
                    pass

                split = str_split(line)
                if list_len(split) == 2:
                    tag, val = split

                    if tag == 'num-stack-size':
                        ns_d = g_int(val)
                        if ns_d < 2 or ns_d > sys_max_size:
                            ns_d = 32

                    elif tag == 'num-stack-cell-type':
                        try:
                            ns_c = match_sct(val)
                        except KeyError:
                            ns_c = 'q'

                    elif tag == 'ret-stack-size':
                        rs_d = g_int(val)
                        if rs_d < 1 or rs_d > sys_max_size:
                            rs_d = 16

                    elif tag == 'ret-stack-cell-type':
                        try:
                            rs_c = match_sct(val)
                        except KeyError:
                            rs_c = 'q'

                    elif tag == 'code-page':
                        codr = val

                    elif tag == 'localization':
                        locn = val

                    elif tag == 'debug':
                        try:
                            dbgc = parse_debug_settings(val)
                        except KeyError:
                            pass

                    elif tag == 'disable-garbage-collection':
                        nogc = True if val in ['True', 'true'] else False

                    elif tag == 'perform-deep-compilation':
                        dcmp = True if val in ['True', 'true'] else False

                    elif tag == 'add-interrupt-protection':
                        aipr = True if val in ['True', 'true'] else False

    return locn, (ns_d, ns_c, rs_d, rs_c, codr, dbgc, nogc, dcmp, aipr)



# Ref: ((...) -> any, ...) -> (...) -> none
def wrap_in_interrupt_blocker(func, *args, **kwargs):
    def wrapper():
        try:
            func(args, kwargs)
        except KeyboardInterrupt:
            pass

    wrapper.__name__ = func.__name__
    wrapper.__qualname__ = func.__qualname__
    wrapper.__module__ = func.__module__
    return wrapper
