#!/usr/bin/env python
from lxml import etree
import sys
import json
from beta2uni import beta_to_uni

for arg in sys.argv[1:]:
    xml_data = etree.parse(arg)
    json_out = []
    
    # Convert Betacode to Greek Unicode
    for greek in xml_data.xpath('//foreign[@lang="greek"]'):
        greek.text= beta_to_uni(greek.text)
    
    for entry_subelement in xml_data.xpath('/div0/entryFree'):
        entry = etree.ElementTree(entry_subelement)
        entry_dict = {}

        # 'key' and 'type' are easy metadata to grab
        entry_dict['key'] = entry.getroot().get("key")
        entry_dict['entry_type'] = entry.getroot().get("type")
        
        # Find part of speech
        if len(entry.xpath("//pos")) == 1:
            if "adj" in entry.xpath("//pos")[0].text:
                entry_dict['part_of_speech'] = "adjective"
            elif "adv" in entry.xpath("//pos")[0].text:
                entry_dict['part_of_speech'] = "adverb"
            elif "prep" in entry.xpath("//pos")[0].text:
                entry_dict['part_of_speech'] = "preposition"
            elif "interj" in entry.xpath("//pos")[0].text:
                entry_dict['part_of_speech'] = "interjection"
            elif "v" in entry.xpath("//pos")[0].text[0]:
                entry_dict['part_of_speech'] = "verb"
            elif "p" in entry.xpath("//pos")[0].text[0]:
                entry_dict['part_of_speech'] = "participle"
            else:
                entry_dict['part_of_speech'] = entry.xpath("//pos")[0].text
            etree.strip_elements(entry, "pos", with_tail=False)
        elif len(entry.xpath("//pos")) == 0:
            if len(entry_dict['key']) < 3 and len(entry.xpath("orth")[0].text)==1:
                entry_dict['part_of_speech'] = 'letter'
            elif entry.xpath("//gen"):
                entry_dict['part_of_speech'] = 'noun'
            else:
                entry_dict['part_of_speech'] = None
        else:
            if len(entry_dict['key']) < 3 and len(entry.xpath("orth")[0].text)==1:
                entry_dict['part_of_speech'] = 'letter'
            else:
                entry_dict['part_of_speech'] = ''.join([x.text for x in entry.xpath("//pos")])
        
        # If the entry is a letter of the alphabet, throw the whole thing in a single definition and move on.
        if entry_dict['part_of_speech'] == 'letter':
            entry_dict['title_orthography'] = entry.xpath("orth")[0].text + ', ' + entry.xpath("orth")[1].text
            etree.strip_elements(entry, "orth", with_tail=False)
            entry_dict['main_notes'] = etree.tostring(entry, method="text", encoding="unicode", with_tail=False)
            entry_dict['main_notes'] = entry_dict['main_notes'].strip(' ,')
            entry_dict['main_notes'] = entry_dict['main_notes'][0].capitalize() + entry_dict['main_notes'][1:]
            json_out.append(entry_dict)
            continue
        
        # For nouns
        if entry_dict['part_of_speech'] == "noun":
            
            # Set orthography
            if len(entry.xpath("//orth")) == 0:
                entry_dict['title_orthography'] = None
            elif len(entry.xpath("//orth")) == 1:
                entry_dict['title_orthography'] = entry.xpath("//orth")[0].text
            else:
                entry_dict['title_orthography'] = entry.xpath("//orth")[0].text
                entry_dict['alternative_orthography'] = [x.text for x in entry.xpath("//orth")[1:]]
            etree.strip_elements(entry, "orth", with_tail=False)
            
            # Set genitive
            if len(entry.xpath("//itype")) == 0:
                entry_dict['title_genitive'] = None
            elif len(entry.xpath("//itype")) == 1:
                entry_dict['title_genitive'] = entry.xpath("//itype")[0].text
            else:
                entry_dict['title_genitive'] = entry.xpath("//itype")[0].text
                entry_dict['alternative_genative'] = [x.text for x in entry.xpath("//itype")[1:]]
            etree.strip_elements(entry, "itype", with_tail=False)
            
            # Set gender of word
            entry_dict['gender'] = ''.join([x.text for x in entry.xpath("//gen")]).strip(' .').capitalize()
            if len(entry.xpath("//gen")) == 0:
                entry_dict['gender'] = None
            
            if len(entry.xpath("gen")) == 1:
                etree.strip_elements(entry, "gen", with_tail=False)
            
            # Set declension
            if entry_dict['title_orthography'] == None or entry_dict['title_genitive'] == None:
                entry_dict['declension'] = None
            elif entry_dict['title_orthography'][-1] == "a" and entry_dict['title_genitive'][-2:] == "ae":
                entry_dict['declension'] = 1
            elif (entry_dict['title_orthography'][-2:] == "us" or entry_dict['title_orthography'][-2:] == "um") and entry_dict['title_genitive'][-1] == "i":
                entry_dict['declension'] = 2
            elif entry_dict['title_orthography'][-2:] == "us" and entry_dict['title_genitive'][-2:] == "us":
                entry_dict['declension'] = 4
            elif entry_dict['title_orthography'][-2] == "e" and entry_dict['title_genitive'][-2:] == "es":
                entry_dict['declension'] = 5
            elif entry_dict['title_genitive'][-2:] == "is":
                entry_dict['declension'] = 3
            else:
                entry_dict['declension'] = None
                
        # Get the <sense> elements for the main part of the dictionary entry
        entry_dict['senses'] = []
        for sense in entry.xpath('sense'):
            #etree.strip_attributes(sense, 'n', 'id')
            sense_level = int(sense.get("level"))
            if len(entry_dict['senses']) > 0 and sense_level - entry_dict['senses'][-1][0] > 1:
                sense_level = entry_dict['senses'][-1][0] + 1
            sense_text = etree.tostring(sense, method="text", encoding="unicode", with_tail=False)
            sense_text = sense_text.strip(' ,—')
            if len(sense_text) < 2:
                continue
            sense_text = sense_text[0].capitalize() + sense_text[1:]
            entry_dict['senses'].append((sense_level, sense_text))
        
        # Strip out the <sense> elements and get the remainder for the front part of entry
        etree.strip_elements(entry, "sense")
        
        # If a word is Greek, record the greek word
        if entry_dict['entry_type'] == 'greek' and len(entry.xpath('foreign[@lang="greek"]')) == 1:
            entry_dict['greek_word'] = entry.xpath('foreign[@lang="greek"]')[0].text
            entry.xpath('foreign[@lang="greek"]')[0].text = ""

        entry_dict['main_notes'] = etree.tostring(entry, method="text", encoding="unicode", with_tail=False).strip(r'= ,—')
        
        # Put it all into a Python dict to convert to JSON
        json_out.append(entry_dict)
    
    if arg[-4:] == '.xml':
        arg = arg[:-4]
    print(arg + '.json')
    with open(arg + '.json', 'w') as fp:
        json.dump(json_out, fp, indent=4, ensure_ascii=False, sort_keys=True)