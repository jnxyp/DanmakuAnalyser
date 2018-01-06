import xml.etree.ElementTree as Et

from danmaku.Danmaku import Danmaku


class DanmakuList:
    chat_server = ''
    cid = 0
    mission = 0
    max_limit = 0
    real_name = ''
    source = ''
    danmakus = []

    def __init__(self, chat_server: str, cid: int, mission: int, max_limit: int, real_name: str, source: str,
                 danmakus: list):
        self.chat_server = chat_server
        self.cid = cid
        self.mission = mission
        self.max_limit = max_limit
        self.real_name = real_name
        self.source = source
        self.danmakus = danmakus

    @staticmethod
    def parse(s: str):
        root = Et.fromstring(s)
        danmakus = []
        for node in root.findall('d'):
            properties = node.attrib.get('p').split(',')
            content = node.text
            danmaku = Danmaku(*properties, content)
            danmakus.append(danmaku)
        return DanmakuList(root.findtext('chatserver'), root.findtext('chatid'), root.findtext('mission'),
                           root.findtext('maxlimit'), root.findtext('realname'), root.findtext('source'), danmakus)

    def merge(self, d_list):
        if self.cid == d_list.cid:
            self.danmakus = list(set(self.danmakus) | set(d_list.danmakus))
        else:
            print('Cannot perform merging: two Danmaku Lists have different cid.')

    def get_danmaku_ids(self):
        dids = []
        for d in self.danmakus:
            dids.append(d.did)
        return dids


if __name__ == '__main__':
    with open('10086.xml', encoding='utf-8') as f:
        s = f.read()
    l = DanmakuList.parse(s)
    print(*l.danmakus)
