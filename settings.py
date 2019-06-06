PHAB_BASE_URL = 'https://secure.phabricator.com'
PHAB_DEFAULT_PROJECT = None
PHAB_AUTHORS = None

# allow custom over rides NOT checked in to git (in .gitignore)
# to use, create a settings_override.py file and duplicate the
# subset of settings you wish to over-ride there
try:
    from settings_override import *
except ImportError:
    pass
