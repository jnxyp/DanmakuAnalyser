
from xml.dom.minidom import parseString
from data.Rule import Rule

def timestamp_to_datetime(stamp: int):
    import datetime
    return datetime.datetime.fromtimestamp(stamp).strftime('%Y-%m-%d %H:%M:%S')


def parse_rule_xml_str(xml_string: str):
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


def parse_rule_xml(path: str, encoding='utf-8'):
    with open(path, encoding=encoding) as f:
        s = f.read()
    return parse_rule_xml_str(s)


if __name__ == '__main__':
    import requests

    # parse_rule_xml_str(requests.get('https://raw.githubusercontent.com/jnxyp/Bilibili-Block-List/master/API/test.xml').content)
    parse_rule_xml('D:\My File\Projects\Bilibili-Block-List\API\\test.xml')