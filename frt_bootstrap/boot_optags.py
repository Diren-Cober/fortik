
# Author: Kirill Leontyev (DC)



def get_optags():

    class Tags:

        # Ref: <all>: object
        __slots__ = (
            'push', 'define', 'fork', 'loop_while', 'loop_for', 'clock_p', 'call'
        )

        # Ref: (object, object, object, object, object, object, object, object) -> none
        def __init__(
                self, push, define, fork, loop_while, loop_for, clock_p, call
        ):
            self.push   = push
            self.define = define
            self.fork   = fork
            self.loop_while = loop_while
            self.loop_for   = loop_for
            self.clock_p    = clock_p
            self.call   = call


    class Opcodes:

        # Ref: <all>: object
        __slots__ = (
            'push', 'call', 'move', 'fork', 'setup_cycle', 'check_cycle', 'clock', 'clock_p', 'define',
        )

        # Ref: (object, object, object, object, object, object, object, object) -> none
        def __init__(self, push, call, move, fork, setup_cycle, check_cycle, clock, clock_p, define):
            self.push = push
            self.call = call
            self.move = move
            self.fork = fork
            self.setup_cycle = setup_cycle
            self.check_cycle = check_cycle
            self.clock   = clock
            self.clock_p = clock_p
            self.define  = define


    o_push = object()
    o_call = object()
    o_fork = object()
    o_define = object()
    o_clock_f = object()

    t = Tags(o_push, o_define, o_fork, object(), object(), o_clock_f, o_call)
    o = Opcodes(o_push, o_call, object(), o_fork, object(), object(), object(), o_clock_f, o_define)

    return t, o
