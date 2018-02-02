# 弹幕请求地址：http://comment.bilibili.com/<cid>.xml

# http://comment.bilibili.com/rolldate,<cid>
# 后面的数字是cid
# 这个请求会返回视频每天分别新增弹幕数：

# http://comment.bilibili.com/dmroll,1414944000,2543804
# 1414944000就是2014-11-03 00:00，2543804是视频cid

# Third-party API
# https://bili.b612.in/api/?type=usermid&hash=<sender_hash>

from json import JSONDecodeError
from data.DanmakuList import DanmakuList
import requests
from data.Video import Video

DEBUG = True
UNDEFINED = -666


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
        raise ValueError('Failed to get the video chapter cid for aid #%d, login required. (Not supported yet)' % aid)


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
    from util.Util import timestamp_to_datetime
    pools = get_history_danmaku_pools(cid)
    timestamps = [timestamp[0] for timestamp in pools]
    _p('Got history data pools list: ' + str(timestamps))
    d_list = get_history_danmaku_list(cid, timestamps[0])
    _p('Got history data pool ' + timestamp_to_datetime(timestamps[0]))
    i = 1
    while i < len(timestamps) and not (i > max_pools >= 1):
        d_list_new = get_history_danmaku_list(cid, timestamps[i])
        _p('Got history data pool ' + timestamp_to_datetime(timestamps[i]))
        d_list.merge(d_list_new)
        i += 1
    return d_list


def get_uid(sender_hash: str) -> list:
    # Third-party API
    received = requests.get('http://biliquery.typcn.com/api/user/hash/%s' % sender_hash).json().get('data')
    uids = [id.get('id') for id in received]
    return uids


def get_video_stat_by_aid(aid: int):
    '''
    Bilibili video statistic API
    :param aid: the av number of the video
    :return: aid, view, danmaku, reply, favourite, coin, share, now_rank, his_rank, like, no_reprint, copyright
    '''
    received = requests.get('http://api.bilibili.com/archive_stat/stat?aid=%d' % aid).json().get('data')
    return received


def get_video_info_by_aid(aid: int):
    '''
    Bilibili video playing site analysing
    :param aid: the av number of the video
    :return: title, description, author_name
    '''
    received = requests.get('https://www.bilibili.com/video/av%d/' % aid).content.decode()

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(received, 'html.parser')
    any = True

    title = soup.find(name='h1', attrs={'title': any}).string
    description = soup.find(name='div', attrs={'id': 'v_desc'}).string
    author_name = soup.find(name='a', attrs={'class': 'name'}).string

    return {'title':title, 'description':description, 'author_name':author_name}



TID = {'All': 0, 'Animation': 1, 'Guochuang': 168, 'Music': 3, 'Dancing': 129, 'Gaming': 4, 'Tech': 36, 'Life': 160,
       'OtoMAD': 119, 'Fashion': 155, 'Entertainment': 5, 'Movie&TV': 181}
TIME_RANGE = {'Today': 1, 'Three_days': 3, 'Week': 7, 'Month': 30}


def get_ranking_video_aids(tid: int = TID.get('All'), time_range: int = TIME_RANGE.get('Three_days'),
                           recent: bool = False):
    if recent:
        recent = '0'
    else:
        recent = ''
    received = \
        requests.get('https://www.bilibili.com/index/rank/all-%s%d-%d.json' % (recent, time_range, tid)).json()['rank'][
            'list']
    aids = []
    for video in received:
        aids.append(int(video.get('aid')))
    return aids


if __name__ == '__main__':
    video = get_video_info_by_aid(18900448)
