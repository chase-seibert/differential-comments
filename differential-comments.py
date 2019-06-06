import argparse
from collections import Counter

import colorama

import lib_phab
import settings


def kwargs_or_default(setting_value):
    if setting_value:
        return dict(default=setting_value)
    return dict(required=True)


def list(args):
    author_phids = lib_phab.get_author_phids(settings.TEAM_EMAILS)
    counts = Counter()
    for diff in lib_phab.get_diffs(author_phids, settings.DIFF_STATUS):
        # import ipdb; ipdb.set_trace()
        diff_phid = diff.get('id')
        fields = diff.get('fields')
        diff_author_phid = fields.get('authorPHID')
        diff_author = lib_phab.phid_to_name(diff_author_phid)
        #print '%s (%s) "%s"' % (diff_phid, author, fields.get('title'))
        comments = lib_phab.get_comments(diff_phid, author_phids, diff_author_phid)
        if not comments:
            continue
        print '=== %s ===' % (
            lib_phab.phab_url('D%s' % diff_phid),
        )
        for comment in comments:
            comment_author = lib_phab.phid_to_name(comment.get('authorPHID'))
            comment_text = comment.get('comments')
            print "> %s: @%s\n%s%s\n" % (
                comment_author,
                diff_author,
                colorama.Fore.CYAN,
                comment_text,
            )
            counts[comment_author] += 1
    print counts


if __name__ == '__main__':
    colorama.init(autoreset=True)
    parser = argparse.ArgumentParser(prog='differential-comments')
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_auth = subparsers.add_parser('list', help='List comments')
    #parser_auth.add_argument('--server', help='Phabricator Server URL',
    #    **kwargs_or_default(settings.PHAB_BASE_URL))
    #parser_auth.add_argument('--project', help='Phabricator Server URL',
    #    **kwargs_or_default(settings.PHAB_DEFAULT_PROJECT))
    #parser_auth.add_argument('--author', help='Phabricator team PHID',
    #    **kwargs_or_default(settings.PHAB_AUTHORS))
    parser_auth.add_argument('--emails', help='Phabricator team PHID',
        **kwargs_or_default(settings.TEAM_EMAILS))
    parser_auth.set_defaults(func=list)

    args = parser.parse_args()
    args.func(args)
