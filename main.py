# Author: Kirill Leontyev (DC)



# Preparations...
from os.path import abspath, split
from inspect import getsourcefile

# 1. We pass in-place defined lambda to os.path.getsourcefile => we get *THIS* file's name.
# 2. os.abspath provides us with the full name of *THIS* file.
# 3. os.split(...)[0] extracts catalogue's name.
location = split(abspath(getsourcefile(lambda: None)))[0]
del abspath, split, getsourcefile



import sys
from frt_bootstrap.boot_starter import boot
from frt_bootstrap.boot_cli import boot_interface
write = sys.stdout.write
flush = sys.stdout.flush
retcode, *others = boot(location, boot_interface, sys.stdin.readline, write)
del sys, boot, boot_interface



if retcode:
    from frt_bootstrap.boot_low import reduce_commas
    write(
        {
            1: """
Ошибка: не удалось проверить целостность системы: отсутствует папка 'frt_bootstrap'.
Error: system's integrity check has been failed due to loss of the 'frt_bootstrap' directory.
""",
            2: """
Ошибка: не удалось проверить целостность системы: отсутствует файл 'frt_bootstrap/boot_low.py'.
Error: system's integrity check has been failed due to loss of the 'frt_bootstrap/boot_low.py' file.
""",
            3: """
Ошибка: не удалось проверить целостность системы: файл 'frt_bootstrap/boot_low.py' повреждён.
Error: system's integrity check has been failed due to corruption of the 'frt_bootstrap/boot_low.py' file.
""",
            4: """
Ошибка: целостность системы нарушена.
Error: the system is corrupted.
Недостаёт: {0}.
Missing: {0}.
""".format(reduce_commas(others[0])),
            5: """
Ошибка: недостаёт следующих файлов локализации: {0}.
Error: the next localization files are missing: {0}.
""".format(reduce_commas(others[0])),
            6: """
Ошибка: недостаёт следующих кодовых страниц: {0}.
Error: the next code pages are missing: {0}.
""".format(reduce_commas(others[0])),
            7: """
Ошибка в аргументах командной строки.
Command line arguments error.
Ключ '{0}' должен сопровождаться одним из следующих значений: {1}.
A '{0}' key must be followed by one of these values: {1}.
""".format(others[0], reduce_commas(others[1])),
            8: """
Ошибка: запрашиваемый модуль локализации ('{0}') не найден.
Error: the requested localization module ('{0}') have not been found.
""".format(others[0]),
            9: """
Ошибка: запрашиваемый модуль локализации ('{0}') повреждён.
Error: the requested localization module ('{0}') has been corrupted.
""".format(others[0]),
            10: others[0],
            11: '',  # coder not found
            12: '',  # coder corrupted

        }.__getitem__(retcode)
    )
    flush()
    exit(retcode)

elif retcode is None:
    write(others[0])
    flush()
    exit(0)

else:
    vm = others[0]
    del retcode, others

    # Entering the main loop...
    from frt_bootstrap.boot_optags import get_optags
    from frt_bootstrap.boot_parser import get_parser
    from frt_bootstrap.boot_compiler import get_compiler
    from frt_bootstrap.boot_executor import get_executor

    t, o = get_optags()
    parse = get_parser(with_debug=True, get_dbg_msg=vm.localization.dbgs.__getitem__)
    compile_tagged = get_compiler(
        t, o, with_debug=True, get_dbg_msg=vm.localization.dbgs.__getitem__,
        widest_cell=max(map(lambda x: len(x[1]), vm.localization.dbgs.items()))
    )
    execute = get_executor(vm.state)

    tokens = input("> ").split()
    parsed = parse(tokens, 0, len(tokens), t, vm.state.words)
    print("\t-- Parsed --\n{}\n\t-- ------ --".format(parsed[2]))
    print("\t     ***")
    compiled = compile_tagged(parsed[1], t, o)
    print("\t-- Compiled --\n{}\n\t -- -------- --".format(compiled[1]))
    execute(compiled[0], o)
