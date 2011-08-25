# -*- coding: iso-8859-1 *-*
"""
SenteceSplitter.py for splitting chunks of text into ortographic sentences.

Contains a class SentenceSplitter which is used to split paragraphs into
sentences using a simple punctuation mark detecting regular expression and
a list of abbreviations that should not trigger a split.

Copyright (C) 2004  Mickel Grönroos

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

Contact information:
  mickel dot gronroos at gmail dot com
  www.pojkfilmsklubben.org/mickel/
  www.linkedin.com/in/mickel/

Version: $Id: SentenceSplitter.py,v 1.5 2004/03/19 10:31:17 mickel Exp $

Known limitations:

- Cannot handle correctly citations (in citation marks) that contains
  multiple sentences, e.g. "This is a citation. It has two sentences."
"""

import re
import locale
import string
import os

## Default module variables
if os.name == "posix":
    LOCALE = "fi_FI"
else:
    LOCALE = "fi"
ESCAPE = [(".", "_PERIOD_"), (":", "_COLON_")]

class SentenceSplitter(object):
    """The SentenceSplitter class."""

    def __init__(self,
                 loc=LOCALE,
                 abbreviations=[],
                 escape=ESCAPE):
        """Construct a SentenceSplitter object.

        Parameters:
        1. loc (a string or tuple to feed locale.setlocale()
           (Default: """+str(LOCALE)+""")
        2. abbreviations (a "stop list" of abbreviations that should not be
           split)
           (Default: [])
        3. escape (a sequence of tuples to escape punctuation in the stop list)
           (Default: """+str(ESCAPE)+""")
        """

        ## Set prerequisites
        self.setLocale(loc)
        self.setAbbreviations(abbreviations)
        self.setEscape(escape)

        ## The regular expression matching sentence boundaries
        self._regexpstring   = ("""([\!\"#\'\(\)\.\?]+) ([\"\'\(\-]*\s?["""+
                                string.uppercase+string.digits+"""])""")
        ## A pattern to go with the regular expression for splitting
        ## a chunk of text into sentences
        self._replacepattern = r"\1\n\2"

        ## Compile the regular expression object
        self._regexpobject   = re.compile(self._regexpstring)

    def setLocale(self, loc):
        """Sets the locale. Parameter must be in the format accepted
        by locale.setlocale()."""
        locale.setlocale(locale.LC_ALL, loc)

    def getLocale(self):
        """Returns the current locale."""
        return locale.getlocale()
    
    def setAbbreviations(self, abbreviations):
        """Sets the abbreviation "stop list", i.e. a list of abbreviations
        that should not trigger a split."""
        self._abbreviations = abbreviations

    def getAbbreviations(self):
        """Returns the "stop list" of abbreviations."""
        try:
            return self._abbreviations
        except:
            return []

    def setEscape(self, escape):
        """Sets the the escape handling, i.e. how the punctuation characters
        in the abbreviation stop list should be escaped before splitting
        and turned back to after splitting. The parameter should be a sequence
        of tuples.
        (Example: escape=[(".", "_PERIOD_"), (":", "_COLON_")]
        """
        self._escape = escape

    def getEscape(self):
        """Returns the current sequence of tuples used for escaping
        punctuation in the abbreviations in the stop list."""
        try:
            return self._escape
        except:
            return []

    def split(self, text):
        """Splits a chunk of text into a list of sentences."""

        ## First "escape" all abbreviations in a rather ugly manner
        for abbrev in self.getAbbreviations():
            if text.count(abbrev):
                for t_escapemapping in self.getEscape():
                    escabbrev = abbrev.replace(t_escapemapping[0],
                                               t_escapemapping[1])
                    text = text.replace(abbrev, escabbrev)
                
        ## Then try doing the replace given the regular expression
        ## and the replace pattern
        sentencestring = self._regexpobject.sub(self._replacepattern, text)

        ## Now "unescape" the abbreviations
        for t_escapemapping in self.getEscape():
            if sentencestring.count(t_escapemapping[1]):
                sentencestring = sentencestring.replace(t_escapemapping[1],
                                                         t_escapemapping[0])

        ## Split sentencestring on newlines and return the list
        return sentencestring.split("\n")

## Self-test code
if __name__ == '__main__':
    ## Use the codecs module to enable easy encoding/decoding
    import codecs 

    ## A way too small list of Finnish abbreviations containing punctuation
    abbreviations = ("esim.", "Esim.", "tms.", "Tms.", "prof.", "Prof.")

    ## Create the SentenceSplitter object
    ss = SentenceSplitter(abbreviations=abbreviations)

    ## Ask the user for a file containing test text and for the encoding
    ## of the file
    filename = raw_input("File: ")
    encoding = raw_input("File encoding: ")

    ## Open the file for reading
    fh = codecs.open(filename, encoding=encoding)

    ## Read all lines in the file, strip whitespace and newlines at the end
    ## and join it all into a large textchunk string with all stuff on one line
    lines =  map((lambda x: x.rstrip()), fh.readlines())
    textchunk = string.join(lines, " ")

    ## Split the textchunk into sentences
    l_sentences = ss.split(textchunk)

    ## Print out the textchunk
    print "INPUT:"
    if os.name == "posix":
        print textchunk.encode(ss.getLocale()[1])
    else:
        print textchunk

    ## Print out the sentences
    print "OUTPUT:"
    for sentence in l_sentences:
        if os.name == "posix":
            print sentence.encode(ss.getLocale()[1])
        else:
            print sentence
