HOW TO RELEASE
==============

    $ vi setup.py
        # Update 'version'.
        # Update 'packages' if necessary.
    $ git add setup.py
    $ git commit

    $ make clean
    $ make test
    $ make dist
    $ make release

