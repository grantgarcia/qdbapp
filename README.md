qdbapp
======

A minimal IRC quote database for Django.  Anonymous voting is done via [django-secretballot](https://github.com/sunlightlabs/django-secretballot).  Quotes can be searched and filtered by user and channel, as well as sorted by most recent and highest voted.  The frontend uses Bootstrap almost exclusively.

Setup
-----

qdbapp uses Python 2.7.  [requirements.txt][/requirements.txt] contains the list of dependencies.  virtualenv is recommended.

Copy [local\_settings\_example.py](/qdb/local_settings_example.py) to local\_settings.py and edit the configuration values accordingly.
