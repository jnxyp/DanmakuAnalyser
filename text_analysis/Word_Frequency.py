import operator
import re

from danmaku.Util import *
import jieba

CHINESE_CHARACTERS = re.compile('[\u4e00-\u9fa5]+')
AID = 17977214

danmakus = get_danmaku_list(get_cids(AID)[0]).get_danmaku_contents()

chinese_danmakus = []
for d in danmakus:
    m = CHINESE_CHARACTERS.findall(d)
    if m:
        for w in m:
            chinese_danmakus.append(w)
danmaku_words = {}
for d in chinese_danmakus:
    words = jieba.lcut(d)
    for w in words:
        if w not in danmaku_words.keys():
            danmaku_words[w] = 1
        else:
            danmaku_words[w] += 1

sorted_x = sorted(danmaku_words.items(), key=operator.itemgetter(1))
sorted_x.reverse()
print(sorted_x)