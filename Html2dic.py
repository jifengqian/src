#!/usr/bin/python
# Jifeng Qian created on 5/16/2013
from HTMLParser import HTMLParser
from string import lower
import numpy
class JFHTMLParser(HTMLParser): # this is to parse an html file to a dictionary, the key of that dictionary is the table name, the value is the content of the table
    def __init__(self):
        HTMLParser.__init__(self)
        self.dic_table={}  # The whole table
        self.buf=''  # The current content being constructed from HTML
        self.tablename = '' # Used to track if we are inside or outside a <table>...</table> tag.
        self.row =[] # one row of a table
        self.tablename='' # this is the name of the tables
        self.start=0
        self.i=0
    def handle_starttag(self, tag, attrs):
        if lower(tag) == 'head':
            self.tablename = ''
        elif lower(tag) == 'h1' and self.start==1:
            self.tablename = ''
            self.buf=''
        elif lower(tag) == 'h2' and self.start==1:
            self.tablename = ''
            self.buf=''
        elif lower(tag) == 'tr' and self.start==1:
            self.row= []
            self.buf= ''
        elif lower(tag) == 'td' and self.start==1:
            self.buf = ''
    def handle_endtag(self, tag):
        if lower(tag) == 'head' :
            self.tablename = ''
            self.buf =''
            self.start=1
        elif lower(tag) == 'h1'  and self.start==1:
            self.tablename=self.buf # save the table name
            self.buf=''
            #print self.tablename
        elif lower(tag) == 'h2'  and self.start==1:
            self.tablename=self.buf # save the table name
            self.buf=''
            #print self.tablename
        elif lower(tag) == 'tr' and self.start==1:    
            if self.dic_table.has_key(self.tablename):
                newtable=numpy.vstack((self.dic_table[self.tablename],numpy.array(self.row)))  # add the new row vertically to the previous table
                self.dic_table[self.tablename]=newtable # update the table 
                #print "self.tablename",self.tablename
            else:
                if len(self.row)>0:
                    self.dic_table[self.tablename]=numpy.array(self.row)
            self.buf = ''
        elif lower(tag) == 'td' and self.start==1:
            self.row.append(self.buf.strip()) # add the content to the row container
            self.buf = ''                   
    def handle_data(self, data):
        self.buf += data.strip()
        #print self.i,self.buf,'---'
        self.i=self.i+1
# instantiate the parser and fed it some HTML
if __name__ == "__main__":
    parser = JFHTMLParser()
    data = open('index.html').read()
    parser.feed(data)
    for i in parser.dic_table.keys():
        print i
        print parser.dic_table[i]
    #print parser.dic_table
    #print parser.dic_table