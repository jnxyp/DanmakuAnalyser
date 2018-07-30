# Danmaku Format
# example:
# <d p="1830.6300048828,1,25,16777215,1415241251,0,Da8b0a0d,668464499">再见了我的青春</d>
#              1        2  3     4        5      6    7         8            9
# 1. 弹幕发送相对视频的时间（以前是以秒为单位的整数，现在用浮点记了，更精准）
# 2. 弹幕类型：1~3（但貌似只见过1）滚动弹幕、4底端弹幕、5顶端弹幕、6逆向弹幕、7精准定位、8高级弹幕【默认是1，基本以1、4、5多见】
# 3. 字号：12非常小,16特小,18小,25中,36大,45很大,64特别大【默认是25】
# 4. 字体颜色：不是RGB而是十进制
# 5. 弹幕发送时的UNIX时间戳，基准时间1970-1-1 08:00:00
# 6. 弹幕池类型：0普通 1字幕 2特殊
# 7. 发送者ID【注意不是uid，具体怎么关联的还不清楚，屏蔽用】
# 8. 弹幕在数据库的ID
import uuid
from model.Constants import *

class Danmaku:
    appear_time = 0.0
    d_type = 1
    size = 25
    color = 0
    timestamp = 0
    pool = 0
    sender_hash = ''
    did = 0
    content = ''

    def __init__(self, appear_time: float, d_type: int, size: int, color: int, timestamp: int,
                 pool: int,
                 sender_hash: str, did: int, content: str):
        self.appear_time = appear_time
        self.type = d_type
        self.size = size
        self.color = color
        self.timestamp = timestamp
        self.pool = pool
        self.sender_hash = sender_hash
        if type(did) is str:
            self.did = int(did)
        else:
            self.did = did
        self.content = content
        if self.content is None:
            self.content = ''

    def __str__(self):
        return self.content

    def __eq__(self, other):
        return self.did == other.did

    def __lt__(self, other):
        return self.did < other.did

    def __gt__(self, other):
        return self.did > other.did

    def __hash__(self):
        return self.did

    @staticmethod
    def create_instance(appear_time: float = 0, d_type: int = 1, size: int = DANMAKU_SIZES.get('M'),
                        color: int = 0,
                        timestamp: int = 0, pool: int = 0,
                        sender_hash: str = '', did: int = uuid.uuid1().__int__(),
                        content: str = ''):
        return Danmaku(appear_time, d_type, size, color, timestamp, pool, sender_hash, did, content)


if __name__ == '__main__':
    l1 = [Danmaku.create_instance(did=1), Danmaku.create_instance(), Danmaku.create_instance(),
          Danmaku.create_instance()]
    l2 = [Danmaku.create_instance(did=1)]
    print(l2[0] in l1)
