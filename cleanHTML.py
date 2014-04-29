#! /usr/bin/env python

# Entity refs: &nbsp; &lsquo; &rsquo;

import sys
import os
import imp
import xml.etree.ElementTree as ET
import re

parser = ET.XMLParser()
parser.entity["nbsp"] = unichr(160)

def printNodeInfo(dataAsElement): 
    for node in dataAsElement.iter():
        sys.stderr.write(node.tag)
        sys.stderr.write(node.text)

def processBody(node):
    for child in node:
        if child.tag == "table":
            processTable(child)
            
def processTable(node):

    # Insert thead and tbody elements

    node.insert(0,ET.Element("thead"))
    node.insert(1,ET.Element("tbody"))
    
    thead = node.find("./thead")
    tbody = node.find("./tbody")
                 
    rowCount = 0
    for child in node:
        if child.tag == "tr":
            if rowCount == 0:
                # Fix row contents
                processFirstRow(child)
                # Add row to thead element
                thead.append(child)
                              
            elif rowCount != 0:
                # Fix row contents
                processRow(child)
                # Add row to tbody element
                tbody.append(child)               
            rowCount += 1
    
    # Remove all tr elements that are direct child of table element 
    for tr in node.findall('tr'):
        node.remove(tr)
   
                   
def processFirstRow(node):
    for child in node.findall("td"):
        child.tag = "th"
        child.text = child[0][0].text
        
        for p in child.findall("p"):
            child.remove(p)
               
def processRow(node):
    for child in node.findall("td"):
        child.text = child[0][0].text
        
        for p in child.findall("p"):
            child.remove(p)
    
def main():
    fileIn = "tableIn.html"
    #fileIn = "table2.html"
    f = open(fileIn,"r")
    textData = f.read()
    f.close()
    
    # Remove namespace declaration so we don't have to specify it each time
    # while parsing the tree structure
    xmlstring = re.sub(' xmlns="[^"]+"', '', textData, count=1)
      
    root = ET.fromstring(xmlstring)    
    
    for child in root:
        if child.tag == "body":
            processBody(child)
   
    tree = ET.tostring(root, encoding="UTF-8") 
    print(tree)

if __name__ == "__main__":
    main()


"""
# build a tree structure
root = ET.Element("html")
#root = Element("html")

head = ET.SubElement(root, "head")

title = ET.SubElement(head, "title")
title.text = "Page Title"

body = ET.SubElement(root, "body")
body.set("bgcolor", "#ffffff")

body.text = "Hello, World!"

# wrap it in an xml.etree.ElementTree instance, and save as XML
#tree = root
tree = ET.ElementTree(root)

tree.write("page.xhtml")
"""

