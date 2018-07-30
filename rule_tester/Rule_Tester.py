from model.Danmaku import Danmaku
from model.Rule import Rule
from util.Bili_API import *
from util.Util import parse_rule_xml_str
from model.Constants import *
from util.Mult_Thread import mult_thread_execute

def _p(s, end='\n'):
    if DEBUG:
        print(s, end=end)


def get_danmakus_from_ranking(limit: int = 10):
    aids = list(map(lambda x: x['aid'], get_ranking_video_info(recent=True)))[:limit]
    danmakus = []
    print('Loading danmakus: %d in total' % len(aids))
    total = len(aids)
    count = 0

    def _get_danmaku(aid: int):
        nonlocal count
        count += 1
        print_progress_bar(count, total)
        cid = get_cids_by_aid(aid)[0]
        return get_danmaku_list(cid).danmakus

    r = mult_thread_execute(_get_danmaku, len(aids), [[aid] for aid in aids], thread_number=6)

    print('')
    for danmaku in r:
        danmakus += danmaku

    return danmakus


def load_rule_list(
        url: str = 'https://raw.githubusercontent.com/jn'
                   'xyp/Bilibili-Block-List/master/API/test.xml') -> list:
    print('Loading rule list xml from %s' % url)
    print_progress_bar(0, 1)
    received = requests.get(url).content.decode()
    rules = parse_rule_xml_str(received)
    print_progress_bar(1, 1)
    print('')
    return rules


def record_match(rule: Rule, danmaku: Danmaku):
    if 'matched_danmaku' not in rule.__dict__:
        rule.matched_danmaku = {}
    if 'matched_rules' not in danmaku.__dict__:
        danmaku.matched_rules = {}
    matches = rule.match(danmaku)
    if len(matches) > 0:
        _p('Match found between rule ' + str(rule)[:20] + ' and danmaku ' + str(danmaku))
        rule.matched_danmaku[danmaku] = matches
        danmaku.matched_rules[rule] = matches


if __name__ == '__main__':
    danmakus = get_danmakus_from_ranking(20)
    rules = load_rule_list()
    total = len(rules)
    count = 0
    print('Recording machining')
    for rule in rules:
        count += 1
        print_progress_bar(count, total)
        for danmaku in danmakus:
            record_match(rule, danmaku)
