
# Author: Kirill Leontyev (DC)



class Settings:

    __slots__ = ()

    # Ref: (int) -> Settings
    @staticmethod
    def get(code):
        return Settings_factory.get(code, Debugger_settings, Compiler_settings, VM_settings)



class Settings_factory:

    __slots__ = ()

    current_mask = 0x00000001

    # Ref: (iterable<type>, int) -> iterable<type::instance>
    @classmethod
    def get(cls, code, *classes):
        g_bool = bool
        res = []

        for _class in classes:
            obj = object.__new__(_class)
            for slot in _class.__slots__:
                obj.__setattr__(slot, g_bool(code & cls.current_mask))
                cls.current_mask <<= 1
            res.append(obj)

        return res


class Debugger_settings:
    # Ref: <all> bool
    __slots__ = ('do_debug_parsing', 'do_debug_compilation', 'do_debug_execution')


class Compiler_settings:
    # Ref: <all> bool
    __slots__ = ('do_optimize_code', 'do_inline_calls')


class VM_settings:
    # Ref: <all> bool
    __slots__ = ('do_disable_gc','do_block_interrupts')
