# Author: Kirill Leontyev (DC)



# Res = tuple< union<int, none>, optional<union<str, frt_core.machine.VM>>, optional<iterable<str>> >
# IRes = tuple< union<int, none>, union<str, frt_core.machine.VM>, optional<iterable<str>> >
# Defaults = tuple<int, str, int, str, str, int, bool, bool>
# Writer = (str) -> none; reader = (int) -> str
# Ref: (str, (str, Defaults, Writer, Reader) -> IRes, Writer, Reader) -> Res
def boot(location,  boot_interface, read, write):

    from os.path import sep, exists

    # Checking system's integrity...
    sep_join = sep.join
    frt_bootstrap_location = sep_join([location, 'frt_bootstrap'])
    if exists(frt_bootstrap_location):

        if exists(sep_join([frt_bootstrap_location, 'boot_low.py'])):

            try:
                from frt_bootstrap.boot_low import check_if_any_system_files_are_missing
            except ImportError:
                # The 'frt_bootstrap/boot_low.py' file has been corrupted...
                return 3,

            status = check_if_any_system_files_are_missing(location)
            if status[0]:
                # System files are missing...
                return 4, status[1]

            from frt_localization.locale import check_if_any_localizations_are_missing
            status = check_if_any_localizations_are_missing(location)
            if status[0]:
                # Localization files are missing...
                return 5, status[1]

            from frt_encoding.coder import check_if_any_code_pages_are_missing
            status = check_if_any_code_pages_are_missing(location)
            if status[0]:
                # Code pages are missing...
                return 6, status[1]

        else:
            # The 'frt_bootstrap/boot_low.py' file is missing...
            return 2,

    else:
        # The 'frt_bootstrap' folder is missing...
        return 1,

    from frt_bootstrap.boot_low import get_boot_defaults

    # Starting system's initialization...
    loc_name, defaults = get_boot_defaults(location)
    return boot_interface(loc_name, defaults, read, write)
