
# Author: Kirill Leontyev (DC)



class Locale:

    ######### ! !! !!! !!!! !!!!!! !!!! !!! !! ! #########
    loc_names = ('rus', 'eng')
    dfl_loc = 'eng'
    ######### ! !! !!! !!!! !!!!!! !!!! !!! !! ! #########

    # Ref: <all>: dict<str, str>
    __slots__ = ('errs', 'help', 'dbgs', 'tags', 'words')

    # Ref: (module) -> none
    def __init__(self, loc_module):
        self.errs   = loc_module.errs
        self.help   = loc_module.refs
        self.dbgs   = loc_module.dbgs
        self.tags   = loc_module.tags
        self.words  = loc_module.words



# This function is optimized to process multiple objects (so do the analogue in frt_encoding/coder.py),
# .. because 'localizations' folder may contain lots of localization modules.
#
# Ref: (str) -> tuple<bool, optional<str>>
def check_if_any_localizations_are_missing(location):

    from os.path import sep, exists

    g_exists = exists
    sep_join = sep.join
    sep_join_arg = [sep_join( (location, 'frt_localization', 'localizations') ), None]
    sep_join_arg_set = sep_join_arg.__setitem__
    losses = []
    losses_append = losses.append
    missing = False

    for loc_name in Locale.loc_names:
        sep_join_arg_set(1, f'loc_{loc_name}.py')
        if not g_exists(sep_join(sep_join_arg)):
            missing = True
            losses_append(f'frt_localization/localizations/loc_{loc_name}.py')

    return (
        True, tuple(losses)
    ) if missing else (
        False, None
    )



# Ref: (str) -> tuple<bool, union<Locale, bool>>
def load_localization(loc_name):

    from importlib import import_module

    try:
        loc_module = import_module("frt_localization.localizations.loc_{}".format(loc_name))
    except ModuleNotFoundError:
        return False, True
    g_hattr = hasattr
    
    # If all needed parts of localization are there...
    if (
            g_hattr(loc_module, 'errs') and g_hattr(loc_module, 'refs') and
            g_hattr(loc_module, 'dbgs') and g_hattr(loc_module, 'tags') and
            g_hattr(loc_module, 'words')
    ):
        return True, Locale(loc_module)
    else:
        return False, False
