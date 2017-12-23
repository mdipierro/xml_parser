# Created by Massimo Di Pierro @ 2015
# https://github.com/mdipierro/xml_parser
# License: BSDv3

import xml.etree.ElementTree as ET
import collections
import json

example = """<?xml version="1.0"?>
<A>
  <B>
    <E>Hello</E>
  </B>
  <C> 
     <D>True</D>
     <D>2</D>
     <D>3.1</D>
  </C>
</A>
"""

example_json = '{"A": {"B": [{"E": ["Hello"]}], "C": [{"D": [true, 2, 3.1]}]}}'

class XMLParser(object):
    def __init__(self, xml):
        self.soup = ET.fromstring(xml)
    def parse_text(self, text):
        if not text: 
            return text
        d = {'true':True, 'false':False}
        text = text.strip()
        try:            
            return int(text)
        except:
            try:
                return float(text)
            except:
                return d.get(text.lower(), text)
    def parse_rec(self, items):
        node = collections.OrderedDict()
        children = items.getchildren()
        n = len(children)
        if n == 0:
            return self.parse_text(items.text)
        else:
            tags = [obj.tag for obj in children]
            for obj in children:
                tag = obj.tag
                parsed = self.parse_rec(obj)
                if tags.count(tag) == 0:
                    node[tag] = parsed
                else:
                    if not tag in node:
                        node[tag] = []
                    node[tag].append(parsed)
        return node
    def parse(self):
        obj = collections.OrderedDict()
        obj[self.soup.tag] = self.parse_rec(self.soup)
        return obj
    def to_json(self):
        return json.dumps(self.parse())

if __name__ == '__main__':
    assert XMLParser(example).to_json() == example_json
