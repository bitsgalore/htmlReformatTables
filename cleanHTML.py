#! /usr/bin/env python

import sys
import os
import imp
import xml.etree.ElementTree as ET
import re

def printNodeInfo(dataAsElement): 
    for node in dataAsElement.iter():
        sys.stderr.write(node.tag)
        sys.stderr.write(node.text)

def processBody(node):
    for child in node:
        if child.tag == "table":
            processTableTest(child)
            
def processTable(node):

    # Insert thead and tbody elements

    node.insert(0,ET.Element("thead"))
    node.insert(1,ET.Element("tbody"))
    
    thead = node.find("./thead")
    tbody = node.find("./tbody")
    
    # What about this:
    # 1. Count number of child elements
    # 2. Explicitly address those by their index
    # 3. Do processing and apply remove to indexed child
    #
    # Current approach *might* mess up internal indexing
    
           
    rowCount = 0
    for child in node:
        if child.tag == "tr":
            if rowCount == 0:
                # Add row to thead element
                thead.append(child)
                
                # Remove row from parent node
                #node.remove(child)
                #processFirstRow(child)
                
                #sys.stderr.write("header row, row count =" + str(rowCount))
                
            elif rowCount != 0:
                # Add row to tbody element
                tbody.append(child)
                
                # Remove row from parent node
                #node.remove(child)
                #processRow(child)
                #node.insert(0, subnode)
                
                #sys.stderr.write("body row, row count =" + str(rowCount))
                
            rowCount += 1
    
    for child in node:
        sys.stderr.write(child.tag + "\n")
        
        if child.tag == "tr":
            node.remove(child)
            sys.stderr.write("removed child \n")

    for child in node:
        sys.stderr.write(child.tag + "\n")

def processTableTest(node):

    for child in node:
        sys.stderr.write(child.tag + "\n")
        
        if child.tag == "tr":
            sys.stderr.write("removing child \n")
            node.remove(child)
    
    sys.stderr.write("---------------------\n")

    for child in node:
        sys.stderr.write(child.tag + "\n")

                              
def processFirstRow(node):
    pass

def processRow(node):
    pass
    
def main():
    fileIn = "tableIn.html"
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

