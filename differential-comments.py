import argparse
from collections import Counter
import sys

import colorama

import cache
import lib_phab
import settings


def kwargs_or_default(setting_value):
    if setting_value:
        return dict(default=setting_value)
    return dict(required=True)


def list(args):
    team_emails = settings.TEAMS.get(args.team)
    if not team_emails:
        raise Exception('No emails configured for team %s' % args.team)
    team_phids = lib_phab.get_author_phids(team_emails)
    commentor_phids = team_phids
    if args.just_email:
        commentor_phids = lib_phab.get_author_phids([args.just_email, ])
    counts = Counter()
    diffs = lib_phab.get_diffs(team_phids, args.days)
    total_diffs = len(diffs)
    for diff in diffs:
        # import ipdb; ipdb.set_trace()
        diff_phid = diff.get('id')
        fields = diff.get('fields')
        diff_author_phid = fields.get('authorPHID')
        diff_author = lib_phab.phid_to_name(diff_author_phid)
        #print '%s (%s) "%s"' % (diff_phid, author, fields.get('title'))
        comments = lib_phab.get_comments(diff_phid, commentor_phids, diff_author_phid, args.comment_days)
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
                sys.stdout.write('.')
                sys.stdout.flush()
    if args.just_tally:
        print ''
    print '=== Counts ==='
    for key, value in counts.items():
        print '%s: %s' % (key, value)
    print 'Total: %s comments on %s diffs' % (sum(counts.values()), total_diffs)


if __name__ == '__main__':
    colorama.init(autoreset=True)
    cache.load()
    parser = argparse.ArgumentParser(prog='differential-comments')
    parser.add_argument('--team', help='Which team from settings to use',
        **kwargs_or_default(settings.DEFAULT_TEAM))
    parser.add_argument('--days', help='How many days back to go', default=30)
    parser.add_argument('--comment-days', help='How many days back to go for the comments')
    parser.add_argument('--just-tally', help='Just print the final tally', action='store_true')
    parser.add_argument('--just-email', help='Just one user by email address')
    args = parser.parse_args()
    list(args)
    cache.update()
