PHAB_BASE_URL = 'https://secure.phabricator.com'

TEAMS = {
    'team1': [
        'foo@example.com',
    ],
}

DEFAULT_TEAM = 'team1'

DIFF_STATUS = [
    'changes-planned',
    'needs-review',
    'needs-revision',
    'accepted',
]

# allow custom over rides NOT checked in to git (in .gitignore)
# to use, create a settings_override.py file and duplicate the
# subset of settings you wish to over-ride there
try:
    from settings_override import *
except ImportError:
    pass
