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

# Parameters

datadir = join("/", "home", "christof", "Dropbox", "6-Library", "0-Collections", "converse-data", "")
headerfile = join(os.path.curdir, "teiHeader-model.xml")
htmlfolder = join(datadir, "html", "*.htm")
xmlfolder = join(datadir, "tei", "")


# Functions

   
def read_html(file): 
    with open(file, "r", encoding="utf8") as infile: 
        html = infile.read()
        return html


def remove_htmlhead(text): 
    text = re.sub("<!DOCTYPE.*?</head>", "", text, flags=re.DOTALL)
    text = re.sub("</html>", "", text)
    text = re.sub("<body>", "<text>\n<body>\n<div>", text)
    text = re.sub("</body>", "</div>\n</body>\n</text>", text)
    return text


def replace_nbsp(text): 
    text = re.sub("&nbsp;", " ", text)
    return text


def remove_spans(text): 
    text = re.sub("<span class=\"font\d+\">(.*?)</span>", "\\1", text)
    return text


def mark_italics(text): 
    text = re.sub("<span class=\"font\d+\" style=\"font-style:italic;\">(.*?)</span>", "<hi rend=\"italic\">\\1</hi>", text, flags=re.DOTALL)
    return text


def mark_sup(text): 
    text = re.sub("<sup>(.*?)</sup>", "<hi rend=\"sup\">\\1</hi>", text, flags=re.DOTALL)
    return text


def mark_divs(text): 
    text = re.sub("<h1><a name=\"caption1\"></a><a name=\"bookmark\d+\"></a>(.*?)</h1>", "</div><div><head>\\1</head>", text, flags=re.DOTALL)  
    return text


def mark_directspeech(text): 
    text = re.sub("<p>-- {1,10}(.*?)</p>", "<p>-- <said>\\1</said></p>", text)
    text = re.sub("<p>— {1,10}(.*?)</p>", "<p>-- <said>\\1</said></p>", text)
    return text


def mark_chapters(text): 
    text = re.sub("<h2><a name=\"bookmark\d\"></a>(.*?)</h2>", "\n</div>\n<div type=\"h2\">\n<head>\\1</head>", text)
    text = re.sub("<h1><a name=\"bookmark\d\"></a>(.*?)</h1>", "\n</div>\n<div type=\"h1\">\n<head>\\1</head>", text)    
    return text
    

def get_text(html): 
    text = remove_htmlhead(html)
    text = replace_nbsp(text)
    text = remove_spans(text)
    text = mark_italics(text) 
    text = mark_sup(text)
    text = mark_divs(text) 
    text = mark_directspeech(text) 
    text = mark_chapters(text) 
    #print(text[1000:1500])
    return text


def get_header(headerfile): 
    with open(headerfile, "r", encoding="utf8") as infile: 
        header = infile.read()
        return header 


def merge(header, text): 
    xmltei = header + text + "\n</TEI>"
    return xmltei
    

def save_xmltei(text, xmlfolder, basename): 
    filename = join(xmlfolder, basename + "_generated.xml")
    print(filename)
    with open(filename, "w", encoding="utf8") as outfile: 
        outfile.write(text)
        

def main(headerfile, htmlfolder, xmlfolder): 
    for file in glob.glob(htmlfolder):
        basename,ext = os.path.basename(file).split(".")
        html = read_html(file)
        text = get_text(html)
        header = get_header(headerfile)
        xmltei = merge(header, text)
        save_xmltei(xmltei, xmlfolder, basename)
        

main(headerfile, htmlfolder, xmlfolder)

