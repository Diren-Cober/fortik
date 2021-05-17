
# Author: Kirill Leontyev (DC)



class Coder:

    ######### ! !! !!! !!!! !!!!!! !!!! !!! !! ! #########
    cp_names = ('builtin',)
    ######### ! !! !!! !!!! !!!!!! !!!! !!! !! ! #########

    # Ref:  encode: (str) -> int
    #       decode: (int) -> str
    __slots__ = ('encode', 'decode')

    # Ref: () -> Coder
    @classmethod
    def get_python_builtin(cls):
        self = object.__new__(cls)
        self.encode = ord
        self.decode = chr
        return self

    # Ref: (iterable<tuple<str, int>>) -> optional<TypeError>
    def __init__(self, assoc_list):
        drive_dec = {}
        drive_enc = {}

        g_int = int
        g_str = str

        for k, v in assoc_list:
            drive_dec[g_int(v)] = g_str(k)
            drive_enc[g_str(k)] = g_int(v)

        self.encode = drive_enc.__getitem__
        self.decode = drive_dec.__getitem__



# There should be some...
# In fact, there is only one now...
# But the optimizations are here: for future purposes.
#
# Ref: (str) -> tuple<bool, optional<str>>
def check_if_any_coders_are_missing(location):

    from os.path import sep, exists
    from collections import deque

    sep_join = sep.join
    sep_join_arg = [sep_join( (location, 'frt_encoding', 'code_pages') ), None]
    losses = deque([])
    losses_append = losses.append
    missing = False

    for cp_name in Coder.cp_names:
        sep_join_arg[1] = f'cp_{cp_name}.py'
        if not exists(sep_join(sep_join_arg)):
            missing = True
            losses_append(f'frt_encoding/code_pages/cp_{cp_name}.py')

    return (
        True, tuple(losses)
    ) if missing else (
        False, None
    )



# Ref: (str) -> tuple<bool, union<Coder, bool>>
def load_coder(coder_name):

    if coder_name == 'python-built-in':
        return True, Coder.get_python_builtin()

    else:
        from importlib import import_module

        try:
            coder_m = import_module("frt_encoding.code_pages.cp_{}".format(coder_name))
        except ModuleNotFoundError:
            return False, True

        if hasattr(coder_m, 'cp'):
            return True, Coder(coder_m.cp)
        else:
            return False, False
