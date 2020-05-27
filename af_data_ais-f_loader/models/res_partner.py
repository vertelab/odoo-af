# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2019 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

import csv
import os
import tempfile

# TODO:
# gör så att det går att läsa in fler filer
# ändra värdet på t.ex. externt_id på en plats där det kan göras beroende på vilken fil som läses in
# external_id = row['external_id]
# row.update('external_id' : 'part_org_%s' % external_id)
# 
#
#
#
#

class ResUsers(models.Model):
    _inherit = "res.partner"
    @api.model
    def create_employers(self):
        headers_header = ['arbetsgivare.csv', 'Notering', 'Odoo', 'Odoo2']
        header_reader = ReadCSV("usr/share/odoo-af/af_data_ais-f_loader/data/arbetsgivare_mapping.csv", headers_header)
        header_rows = header_reader.parse_header()
        old_header = []
        field_map = {}
        for row in header_rows:
            if row['Odoo'] != '' and "!" not in row['Odoo']:
                field_map.update({row['Odoo']: row['arbetsgivare.csv']})
            if row['Odoo2'] != '' and "!" not in row['Odoo2']:
                field_map.update({row['Odoo']: row['arbetsgivare.csv']})
            old_header.append(row['arbetsgivare.csv'])
        _logger.info("header: %s" % field_map.keys())
        _logger.info("old_header: %s" % old_header)
        reader = ReadCSV("usr/share/odoo-af/af_data_ais-f_loader/data/arbetsgivare_test.csv", old_header)
        self.create_partner_from_row(reader.parse(field_map))
    
    @api.model
    def create_partner_from_row(self, rows):
        for row in rows:
            _logger.info("creating row %s" % row)
            
            for key in row.keys:
                if row[key] == '(null)':
                    row.pop(key, None)

            if 'parent_id' in row:
                
                parent_id = row.pop('parent_id', None)
                parent_xmlid_name = "%s" % parent_id
                parent_xmlid = xmlid_module + "." + parent_xmlid_name
                parent_id = self.env['ir.model.data'].xmlid_to_res_id(parent_xmlid) #få ut id:t från en min partner för att sätta den som parent till en annan


            partner_id = row.pop('external_id', None)
            xmlid_module="__ais_import__"
            xmlid_name="part_cfar_%s" % partner_id

            partner = self.env['res.partner'].create(row)

            xmlid = xmlid_module + "." + xmlid_name
            self.env['ir.model.data'].create({
                'name': xmlid.split('.')[1],
                'module': xmlid.split('.')[0],
                'model': partner._name,
                'res_id': partner.id
            })


            
    #create a record using data from csv

class ReadCSV(object):
    def __init__(self, path, header): 
        self.header = header    
        try:
            rows = []
            f = open(path)
            f.seek(0)
            reader = csv.DictReader(f,delimiter=",")
            for row in reader:
                rows.append(row)
            f.close()
            self.data = rows
        except IOError as e:
            _logger.error(u'Could not read CSV file')
            raise ValueError(e)
        for i in range(len(self.header)):
            if not self.header[i] in self.data[0].keys(): 
                _logger.error(u'Row 0 could not find "%s"' % self.header[i])
                raise ValueError("Missing column '%s', columns found: %s" % (self.header[i], list(self.data[0].keys())))

    def parse(self, field_map):
        csvIter = CSVIterator(self.data,len(self.data), list(field_map.keys()), field_map)
        pairs = []
        while csvIter.hasNext():
            _logger.info("appending row %s" % csvIter.getRow())
            pairs.append(csvIter.getRow())
            csvIter.next()
        return pairs
    
    def parse_header(self):
        field_map = {
            self.header[0] : self.header[0],
            self.header[1] : self.header[1],
            self.header[2] : self.header[2],
            self.header[3] : self.header[3]
        }
        csvIter = CSVIterator(self.data,len(self.data), self.header, field_map)
        pairs = []
        while csvIter.hasNext():
            _logger.info("appending header row %s" % csvIter.getRow())
            pairs.append(csvIter.getRow())
            csvIter.next()
        return pairs



class CSVIterator(object):
    def __init__(self, data, nrows, header, field_map):
        self.nrows = nrows
        self.row = 0
        self.data = data
        self.rows = nrows - 2
        self.header = header
        self.field_map = field_map

    def next(self):
        if self.hasNext():
            self.row += 1

    def hasNext(self):
        return self.row <= self.nrows -1

    def getRow(self):
        r = {}
        for i in range(len(self.header)):
            if self.header[i] in self.field_map:
                _logger.info("Updating row %s : %s" % (self.header[i], self.data[self.row][self.field_map[self.header[i]]]))
                r.update({self.header[i] : self.data[self.row][self.field_map[self.header[i]]]})

        return r

     
