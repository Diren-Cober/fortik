
    0. ABOUT LOCALIZATIONS
Localization files ('loc_*.py') are in 'frt_localization/localizations' catalogue.
All of them must contain five python-built-in dictionaries:
>	errs,
>   refs,
>	dbgs,
>	tags,
>	words.
The keys are pre-determined (look in existing 'loc_*.py' files).
Note: the default localization's name is hold in filed 'dfl_loc' of class 'frt_localization.locale.Locale'.


    1. HOW TO ADD YOUR LOCALIZATION
Creating your own localization follow the steps below.
1. Create file '/frt_localization/localizations/loc_{$YOUR_LOC_NAME}.py' (for example, '.../loc_mine.py').
2. Ensure the file to contain needed dictionaries with pre-determined keys; write your (string) values.
3. Find the 'loc_names' tuple in a Locale class scope in the 'frt_localization/locale.py' file, this tuple may look like
.. ('rus', 'eng'); add '$YOUR_LOC_NAME' to the tuple (after that it may look like ('rus', 'eng', 'mine')).

When the steps are done, if you add '--localization $YOUR_LOC_NAME' to command-line arguments, fortik will boot up
.. using the localization you mentioned.
In addition, fortik will check existence of 'frt_localization/localizations/loc_{$YOUR_LOC_NAME}.py' file every boot.


    2. HOW TO REMOVE A LOCALIZATION
If you'd like to remove a localization, your should both delete its file and remove its name from the 'loc_names' tuple.


    3. HOW TO DISABLE A LOCALIZATION
To disable a localization, you should remove its name from the 'loc_names' tuple.
If a localization is disabled, fortik knows nothing about it, thus, does not check its file's existence and
.. is not able to boot using it.


    4. HOW TO ENABLE AN EXISTING LOCALIZATION OR TO ADD ONE
Enabling an existing localization, you should simply add its name to the 'loc_names' tuple.
If the localization file does not exist, your also should add it in the 'frt_localization/localizations' folder.
