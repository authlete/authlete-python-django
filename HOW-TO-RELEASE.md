HOW TO RELEASE
==============

    $ vi pyproject.toml
        # Update 'version'.
    $ git add pyproject.toml
    $ git commit

    $ make clean
    $ make test
    $ make dist
    $ make release

    $ git tag authlete-python-django-{version}
    $ git push origin authlete-python-django-{version}
