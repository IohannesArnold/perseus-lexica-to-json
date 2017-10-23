#!/usr/bin/env python
from lxml import etree
import string
import sys
import os

parser = etree.XMLParser(remove_blank_text=True, no_network=False)
doc = etree.parse(sys.argv[1], parser)

etree.strip_tags(doc, "hi")
for letter in string.ascii_uppercase:
    path = "//div0[@n='%s']" % letter
    printDoc = open('ls_'+letter+'.xml', 'w')
    for i in doc.xpath(path):
        printDoc.write(etree.tounicode(i, pretty_print=True))
    printDoc.close()

# remove any empty files; e.g. W doesn't exist in a Latin dictionary
for root, dirs, files in os.walk("."):
    for filename in files:
        if os.stat(filename).st_size == 0:
            print("removing empty file: ", filename)
            os.unlink(filename)
