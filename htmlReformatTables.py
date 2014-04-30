#! /usr/bin/env python

"""
Reformat tables in HTML document so that Pandoc will be able to convert them to
(almost) proper Markdown Extra tables. Written specifically for HTML that was exported
by MS Word. For each table, this script does the following:

1. Wrap first row in thead element and change td elements there to th
2. Wrap remaining rows in tbody elements
3. Remove outer p element from all table cells

Resulting html can be converted to Markdown with Pandoc:
    http://johnmacfarlane.net/pandoc/ 

Use the following command:

    pandoc -f html -t markdown_phpextra file.html > file.md
    
Notes:

1. Before using this script, clean up MS Word-generated HTML with: 
    http://infohound.net/tidy/
2. Table conversion isn't 100% fool-proof. 
3. Even if subsequent Markdown conversion with Pandoc is successful, you
   will probably have to do a fair amount of manual editing afterwards.  

Use at your own risk!

Johan van der Knijff, 2014

"""

import sys
import os
import imp
import xml.etree.ElementTree as ET
import re
import argparse
from cStringIO  import StringIO

parser = ET.XMLParser()
parser.parser.UseForeignDTD(True)
parser.entity["nbsp"] = unichr(160)
parser.entity["lsquo"] = unichr(8216)
parser.entity["rsquo"] = unichr(8217)
parser.entity["ldquo"] = unichr(8220)
parser.entity["rdquo"] = unichr(8221)
parser.entity["middot"] = unichr(183)
parser.entity["hellip"] = unichr(8230)
parser.entity["ndash"] = unichr(8211)
parser.entity["le"] = unichr(8804)
parser.entity["ge"] = unichr(8805)
parser.entity["mdash"] = unichr(8212)

etree = ET.ElementTree()


def printNodeInfo(dataAsElement): 
    for node in dataAsElement.iter():
        sys.stderr.write(node.tag + "\n")
        if node.text != None: 
            sys.stderr.write(node.text + "\n")

def parseCommandLine():
    # Create parser
    parser = argparse.ArgumentParser(description="Reformat tables in HTML document")
 
    # Add arguments
    parser.add_argument('htmlIn', 
        action = "store", 
        help = "input HTML file")
    args=parser.parse_args()
    
    return(args)
            
def processTable(node):

    # Insert thead and tbody elements
    node.insert(0,ET.Element("thead"))
    node.insert(1,ET.Element("tbody"))
    
    thead = node.find("./thead")
    tbody = node.find("./tbody")
    
    # Iterate over table rows
    rowCount = 0
    for child in node:
        if child.tag == "tr":
            if rowCount == 0:
                # Fix row contents
                processHeaderRow(child)
                # Add row to thead element
                thead.append(child)
                              
            elif rowCount != 0:
                # Fix row contents
                processRow(child)
                # Add row to tbody element
                tbody.append(child)               
            rowCount += 1
    
    # Remove all tr elements that are direct a child of table element 
    for tr in node.findall('tr'):
        node.remove(tr)
                      
def processHeaderRow(node):

    for td in node.findall("td"):
        for p in td.findall("p"): 
            # Rename all p nodes to th and append them to parent element
            p.tag = "th"
            node.append(p)
               
    for td in node.findall("td"):
            node.remove(td)
               
def processRow(node):
    
    for td in node.findall("td"):
        # Rename all td nodes so we can easily remove them later
        td.tag = "td_old"
        for p in td.findall("p"):
            # Rename all p nodes to td and append them to parent element
            p.tag = "td"
            node.append(p)
               
    for td in node.findall("td_old"):
            node.remove(td)
    
def main():
    args = parseCommandLine()
    fileIn=args.htmlIn
    f = open(fileIn,"r")
    textData = f.read()
    f.close()
    
    # Remove namespace declaration so we don't have to specify it each time
    # while parsing the tree structure
    xmlstring = re.sub(' xmlns="[^"]+"', '', textData, count=1)
    
    root = etree.parse(StringIO(xmlstring), parser=parser)

    for element in root.iter('table'):
        processTable(element)   
    
    tree = ET.tostring(root, encoding="UTF-8") 
    print(tree)

if __name__ == "__main__":
    main()
