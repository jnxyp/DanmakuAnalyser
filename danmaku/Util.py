# 弹幕请求地址：http://comment.bilibili.com/<cid>.xml

# http://comment.bilibili.com/rolldate,<cid>
# 后面的数字是cid
# 这个请求会返回视频每天分别新增弹幕数：

# http://comment.bilibili.com/dmroll,1414944000,2543804
# 1414944000就是2014-11-03 00:00，2543804是视频cid

# Third-party API
# https://bili.b612.in/api/?type=usermid&hash=<sender_hash>

DEBUG = True
UNDEFINED = -666

from json import JSONDecodeError
from danmaku.DanmakuList import DanmakuList
from danmaku.Danmaku import Danmaku
import requests

# HEADERS = {'Host': 'comment.bilibili.com',
#            'Connection': 'keep-alive',
#            'Pragma': 'no-cache',
#            'Cache-Control': 'no-cache',
#            'Upgrade-Insecure-Requests': '1',
#            'User-Agent': 'Mozilla/6.6 (Windows NT 11.0; Win128; x128) AppleWebKit/666.66 (KHTML, like Gecko) Chrome/66.6.6666.66 Safari/666.66',
#            'Accept': 'text/html,application/xhtml+xml,application/xml',
#            'DNT': '1',
#            'Accept-Encoding': 'gzip, deflate',
#            'Accept-Language': 'zh-CN,zh;'}

DEBUG = True

def _p(s):
    if DEBUG:
        print(s)


def get_danmaku_list(cid: int):
    received = requests.get('http://comment.bilibili.com/%d.xml' % cid).content.decode()
    return DanmakuList.parse(received)


def get_danmaku_list_from_file(path: str, encoding: str = 'utf-8'):
    with open(path, encoding=encoding) as f:
        s = f.read()
    return DanmakuList.parse(s)


def get_cids(aid: int):
    try:
        received = requests.get('http://www.bilibili.com/widget/getPageList?aid=%d' % aid).json()
        aids = []
        for p in received:
            aids.append(p.get('cid'))
        return aids
    except JSONDecodeError as e:
        print('Failed to get the video chapter cid for aid #%d, login required. (Not supported yet)' % aid)
        return []


def get_history_danmaku_pools(cid: int, skipping_threshold: int = 1000):
    received = requests.get('http://comment.bilibili.com/rolldate,%d' % cid).json()
    pools = []
    for pool in received:
        pools.append((int(pool.get('timestamp')), int(pool.get('new'))))
    if skipping_threshold <= 0:
        return pools
    else:
        major_pools = [pools[0]]
        changes = 0
        for pool in pools[1:]:
            changes += pool[1]
            if changes > skipping_threshold:
                major_pools.append(pool)
                changes = 0
        return major_pools


def get_history_danmaku_list(cid: int, timestamp: int):
    received = requests.get('http://comment.bilibili.com/dmroll,%d,%d' % (timestamp, cid)).content.decode()
    return DanmakuList.parse(received)


def get_all_history_danmaku_lists(cid: int, max_pools: int = -1):
    pools = get_history_danmaku_pools(cid)
    timestamps = [timestamp[0] for timestamp in pools]
    _p('Got history danmaku pools list: ' + str(timestamps))
    d_list = get_history_danmaku_list(cid, timestamps[0])
    _p('Got history danmaku pool ' + timestamp_to_datetime(timestamps[0]))
    i = 1
    while i < len(timestamps) and not (i > max_pools >= 1):
        d_list_new = get_history_danmaku_list(cid, timestamps[i])
        _p('Got history danmaku pool ' + timestamp_to_datetime(timestamps[i]))
        d_list.merge(d_list_new)
        i += 1
    return d_list

def get_uid(sender_hash:str):
    # Third-party API
    # received = requests.get('http://biliquery.typcn.com/api/user/hash/%s' % sender_hash).json()
    received = requests.get('https://bili.b612.in/api/?type=usermid&hash=%s' % sender_hash).content.decode()
    if received == '':
        return UNDEFINED
    return int(received)


def timestamp_to_datetime(stamp: int):
    import datetime
    return datetime.datetime.fromtimestamp(stamp).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    # l = parse_danmaku_list_from_bili(66478)
    # for danmaku in l.danmakus:
    #     print(danmaku)

    # l = parse_danamku_list_from_file('10086.xml')
    # for danmaku in l.danmakus:
    #     print(danmaku)

    # aids = parse_danmaku_list_from_bili(get_cids_by_aid(7)[0])
    # print(*aids.danmakus)

    # pool = get_history_danmaku_list_by_timestamp(2543804, list(get_history_danmaku_pools(2543804).keys())[0])
    # print(*pool.danmakus)

    # l = get_all_history_danmaku_lists(get_cids(1999286)[0])
    # s = ''
    # for d in l.danmakus:
    #     s += str(d) + '\n'
    # with open('dmk2.txt', 'w', encoding='utf-8') as f:
    #     f.write(s)

    print(get_uid('f9ff56e4'))
