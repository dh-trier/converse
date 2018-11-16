#!/usr/bin/env python3

"""
Script for turning FineReader HTML to simple XML-TEI.
See: https://lxml.de/

"""


# Imports

import os
import re
import glob
from os.path import join
from bs4 import BeautifulSoup as bs

# Parameters

datadir = join("/", "home", "christof", "Dropbox", "6-Library", "0-Collections", "converse-data", "")
#datadir = join("/", "home", "christof", "Dropbox", "6-Library", "1-Literature", "RO", "Hajduk", "")
#datadir = join("/", "home", "christof", "Dropbox", "6-Library", "0-Collections", "rompop", "")
headerfile = join("teiHeader-model.xml")
htmlfolder = join(datadir, "html", "Mortimer_Adorable.htm")
xmlfolder = join(datadir, "tei", "")


# Functions


def read_html(file): 
    with open(file, "r", encoding="utf8") as infile: 
        html = infile.read()
        html = bs(html, "html.parser")
        return html


def mark_html(html): 
    # chapter headings
    for item in html.find_all("h3"): 
        item.insert_before("\n{CH=}")
        item.insert_after("{=CH}")
    for item in html.find_all("h2"): 
        item.insert_before("\n{CH=}")
        item.insert_after("{=CH}")
    # italics
    for item in html.find_all("span", style="font-style:italic;"): 
        item.insert_before("\n{HI=}")
        item.insert_after("{=HI}")
    # paragraphs
    for item in html.find_all("p"): 
        item.insert_before("\n{P=}")
        item.insert_after("{=P}")
    return html
    

def get_text(html): 
    text = html.get_text()
    text = re.sub("&nbsp;", " ", text)
    return text


def add_tei(text): 
    # chapter headings
    text = re.sub("{CH=}", "</div>\n<div>\n<head>", text)
    text = re.sub("{=CH}", "</head>", text)
    # paragraphs
    text = re.sub("{P=}", "<p>", text)
    text = re.sub("{=P}", "</p>", text)
    # italics
    text = re.sub("{HI=}", "<hi>", text)
    text = re.sub("{=HI}", "</hi>", text)
    # start and end
    start = "<text>\n<front><div><p></p></div></front>\n<body xml:lang=\"fra\"><div>"
    end = "</div>\n</body>\n<back><div><p></p></div></back>\n</text>\n</TEI>"
    text = start + text + end
    return text


def add_said(text): 
    text = re.sub("<p>[“—-][ ]{0,5}(.*?)</p>", "<p><said>-- \\1</said></p>", text)
    return text


def get_header(headerfile): 
    with open(headerfile, "r", encoding="utf8") as infile: 
        header = infile.read()
        return header 

def merge(header, text): 
    xmltei = header + text
    return xmltei
    

def clean_xmltei(xmltei): 
    xmltei = re.sub(" {3,5}", " ", xmltei)
    xmltei = re.sub(" {2}", " ", xmltei)
    xmltei = re.sub("\n{2,5}", "\n", xmltei)
    xmltei = re.sub("<p>\n<seg", "<p><seg", xmltei)
    return xmltei


def save_xmltei(text, xmlfolder, basename): 
    filename = join(xmlfolder, basename + ".xml")
    #print(filename)
    with open(filename, "w", encoding="utf8") as outfile: 
        outfile.write(text)
        

def main(headerfile, htmlfolder, xmlfolder): 
    for file in glob.glob(htmlfolder):
        basename,ext = os.path.basename(file).split(".")
        print(basename)
        html = read_html(file)
        html = mark_html(html)
        text = html.get_text()
        text = get_text(html)
        text = add_tei(text)
        #text = add_said(text)
        header = get_header(headerfile)
        xmltei = merge(header, text)
        xmltei = clean_xmltei(xmltei)
        save_xmltei(xmltei, xmlfolder, basename)
        

main(headerfile, htmlfolder, xmlfolder)

