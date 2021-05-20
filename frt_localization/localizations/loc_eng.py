
# Author: Kirill Leontyev (DC)

# Various error messages.
errs = {
    # Errors while parsing command-line arguments.
    'cli_syn'               : "Command line arguments' syntax error: {}.",  # Common first part of cli-startup error message.
    'cli_not-int'           : "'{}' key must be followed by an integer value",
    ######################### About formatting style: if a message is too long, go to new line and start with '.. '.
    'cli_bad-stack-size'    : "\n.. '{}' key ('{}' stack's size) must be followed by a positive integer not greater than {}",
    'cli_val-err'           : "'{}' key must be followed by one of the next values: {}",
    ################### Do not forget to escape curly braces in a combination template, because otherwise, the formatting crashes!
    'cli_dbg-val-err'       : "\n.. '{}' key must be followed by a combination ( {{<v1>[+<v2>[+<v3>]]}} ) of the next values: {}",
    'cli_unknown-key'       : "unknown key: '{}'",
    'cli_no-val'            : "the '{}' key must be followed by a value - none has been given"
}

# Short help references about basics.
refs = {
    ':g'    : """
Important: you silently considered to use python3 (version not less than 3.7 is strongly recommended).
Usage: main.py [<keys>...]; if no keys are given, all system settings have their default values.


\tKeys summary

0. { -h | --help }                  <str>   - prints refs and help information, possible values are:
                                                > { :g | :general }         * to see this,
                                                > { :c | :configuration }   * configuration details,
                                                > { :s | :syntax }          * syntax reference,
                                                > { :d | :debugging }       * about debugging modes,
                                                > { :w | :words }           * about some builtin words,
                                                > { :e | :errors }          * about errors
                                                > { [none] | [error] }      * equivalent to ':g'.

[<+int> - means 'positive int value'].
1. { -ns | --num-stack-size }       <+int>  - sets maximal size of the numeric stack.
2. { -nc | --num-stack-cell-type }  <str>   - [advanced, see --help :configuration for details].
3. { -rs | --ret-stack-size }       <+int>  - sets maximal size of the return stack.
4. { -rc | --ret-stack-cell-type }  <str>   - [advanced, see --help :configuration for details].
5. { -ct | --stacks-cell-type }     <str>   - [advanced, see --help :configuration for details].

6. { -cp | --code-page }            <str>   - sets code page used while encoding symbols manually.

7. { -d | --debug }                 <str>   - sets debug mode, see --help :debugging for details.

[to see next keys' description, pass --help :configuration].
8.  { -ngc | --disable-gc | --disable-garbage-collection }.
9.  { -pdc | --perform-deep-compilation }.
10. { -aip | --add-interrupt-protection }.
""",

    ':c'    : """
\tSystem configuration reference

*   Note 0 (about defaults)
There should be a 'frt_bootstrap/boot.config' file containing default configuration data.
This file is read, when the system boots up with no command-line arguments; if the system
.. is unable to find the file, the 'builtin' defaults is used
.. ( placed int frt_bootstrap.boot_low.get_boot_defaults ).

*   Note 1 (about stacks' cells and depths)
As you can see, we are able to change stacks' sizes and cell types. Why it can be useful?
There is an opinion that a good program written in Forth (Forth-like language)
.. uses not more than 5 cells of numeric stack. Of course, the defaults for numeric
.. and return stacks' sizes are bigger! =)
Configuring these values, you can set your own limits. Size of return stack, for example,
.. limits number of nested calls and size of stack cell limits size of numbers we use.
About cells: '-nc' and '-rc' keys must be followed by 'i8', or 'i16', or 'i32', or 'i64'.
('i*' - means 'signed integer of * bits').
So do the '-ct' key, it sets cell type for both numeric and return stacks.

*   Note 2 (about specific settings)
0) Appearing specific setting's key in command-line arguments sets the value to 'true'.
1) There is an experimental option of disabling python-built-in garbage collector. I am not sure
if there is no possible memory leaks in the system and I have no possibilities to make checks...
.. but, maybe, this option can be useful.
2) Enabling deep compilation, you forces the system to hold the code of newly defined words,
then you define a new word with their use, the system inlines their code instead of placing a
.. call sequence. This technique extremely reduces number of nested calls and nesting level,
.. but it has a price: new definitions become slower and explode memory consumption.
May lead to speedup, but should be used carefully.
3) Another experimental option is to add interrupt protection. Protection against keyboard
.. interrupt is meant. Main system functions are wrapped in a simple guard function.
May be useful then the system needed to be a sandbox, should be used carefully.

*   Note 3 (about structure of a configuration file)
The structure is rather simple. The file is read by line and any line considered to include
.. two words: a parameter and its value. The parameters' names are long forms of the
.. corresponding keys without '--' at the beginning.
The values are the same you can pass through command line, the exception is specific settings:
.. they should have values of this list: [true, True, false, False].
The parameter tag and its value is separated by 1+ whitespace character.
Everything behind '#' symbol considered to be a comment.
""",

    ':s'    : """
WIP
""",

    ':d'    : """
WIP
""",

    ':w'    : """
WIP
""",

    ':e'    : """
WIP
"""
}

# Messages printed in debug mode.
dbgs = {
    'push'      : 'push',
    'wdef'      : 'define',
    'fork'      : 'if-else',
    'lwhl'      : 'while',
    'lfor'      : 'for',
    'clck+'     : 'pop-next-iteration',
    'call'      : 'call',
    'move'      : 'jump-relatively',
    'cycle'     : 'setup-cycle',
    'cycle?'    : 'check-counter',
    'clck'      : 'next-iteration',
    'cycle>'    : 'Entering iteration',
    'cycle!'    : 'Exiting iteration',
    'output'    : 'Output: ',
    '>word'     : "Entering derived word '{}'",
    'word>'     : "Exiting derived word '{}'"
}

# Strings used in stringification of internal operations' tags.
tags = {

}

# And the main one - names in the system dictionary.
words = {

}
