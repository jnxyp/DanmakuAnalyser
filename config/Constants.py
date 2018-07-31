import os

DANMAKU_TYPES = {'Rolling_1': 1, 'Rolling_2': 2, 'Rolling_3': 3, 'Bottom': 4, 'Top': 5,
                 'Reverse': 6,
                 'Advanced_mode_7': 7,
                 'Advanced_mode_8': 8}
DANMAKU_SIZES = {'XXS': 12, 'XS': 16, 'S': 18, 'M': 25, 'L': 36, 'XL': 45, 'XXL': 64}
DANMAKU_POOLS = {'NORMAL': 0, 'SUBTITLE': 1, 'SPECIAL': 2}

# 分区ID
TID = {'All': 0, 'Animation': 1, 'Guochuang': 168, 'Music': 3, 'Dancing': 129, 'Gaming': 4,
       'Tech': 36, 'Life': 160,
       'OtoMAD': 119, 'Fashion': 155, 'Entertainment': 5, 'Movie&TV': 181}
# 排行榜时间范围
TIME_RANGE = {'Today': 1, 'Three_days': 3, 'Week': 7, 'Month': 30}

UNDEFINED = -666
DEBUG = False
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
