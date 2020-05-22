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
    def create_partners(self):
        reader = ReadCSV("usr/share/odoo-af/af_data_ais-f_loader/data/arbetsgivare_test.csv")
        self.create_partner_from_row(reader.parse())
    
    @api.model
    def create_partner_from_row(self, rows):
        for row in rows:
            #partner_id = self.env['res.partner'].search([('id', '=', "af_data_ais-f_loader.%s" % row['id'])])
            #partner_id = self.env.ref(row['external_id'])
            #row.update({'parent_id' :  parent_id}) 
            #_logger.info("%s" % row['partner_id'])
            _logger.info("creating row %s" % row)
            #if not partner_id:
            #    self.env['res.partner'].create(row)
            #else:
            #    self.env['res.partner'].update(row)
            partner = self.env['res.partner'].create(row)
            
            xmlid = "foo.bar"
            self.env['ir.model.data'].create({
                'name': xmlid.split('.')[1],
                'module': xmlid.split('.')[0],
                'model': partner._name,
                'res_id': partner.id
            })


    #create a record using data from csv

class ReadCSV(object):
    def __init__(self, path):     
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
        
        header = ['KUNDNR', 'AG_NAMN']
        for i in range(len(header)):
            if not header[i] in self.data[0].keys(): 
                _logger.error(u'Row 0 could not find "%s"' % header[i])
                raise ValueError("Missing column '%s', columns found: %s" % (header[i], list(self.data[0].keys())))

    def parse(self):
        header = ['external_id', 'name']
        old_header = ['KUNDNR', 'AG_NAMN']
        csvIter = CSVIterator(self.data,len(self.data), header, old_header)
        pairs = []
        while csvIter.hasNext():
            _logger.info("appending row %s" % csvIter.getRow())
            pairs.append(csvIter.getRow())
            csvIter.next()
        return pairs


class CSVIterator(object):
    def __init__(self, data, nrows, header, old_header):
        self.nrows = nrows
        self.row = 0
        self.data = data
        self.rows = nrows - 2
        self.header = header
        self.old_header = old_header

    def next(self):
        if self.hasNext():
            self.row += 1

    def hasNext(self):
        return self.row <= self.nrows -1

    def getRow(self):
        field_map = {
            self.header[0]: self.old_header[0],
            self.header[1]: self.old_header[1],
        } #not a for loop because fields don't map 1:1
        r = {}
        for i in range(len(self.header)):
            if self.header[i] in field_map:
                if i == 0: #this should be the index of 'external_id'
                    r.update({self.header[i] : 'part_org_%s' % self.data[self.row][field_map[self.header[i]]]})
                else:
                    r.update({self.header[i] : self.data[self.row][field_map[self.header[i]]]})
                #TODO: explain this mess
                #
            else:
                r.update({self.header[i]: 'something'})
        
        return r

     
