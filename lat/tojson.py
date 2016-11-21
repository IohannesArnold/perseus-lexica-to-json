#!/usr/bin/env python
import xmltodict
import sys
import json

for i in sys.argv[1:]:
    with open(i, 'rb') as f:
        data = xmltodict.parse(f)
    with open(i + '.json', 'w') as fp:
        json.dump(data, fp, indent=4)