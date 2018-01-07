import re

from danmaku.Util import *
from text_analysis.Edit_Distance import calc_similarities

CHINESE_CHARACTERS = re.compile('[\u4e00-\u9fa5]+')
AID = 17977214

danmakus = get_danmaku_list(get_cids(AID)[0]).get_danmaku_contents()

chinese_danmakus = []
for d in danmakus:
    m = CHINESE_CHARACTERS.findall(d)
    if m:
        s = ''
        for w in m:
            s += w
        chinese_danmakus.append(s)

def similarity_merging(strings:list, min_sim:int = 0.7):
    merged = []
    i = 0
    while i < len(strings):
        merged.append(strings[i])
        j = i + 1
        while j < len(strings):
            if calc_similarities(strings[i], strings[j]) >= min_sim:
                strings.pop(j)
            else:
                j += 1
        i += 1
    return merged

print(similarity_merging(['aaab','aaaa']))