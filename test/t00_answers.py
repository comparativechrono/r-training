"""The short questions of the courses accept the answers they should, and not others. (No browser: the patterns are
tried here as tutorial.js tries them – on the answer in lower case, with its spaces tidied – with Python's re.)
Run:  python3 test/t00_answers.py"""
import re
import sys
from html.parser import HTMLParser
from student import check
import course_r_basics
import course_tidyverse


class Questions(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.q = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'data-q' in a and 'data-accept' in a:
            self.q[a['data-q']] = a['data-accept']


def norm(s):
    return re.sub(r'\s+', ' ', re.sub('[‐-―−]', '-', s.lower())).strip()


def accepts(pattern, answer):
    v = norm(answer)
    return any(re.search(a.strip(), v, re.I) for a in pattern.split('||') if a.strip())


GOOD = {
    'c-q-mult': ['2418', '2,418', ' 2418 '],
    'c-q-div': ['17', '17.0', '17.00'],
    'o-q-z': ['1.77', '1.773', '1.7727', '1.772727'],
    'f-q-log': ['5.598', '5.5977', '5.597686', '5.6', '5.597'],
    'v-q-last': ['299'],
    'vo-q-sub': ['-3 -1 1 4 7', '-3, -1, 1, 4, 7', '[1] -3 -1  1  4  7', '−3 −1 1 4 7'],
    'vo-q-last': ['299000', '299,000', '2.99e+05', '2.99e5'],
    'sv-q-count': ['50'],
    'ds-q-mon': ['0.6', '.6', '0.60'],
    'ds-q-pass': ['3'],
    'rd-q-median': ['6.23', '6.2277', '6.227664', '6.228'],
    'rd-q-mean': ['59.88', '59.882', '59.88219', '59.9'],
    'rd-q-sd': ['24.12', '24.117', '24.11675', '24.1'],
    'fl-q-80': ['16'],
    'fl-q-gene': ['17'],
    'pp-q-quality': ['3961', '3,961'],
    'pp-q-dbsnp': ['23690', '23,690'],
    'mo-q-ref': ['G', 'g', 'G (6982)'],
    'lb-q-p': ['2.44e-06', '2.44e-6', '0.00000244', '2.44 x 10^-6', '2.44×10-6'],
}
BAD = {
    'c-q-mult': ['2408', '24180', '31*78'],
    'c-q-div': ['16', '170', '1.7'],
    'o-q-z': ['1.78', '1.7', '17.7'],
    'f-q-log': ['5.59', '48.43', '5.7'],
    'v-q-last': ['300', '2990'],
    'vo-q-sub': ['3 1 -1 -4 -7', '-3 -1 1 4'],
    'vo-q-last': ['299', '2990000'],
    'sv-q-count': ['49', '500'],
    'ds-q-mon': ['6', '0.66'],
    'ds-q-pass': ['2', '30'],
    'rd-q-median': ['6.3', '72', '6'],
    'rd-q-mean': ['59', '60', '24.12'],
    'rd-q-sd': ['24', '59.88', '24.2'],
    'fl-q-80': ['15', '160'],
    'fl-q-gene': ['16', '170'],
    'pp-q-quality': ['396', '39610'],
    'pp-q-dbsnp': ['2369', '25822'],
    'mo-q-ref': ['C', 'A', 'GC'],
    'lb-q-p': ['2.44', '0.77', '2.44e-05'],
}

found = {}
for mod in (course_r_basics, course_tidyverse):
    p = Questions()
    p.feed('\n'.join(mod.ALL()))
    found.update(p.q)

check(set(found) == set(GOOD), f'every short question is tried here ({sorted(set(found) ^ set(GOOD))})')
for qid, pattern in sorted(found.items()):
    for a in GOOD.get(qid, []):
        check(accepts(pattern, a), f'{qid} accepts {a!r}')
    for a in BAD.get(qid, []):
        check(not accepts(pattern, a), f'{qid} does not accept {a!r}')
print('failed:', check.failed)
sys.exit(1 if check.failed else 0)
