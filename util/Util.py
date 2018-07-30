import sys
from time import sleep
from xml.dom.minidom import parseString
from model.Rule import Rule


def timestamp_to_datetime(stamp: int):
    import datetime
    return datetime.datetime.fromtimestamp(stamp).strftime('%Y-%m-%d %H:%M:%S')


def str_duration_to_second(s: str) -> int:
    '''
    Convert duration time from mm:ss to seconds
    :param s: mm:ss formatted duration string
    :return: duration time in seconds
    '''
    s = s.split(':')
    return int(s[0]) * 60 + int(s[1])


def print_progress_bar(progress: int, total: int, length: int = 100, border: tuple = ('[', ']'),
                       bar: str = '='):
    print('\r', end='')
    print(border[0], end='')
    print('=' * int(progress / total * length), end='')
    print(' ' * (length - int(progress / total * length)), end='')
    print(border[1], end='')
    print('\t', end='')
    print('%d/%d' % (progress, total), end='')
    sys.stdout.flush()


def parse_rule_xml_str(xml_string: str) -> list:
    # Parse XML
    tree = parseString(xml_string)
    items = tree.getElementsByTagName('filters')[0].getElementsByTagName('item')
    rules_str = []
    for item in items:
        if item.childNodes[0].data.startswith('r='):
            rules_str.append(item.childNodes[0].data[2:])

    # Generate Rule objects
    rules = []
    for rule_str in rules_str:
        rules.append(Rule.parse(rule_str))
    return rules


def parse_rule_xml(path: str, encoding='utf-8') -> list:
    with open(path, encoding=encoding) as f:
        s = f.read()
    return parse_rule_xml_str(s)


if __name__ == '__main__':
    import requests

    # parse_rule_xml_str(requests.get('https://raw.githubusercontent.com/jnxyp/Bilibili-Block-List/master/API/test.xml').content)
    # parse_rule_xml('D:\My File\Projects\Bilibili-Block-List\API\\test.xml')

    for i in range(101):
        print_progress_bar(100, i)
        sleep(0.1)
