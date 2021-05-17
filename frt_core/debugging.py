
# Author: Kirill Leontyev (DC)



class Debugger:

    __slots__ = (
        'print_p_debug_info', 'print_c_debug_info', 'print_e_debug_info'
    )

    # Ref: (int, ...) -> Debugger
    def __new__(cls, dbg_code, *args):
        return object.__new__(cls) if dbg_code else None

    # Ref: (int, extends<io,IOBase>) -> none
    def __init__(self, dbg_code, write):
        if self:

            if dbg_code & 0x00000001:

                def _print_p_debug_info():
                    write("")

                self.print_p_debug_info = _print_p_debug_info
            else:
                self.print_p_debug_info = lambda: None

            if dbg_code & 0x00000002:

                def _print_c_debug_info():
                    write.write("")

                self.print_c_debug_info = _print_c_debug_info
            else:
                self.print_c_debug_info = lambda: None

            if dbg_code & 0x00000004:

                def _print_e_debug_info():
                    write.write("")

                self.print_e_debug_info = _print_e_debug_info
            else:
                self.print_e_debug_info = lambda: None
