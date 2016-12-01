#!/usr/bin/env python
import sys
import json

for arg in sys.argv[1:]:
    with open(arg, 'r') as fp:
        doc = json.load(fp)
    for entry in doc:
        if entry['part_of_speech'] == 'letter' or len(entry['senses']) == 0:
            continue
        
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
    with open(arg, 'w') as fp:
        json.dump(doc, fp, indent=4, ensure_ascii=False, sort_keys=True)