#!/usr/bin/env python
import sys
import json

for arg in sys.argv[1:]:
    with open(arg, 'r') as fp:
        doc = json.load(fp)
    
    redirect_count = 0
    null_pos_count = 0
    irreg_pos_count = 0
    null_gender_count = 0
    multi_gender_count = 0
    letter_count = 0
    for entry in doc:
        if entry['entry_type'] in ["redirect", "gloss", "spur"]:
            redirect_count += 1
        elif entry['part_of_speech'] == None:
            null_pos_count += 1
        elif entry['part_of_speech'] not in ["adjective","adverb", "preposition", "interjection", "verb", "participle", "letter", "noun", "conjunction"]:
            irreg_pos_count += 1
        elif entry['part_of_speech'] == "letter":
            letter_count += 1
        elif entry['part_of_speech'] == "noun" and entry['gender'] == None:
            null_gender_count += 1
        elif entry['part_of_speech'] == "noun" and len(entry['gender']) > 1:
            multi_gender_count += 1
    
    print(arg,
        "\nNumber of entries:", len(doc),
        "\nEntries with an irregular part of speech:", irreg_pos_count,
        "\nEntries without a part of speech:", null_pos_count,
        "\nNumber of letter entries (should be 1):", letter_count,
        "\nNouns without a gender:", str(null_gender_count),
        "\nNouns with nonstandard gender:", str(multi_gender_count), "\n")