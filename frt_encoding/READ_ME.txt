
    0. ABOUT CODE PAGES
Code page files ('cp_*.py') are in 'frt_encoding/code_pages' catalogue.
All of them must contain a 'cp' variable which is an iterable data structure (a list or a tuple; a tuple is better),
.. containing tuples consisting of a one-symbol string and an integer number.
This data structure describes the rule of encoding used by a coder.
Note: there is a code page without its own file, its name is 'python-built-in'; this code page implemented with use
.. of python builtin functions 'ord' and 'chr' covers ASCII encoding.


    1. HOW TO ADD YOUR CODE PAGE
Creating your own code page follow the steps below.
1. Create file 'frt_encoding/code_pages/cp_{$YOUR_CODE_PAGE_NAME}.py' (for example, '.../cp_mine.py').
2. Describe an encoding rule using tuple or some other iterable data structure.
3. Find the 'cp_names' tuple in a Coder class scope in the 'frt_encoding/coder.py' file, this tuple may look like
.. ('builtin',); add '$YOUR_CODE_PAGE_NAME' to the tuple (after that it may look like ('builtin', 'mine')).

When the steps are done, if you add '--code-page $YOUR_CODE_PAGE_NAME' to command-line arguments, fortik will boot up
.. using the code page you mentioned.
In addition, fortik will check existence of 'frt_encoding/code_pages/cp_{$YOUR_CODE_PAGE_NAME}.py' file every boot.


    2. HOW TO REMOVE A CODE PAGE
If you'd like to remove a code page, your should both delete its file and remove its name from the 'cp_names' tuple.


    3. HOW TO DISABLE A CODE PAGE
To disable a code page, you should remove its name from the 'cp_names' tuple.
If a code page is disabled, fortik knows nothing about it, thus, does not check its file's existence and
.. is not able to boot using it.


    4. HOW TO ENABLE AN EXISTING CODE PAGE OR TO ADD ONE
Enabling an existing code page, you should simply add its name to the 'cp_names' tuple.
If its file does not exist, your also should add it in the 'frt_encoding/code_pages' folder.
