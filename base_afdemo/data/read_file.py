#!/usr/bin/python
# -*- coding: utf-8 -*-

import unicodedata
from xlrd import open_workbook
from xlrd.book import Book
from xlrd.sheet import Sheet
import csv

import os
idelim = ';'
#wb = open_workbook(os.path.join(os.path.dirname(os.path.abspath(__file__)), u'Kontohändelser.xlsx'))
class Iterator(object):
    def __init__(self, data):
        self.row = 0
        self.data = data
        self.rows = data.nrows - 1
        self.header = [(u'%s'% c.value.lower()).encode('utf-8') for c in data.row(0)]
    
    def __iter__(self):
        return self

    def next(self):
        if self.row >= self.rows:
            raise StopIteration
        r = self.data.row(self.row + 1)
        self.row += 1
        return {self.header[n]: 
                 (u'%s' % r[n].value).encode('utf-8') for n in range(len(self.header))}

wb = open_workbook(os.path.join(os.path.dirname(os.path.abspath(__file__)), u'TestData_Config.xlsx'))

#import csv
#with open('eggs.csv', 'w', newline='') as csvfile:
#    spamwriter = csv.writer(csvfile, delimiter=' ',
#                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
#    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

#with open('names.csv', 'w', newline='') as csvfile:
#    fieldnames = ['first_name', 'last_name']
#    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#    writer.writeheader()
#    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
#    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
#    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

for sheet_name in wb.sheet_names():
    sheet = wb.sheet_by_name(sheet_name)
    names = sheet_name.split('.')
    if len(names)>1:
        print(sheet)
    names2 = sheet_name.split('_')
    if len(names2)>1:
        print(names2)
        print (Iterator(sheet).header)
        with open('%s.csv' % sheet_name, 'w' ) as csvfile:
#        csvfile = open('%s.csv' % sheet_name,'w',encoding='utf-8')
            writer = csv.DictWriter(csvfile, fieldnames=Iterator(sheet).header)

            writer.writeheader()
            for r in Iterator(sheet):
                writer.writerow(r)
                print(r)
#~ print ws.cell(0,0),ws.ncols,ws.nrows,ws.cell(3,10).value

#~ for r in range(ws.nrows):
    #~ if r > 3:
        #~ for c in ws.row(r):
            #~ print c.value




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
