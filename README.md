# differential-comments: Display Differential code review comments for a team

## Quickstart

```bash
virtualenv .virtualenv
source .virtualenv/bin/activate
pip install -r requirements.txt
python differential-comments.py --help
```

### Configure

Create a `settings_override.py`, and include the following:

```bash
PHAB_BASE_URL = 'https://secure.phabricator.com'

TEAM_EMAILS = [
    'foo@example.com',
]
```

If you want to specify a specific set of diff statues, you can define `DIFF_STATUS`.

### List Comments

Phabricator authentication should be automatic via your `~/.arcrc` credentials.

```bash
python differential-comments.py list
```
