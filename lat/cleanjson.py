#!/usr/bin/env python
import sys
import json

for arg in sys.argv[1:]:
    with open(arg, 'r') as fp:
        doc = json.load(fp)
    for entry in doc:
        
        if entry['part_of_speech'] == 'letter' or len(entry['senses']) == 0:
            continue
        
        #Transform the Python dict of levels and senses into nested lists
        sense_dict = {1:[]}
        for sense in entry['senses']:
            max_depth = max(sense_dict.keys())
            if sense[0] == max_depth:
                sense_dict[sense[0]].append(sense[1])
            elif sense[0] - max_depth == 1:
                sense_dict[sense[0]] = []
                sense_dict[sense[0]].append(sense[1])
            elif sense[0] < max_depth:
                for i in range(max_depth, sense[0], -1):
                    sense_dict[i-1].append(sense_dict[i])
                    del sense_dict[i]
                sense_dict[sense[0]].append(sense[1])
            else:
                print(entry['key'])
        
        for i in range(max(sense_dict.keys()), 1, -1):
            sense_dict[i-1].append(sense_dict[i])
            del sense_dict[i]
        
        entry['senses'] = sense_dict[1]
        
        # Fix misaligned parentheticals
        if entry['main_notes'].rfind("(") > entry['main_notes'].rfind(")") and len(entry['senses']) > 0:
            entry['main_notes'] = entry['main_notes'] + entry['senses'][0][:entry['senses'][0].find(")")+1].strip(r'= ,—()')
            entry['senses'][0] = entry['senses'][0][entry['senses'][0].find(")")+1:].strip(r'= ,—()')
            if len(entry['senses'][0]) < 2:
                del entry['senses'][0]
            else:
                entry['senses'][0] = entry['senses'][0][0].capitalize() + entry['senses'][0][1:]
        
        # Clean up parts of speech
        if (entry['part_of_speech'] == None and len(entry['senses']) > 0 and entry['senses'][0][0]=="V") or (entry['part_of_speech'] == None and len(entry['senses']) > 1 and entry['senses'][1][0]=="V"):
            entry['part_of_speech'] = "verb"
        elif (entry['part_of_speech'] == None and len(entry['senses']) > 0 and entry['senses'][0][0:3]=="Adj") or (entry['part_of_speech'] == None and len(entry['senses']) > 1 and entry['senses'][1][0:3]=="Adj"):
            entry['part_of_speech'] = "adjective"
        elif (entry['part_of_speech'] == None and len(entry['senses']) > 0 and entry['senses'][0][0:3]=="Adv") or (entry['part_of_speech'] == None and len(entry['senses']) > 1 and entry['senses'][1][0:3]=="Adv"):
            entry['part_of_speech'] = "adverb"
        elif (entry['part_of_speech'] == None and len(entry['senses']) > 0 and entry['senses'][0][0:4]=="Conj") or (entry['part_of_speech'] == None and len(entry['senses']) > 1 and entry['senses'][1][0:4]=="Conj"):
            entry['part_of_speech'] = "conjunction"
        elif (entry['part_of_speech'] == None and len(entry['senses']) > 0 and entry['senses'][0][0:4]=="Prep") or (entry['part_of_speech'] == None and len(entry['senses']) > 1 and entry['senses'][1][0:4]=="Prep"):
            entry['part_of_speech'] = "preposition"
        elif entry['part_of_speech'] == None and len(entry['main_notes'].split(" ")) >= 2 and "v" in entry['main_notes'].lower().split(" ")[-2]:
            entry['entry_type'] = "redirect"
    
    with open(arg, 'w') as fp:
        json.dump(doc, fp, indent=4, ensure_ascii=False, sort_keys=True)