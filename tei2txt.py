#!/usr/bin/env python3

"""
Transform simple TEI to plain text. 
"""

import re
import os
import glob
from lxml import etree
from os.path import join


datadir = join("/", "home", "christof", "Dropbox", "6-Library", "0-Collections", "converse-data", "")
xmlfolder = join(datadir, "master", "*")
txtfolder = join(datadir, "txt", "")


def read_xml(file):
    xml = etree.parse(file)
    return xml


def transform(xml):
    namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}
    # Remove tags but not contained text
    etree.strip_tags(xml, "{http://www.tei-c.org/ns/1.0}seg")
    etree.strip_tags(xml, "{http://www.tei-c.org/ns/1.0}sup")
    etree.strip_tags(xml, "{http://www.tei-c.org/ns/1.0}said") # deactivate if you want to remove all dialog
    etree.strip_tags(xml, "{http://www.tei-c.org/ns/1.0}hi")
    # Remove elements with contained text
    etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}note", with_tail=False)
    etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}quote", with_tail=False)
    etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}head", with_tail=False)
    #etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}said", with_tail=False) # removes all dialog
    # Select the text
    txt = xml.xpath("//tei:body//text()", namespaces=namespaces) # all text
    #txt = xml.xpath("//tei:body//said()", namespaces=namespaces) # only the dialog
    txt = " ".join(txt)
    txt = str(txt)
    #print(txt)
    return txt


def clean_txt(txt): 
    txt = re.sub("-- *\n? *", "-- ", txt)
    #txt = re.sub("-- *\n? *\n", "", txt) # use if removing all dialog
    txt = re.sub("[ ]{1,20}", " ", txt)
    txt = re.sub("\n{1,20}", "\n", txt)
    txt = re.sub("[ \n]{2,20}", " \n", txt)
    txt = re.sub("\t{1,20}", "\t", txt)
    #print(txt)
    return txt


def save_txt(txt, txtfolder, basename): 
    filename = txtfolder + basename + ".txt"
    with open(filename, "w", encoding="utf8") as outfile: 
        outfile.write(txt)


def main(teifolder, txtfolder):
    if not os.path.exists(txtfolder):
        os.makedirs(txtfolder)
    for file in glob.glob(xmlfolder): 
        basename, ext = os.path.basename(file).split(".")
        try: 
            xml = read_xml(file)
            txt = transform(xml)
            txt = clean_txt(txt)
            save_txt(txt, txtfolder, basename)
            print(basename)
        except: 
            print("Error", basename)
    
main(xmlfolder, txtfolder)
