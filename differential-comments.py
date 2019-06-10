import argparse
from collections import Counter

import colorama

import cache
import lib_phab
import settings


def kwargs_or_default(setting_value):
    if setting_value:
        return dict(default=setting_value)
    return dict(required=True)


def list(args):
    author_phids = lib_phab.get_author_phids(settings.TEAM_EMAILS)
    counts = Counter()
    for diff in lib_phab.get_diffs(author_phids, args.days):
        # import ipdb; ipdb.set_trace()
        diff_phid = diff.get('id')
        fields = diff.get('fields')
        diff_author_phid = fields.get('authorPHID')
        diff_author = lib_phab.phid_to_name(diff_author_phid)
        #print '%s (%s) "%s"' % (diff_phid, author, fields.get('title'))
        comments = lib_phab.get_comments(diff_phid, author_phids, diff_author_phid)
        if not comments:
            continue
        if not args.just_tally:
            print '=== %s ===' % (
                lib_phab.phab_url('D%s' % diff_phid),
            )
        for comment in comments:
            comment_author = lib_phab.phid_to_name(comment.get('authorPHID'))
            comment_text = comment.get('comments')
            if not args.just_tally:
                print "> %s: @%s\n%s%s\n" % (
                    comment_author,
                    diff_author,
                    colorama.Fore.CYAN,
                    comment_text,
                )
            counts[comment_author] += 1
            if args.just_tally:
                print '.',
    if args.just_tally:
        print ''
    print counts


if __name__ == '__main__':
    colorama.init(autoreset=True)
    cache.load()
    parser = argparse.ArgumentParser(prog='differential-comments')
    parser.add_argument('--emails', help='Phabricator team PHID',
        **kwargs_or_default(settings.TEAM_EMAILS))
    parser.add_argument('--days', help='How many days back to go')
    parser.add_argument('--just-tally', help='Just print the final tally', action='store_true')
    args = parser.parse_args()
    list(args)
    cache.update()
