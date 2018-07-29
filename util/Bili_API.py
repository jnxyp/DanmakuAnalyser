# 弹幕请求地址：http://comment.bilibili.com/<cid>.xml

# http://comment.bilibili.com/rolldate,<cid>
# 后面的数字是cid
# 这个请求会返回视频每天分别新增弹幕数：

# http://comment.bilibili.com/dmroll,1414944000,2543804
# 1414944000就是2014-11-03 00:00，2543804是视频cid

# Third-party API
# https://bili.b612.in/api/?type=usermid&hash=<sender_hash>

from json import JSONDecodeError

import re

from model.DanmakuList import DanmakuList
import requests

DEBUG = True
UNDEFINED = -666

# 分区ID
TID = {'All': 0, 'Animation': 1, 'Guochuang': 168, 'Music': 3, 'Dancing': 129, 'Gaming': 4,
       'Tech': 36, 'Life': 160,
       'OtoMAD': 119, 'Fashion': 155, 'Entertainment': 5, 'Movie&TV': 181}
# 排行榜时间范围
TIME_RANGE = {'Today': 1, 'Three_days': 3, 'Week': 7, 'Month': 30}


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

def _p(s, end='\n'):
    if DEBUG:
        print(s, end=end)


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
        raise ValueError(
            'Failed to get the video chapter cid for aid #%d, login required. (Not supported yet)' % aid)


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
    received = requests.get(
        'http://comment.bilibili.com/dmroll,%d,%d' % (timestamp, cid)).content.decode()
    return DanmakuList.parse(received)


def get_history_danmaku_lists(cid: int, max_pools: int = -1):
    from util.Util import timestamp_to_datetime
    pools = get_history_danmaku_pools(cid)
    timestamps = [timestamp[0] for timestamp in pools]
    _p('Got history model pools list: ' + str(timestamps))
    d_list = get_history_danmaku_list(cid, timestamps[0])
    _p('Got history model pool ' + timestamp_to_datetime(timestamps[0]))
    j = 1
    while j < len(timestamps) and not (j > max_pools >= 1):
        d_list_new = get_history_danmaku_list(cid, timestamps[j])
        _p('Got history model pool ' + timestamp_to_datetime(timestamps[j]))
        d_list.merge(d_list_new)
        j += 1
    return d_list


def get_uid(sender_hash: str) -> list:
    '''
    Third-party user ID query API
    :param sender_hash: the hash value in Danmaku list
    :return: the sender's uid
    '''
    received = requests.get('http://biliquery.typcn.com/api/user/hash/%s' % sender_hash).json().get(
        'model')
    uids = [id.get('id') for id in received]
    return uids


def get_video_stat_by_aid(aid: int) -> dict:
    '''
    Bilibili video statistic API
    :param aid: the av number of the video
    :return: dict{aid, view, danmaku, reply, favourite, coin, share, now_rank, his_rank, like, no_reprint, copyright}
    '''
    received = requests.get('http://api.bilibili.com/archive_stat/stat?aid=%d' % aid).json().get(
        'model')
    return received


def get_video_info_by_aid(aid: int) -> dict:
    '''
    Bilibili video playing site analysing
    :param aid: the av number of the video
    :return: dict{title, description, author_name, author_id}
    '''
    received = requests.get('https://www.bilibili.com/video/av%d/' % aid).content.decode()

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(received, 'html.parser')
    any = True

    # Title
    title = soup.find(name='h1', attrs={'title': any})['title']

    # Description
    # description = soup.find(name='div', attrs={'id': 'v_desc'}).string
    description = soup.find(name='meta', attrs={'name': 'description'})['content']

    # Author Name
    # author_name = soup.find(name='a', attrs={'class': 'name'}).string
    author_name = soup.find(name='meta', attrs={'name': 'author'})['content']

    # Author ID
    try:
        author_id = int(soup.find(name='a', attrs={'class': 'name'})['mid'])
    except KeyError:
        author_id = int(
            soup.find(name='a', attrs={'href': re.compile('space\.bilibili\.com')})['href'].split(
                '/')[-1])

    return {'title': title, 'description': description, 'author_name': author_name,
            'author_id': author_id}


def get_ranking_video_info(tid: int = TID['All'],
                           time_range: int = TIME_RANGE['Three_days'],
                           recent: bool = False):
    '''
    Get the information of videos from Bilbili rank
    :param tid: Thread ID, refer to TID
    :param time_range: valid time range for rankings, refer to TIME_RANGE
    :param recent: Set to True if only want to include the video uploaded within specific time range
    :return: list[dict{aid, author_name, coin, duration, author_id, pic, view, title, reply}]
    '''
    if recent:
        recent = '0'
    else:
        recent = ''
    received = \
        requests.get('https://www.bilibili.com/index/rank/all-%s%d-%d.json' % (
            recent, time_range, tid)).json()['rank'][
            'list']

    def mmss2s(s: str):
        s = s.split(':')
        return int(s[0]) * 60 + int(s[1])

    videos = []
    for video in received:
        videos.append(
            {'aid': int(video.get('aid')), 'author_name': video.get('author'),
             'coin': video.get('coins'),
             'duration': mmss2s(video.get('duration')), 'author_id': video.get('mid'),
             'pic': video.get('pic'),
             'view': video.get('play'), 'title': video.get('title'),
             'reply': video.get('video_review')})
    return videos


# TODO Searching API
# TODO User Information API

if __name__ == '__main__':
    for i in get_ranking_video_info():
        print(i)
