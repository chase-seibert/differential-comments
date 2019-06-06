from datetime import datetime

from phabricator import Phabricator

import cache
import settings


def phid_to_name(phid):
    if phid is None:
        return None
    if cache.has(phid):
        return cache.get(phid)
    phab = Phabricator()
    data = phab.phid.lookup(names=[phid, ])
    name = data[phid]['name']
    cache.set(phid, name)
    return name


def phab_timestamp_to_date(timestamp):
    if timestamp is None:
        return None
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def phab_url(phid):
    return '%s/%s' % (settings.PHAB_BASE_URL, phid)


def get_author_phids(emails):
    phab = Phabricator()
    data = phab.user.query(emails=emails)
    return [d['phid'] for d in data]


def get_diffs(author_phids, statuses):
    phab = Phabricator()
    constraints = {
        'authorPHIDs': author_phids,
        'statuses': statuses,
        #'createdStart':

    }
    results = phab.differential.revision.search(
        constraints=constraints,
        #order='newest',
    )
    # import ipdb; ipdb.set_trace()
    # dateCreated 1559798204
    # diffPHID
    # title
    return results.get('data')


def get_comments(phid, author_phids, exclude_author_phid):
    phab = Phabricator()
    transactions = phab.transaction.search(
        objectIdentifier='D%s' % phid,
        constraints={
            'authorPHIDs': author_phids,
        }
    )
    comments = []
    for transaction in transactions.get('data'):
        if not transaction.get('comments'):
            continue
        author_phid = transaction.get('authorPHID')
        if author_phid == exclude_author_phid:
            continue
        comments.append(
            {
                'authorPHID': author_phid,
                'comments': transaction.get('comments')[0].get('content').get('raw'),
            })
    list.reverse(comments)
    return comments