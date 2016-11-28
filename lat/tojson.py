#!/usr/bin/env python
from lxml import etree
import sys
import json

for arg in sys.argv[1:]:
    xml_data = etree.parse(arg)
    json_out = []
    for entry in xml_data.xpath('/div0/entryFree'):

        # 'key' and 'type' are easy metadata to grab
        key = entry.get("key")
        entry_type = entry.get("type")
        
        # Get the <sense> elements for the main part of the dictionary entry
        senses = []
        for sense in entry.xpath('sense'):
            #etree.strip_attributes(sense, 'n', 'id')
            senses.append(etree.tostring(sense, method="text", encoding="unicode", with_tail=False))
        
        # Strip out the <sense> elements and get the remainder for the front part of entry
        etree.strip_elements(entry, "sense")
        front_matter = etree.tostring(entry, method="text", encoding="unicode", with_tail=False)
        
        # Find part of speech
        if len(entry.xpath("pos")) == 1:
            if entry.xpath("pos")[0].text == "adj." or entry.xpath("pos")[0].text == "adj":
                part_of_speech = "adjective"
            elif entry.xpath("pos")[0].text =="adv." or entry.xpath("pos")[0].text =="adv":
                part_of_speech = "adverb"
            elif entry.xpath("pos")[0].text =="prep." or entry.xpath("pos")[0].text =="prep":
                part_of_speech = "preposition"
            elif entry.xpath("pos")[0].text =="interj." or entry.xpath("pos")[0].text =="interj":
                part_of_speech = "interjection"
            elif entry.xpath("pos")[0].text[0] =="v":
                part_of_speech = "verb"
            elif entry.xpath("pos")[0].text[0] =="P":
                part_of_speech = "participle"
            else:
                part_of_speech = entry.xpath("pos")[0].text
        elif len(entry.xpath("pos")) == 0:
            if len(key) == 1:
                part_of_speech = 'letter'
            elif entry.xpath("gen"):
                part_of_speech = 'noun'
            else:
                part_of_speech = None
        
        # Put it all into a Python dict to convert to JSON
        json_out.append({
           'key':key,
           'type':entry_type,
           'senses': senses,
           'front_matter': front_matter,
           'part_of_speech': part_of_speech,
        })
        
        #'gender':"".join([x.text for x in entry.xpath("gen")]),
    #print(json.dumps(json_out, indent=4, ensure_ascii=False, sort_keys=True))
    with open(arg + '.json', 'w') as fp:
        print(json.dump(json_out, fp, indent=4, ensure_ascii=False, sort_keys=True))