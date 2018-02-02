# http://api.bilibili.com/archive_stat/stat?aid=<aid>


UNDEFINED = -666


class Video:
    aid = 0
    view = 0
    danmaku = 0
    reply = 0
    favorite = 0
    coin = 0
    share = 0
    now_rank = 0
    his_rank = 0
    like = 0
    no_reprint = 0
    copyright = 0
    author_id = 0
    title = ''
    cids = []
    description = ''
    author_name = ''

    def __init__(self, aid: int, view: int, danmaku: int, reply: int, favourite: int, coin: int,
                 share: int, now_rank: int, his_rank: int, like: int, no_reprint: int, copyright: int, author_id: int,
                 title: str, cids: list, description: str, author_name: str):
        self.aid = aid
        self.view = view
        self.danmaku = danmaku
        self.reply = reply
        self.favourite = favourite
        self.coin = coin
        self.share = share
        self.now_rank = now_rank
        self.his_rank = his_rank
        self.like = like
        self.no_reprint = no_reprint
        self.copyright = copyright
        self.author_id = author_id
        self.title = title
        self.cids = cids
        self.description = description
        self.author_name = author_name

    @staticmethod
    def create_instance(aid: int = UNDEFINED, view: int = UNDEFINED, danmaku: int = UNDEFINED,
                        reply: int = UNDEFINED, favourite: int = UNDEFINED, coin: int = UNDEFINED,
                        share: int = UNDEFINED, now_rank: int = UNDEFINED, his_rank: int = UNDEFINED,
                        like: int = UNDEFINED, no_reprint: int = UNDEFINED, copyright: int = UNDEFINED,
                        author_id: int = UNDEFINED, title: str = '', cids: list = None, description: str = '',
                        author_name: str = '', auto_fill: bool = False):
        if auto_fill:
            # if cids is not given, get cids by video's aid.
            if cids is None:
                from util.Bili_API import get_cids
                cids = get_cids(aid)

        if cids is None:
            cids = []
        return Video(aid, view, danmaku, reply, favourite, coin, share, now_rank, his_rank, like, no_reprint, copyright,
                     author_id, title, cids, description, author_name)
