# converse

Simple scripts for converting between text formats using Python. 

## Features of HTML to XML-TEI conversion (html2tei.py)

* Minimal `teiHeader` with minimal metadata (author, title, identifier)
* Paragraphs marked as `p`
* Chapter headings `head` and chapter boundaries `div`
* Italics `seg rend="italic"`
* Direct speech `said` (based on formal features alone)
* Subsection markers `milestone`
* Removing all unnecessary HTML markup
* Sorting out front and back matter from the main body text
* Pretty printing
* Checking well-formedness with feedback


 
