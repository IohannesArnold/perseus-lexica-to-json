#!/usr/bin/env python
from lxml import etree
import sys
import json

for arg in sys.argv[1:]:
    xml_data = etree.parse(arg)
    json_out = []
    for entry in xml_data.xpath('/div0/entryFree'):
        
        # Get the <sense> elements for the main part of the dictionary entry
        entries = []
        for sense in entry.xpath('sense'):
            #etree.strip_attributes(sense, 'n', 'id')
            entries.append(etree.tostring(sense, method="text", encoding="unicode", with_tail=False))
        
        # Strip out the <sense> elements and get the remainder for the front part of entry
        etree.strip_elements(entry, "sense")
        front_matter = etree.tostring(entry, method="text", encoding="unicode", with_tail=False)
        
        # Put it all into a Python dict to convert to JSON
        json_out.append({
           'key':entry.get("key"),
           'type':entry.get("type"),
           'entries': entries,
           'front_matter': front_matter,
        })
        
        #'gender':"".join([x.text for x in entry.xpath("gen")]),
        #'part_of_speech':"".join([x.text for x in entry.xpath("pos")]),
    with open(arg + '.json', 'w') as fp:
        print(json.dump(json_out, fp, indent=4, ensure_ascii=False, sort_keys=True))