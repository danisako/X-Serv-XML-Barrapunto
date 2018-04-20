#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

import urllib.request
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys



class myContentHandler(ContentHandler):

    def __init__(self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement(self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement(self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.titulo = "Titulo: " + self.theContent + "."
                print(self.titulo)
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.link = " Link: " + self.theContent + "."+'\n'
                fichero.write("<a href=" + self.theContent + ">" +
                                  self.titulo + "</a><br>\n")
                print(self.link)
                self.inContent = False
                self.theContent = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


# --- Main prog

if len(sys.argv) < 2:
    print("Usage: python xml-parser-barrapunto.py <document>")
    print()
    print(" <document>: file name of the document to parse")
    sys.exit(1)


# Load parser and driver

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!

fichero = open("barrapunto.html", "w")
fichero.write("<html><head><meta http-equiv='Content-Type'" +
                  "content='text/html; charset=utf-8'/></head><body><br>\n")
fichero.write("<h2>NOTICIAS BARRAPUNTO</h2>")
arg = sys.argv[-1]
xml = open(arg, "r")
theParser.parse(xml)

fichero.write("<ul/>"+ '\n'+ "</body>"+ '\n'+ "</html>")
fichero.close()

print("Parse Complete")
