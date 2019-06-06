# differential-comments: Display Differential code review comments for a team

## Quickstart

```bash
virtualenv .virtualenv
source .virtualenv/bin/activate
pip install -r requirements.txt
python differential-comments.py --help
```

### Authenticate to Phabricator

Phabricator authentication should be automatic via your `~/.arcrc` credentials.
You can test it out by searching for Phabricator projects that match a certain
query string:

```bash
python differential-comments.py
```
