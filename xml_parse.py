import xml.etree.ElementTree as et

p = print

tree = et.ElementTree(file = 'danmaku/10086.xml')

root = tree.getroot()

for node in root.iter():
    p(node.tag, node.attrib.get('p'), node.text)

