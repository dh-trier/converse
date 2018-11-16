# converse

Simple scripts for converting between text formats using Python. 

## Features of HTML to XML-TEI conversion (html2tei.py)

* Minimal `teiHeader` with minimal metadata (author, title, identifier)
* Paragraphs marked as `p`
* Chapter headings `head` and chapter boundaries `div`
* Highlighting using `hi`
* Removing all unnecessary HTML markup

## Manual checks

* Pretty printing
* Sorting out front and back matter from the main body text
* Checking well-formedness and validity against schema: `ropo.rnc`


 
