#! /usr/bin/env python

import xml.etree.ElementTree as ET

xmlIn = "<fruit><apple/><apple/><apple/></fruit>"

# String to element object
root = ET.fromstring(xmlIn) 

# Iterate over child elements and remove them

for apple in root.findall('apple'):
    root.remove(apple)
    
"""
for child in root:
    print("Removing child element")
    root.remove(child)
"""

# Iterate over child elements again and print tags
for child in root:
    print(child.tag)
