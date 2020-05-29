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

class ResPartner(models.Model):
    _inherit = "res.partner"

    states = {}
    xmlid_module="__ais_import__"

    @api.model
    def create_employers(self):     
        headers_header = ['arbetsgivare.csv', 'Notering',  'Trans', 'Odoo', 'Odoo2']
        #path = os.path.join(config.options.get('data_dir'), 'mydir')
        header_path = "usr/share/odoo-af/af_data_ais-f_loader/data/arbetsgivare_mapping.csv"
        path = "usr/share/odoo-af/af_data_ais-f_loader/data/arbetsgivare_test.csv" #testing purposes only
        self.create_partners(headers_header, path, header_path)

    @api.model
    def create_organisations(self):     
        headers_header = ['organisationer.csv', 'Notering', 'Trans', 'Odoo', 'Odoo2']
        #path = os.path.join(config.options.get('data_dir'), 'mydir')
        header_path = "usr/share/odoo-af/af_data_ais-f_loader/data/organisationer_mapping.csv"
        path = "usr/share/odoo-af/af_data_ais-f_loader/data/organisationer_test.csv" #testing purposes only 
        self.create_partners(headers_header, path, header_path)

    @api.model
    def create_partners(self, headers_header, path, header_path):

        header_reader = ReadCSV(header_path, headers_header)
        header_rows = header_reader.parse_header()
        old_header = []
        field_map = {}
        transformations = {}
        for row in header_rows:
            #_logger.info("header_rows row processing: %s" % row)
            if row['Odoo'] != '' and "!" not in row['Odoo']:
                field_map.update({row['Odoo']: row[headers_header[0]]})
            if row['Odoo2'] != '' and "!" not in row['Odoo2']:
                field_map.update({row['Odoo2']: row[headers_header[0]]}) 
            if row['Trans'] != '':
                key = row['Trans'].split(",")[0]
                value = row['Trans'].split(",")[1]
                transformations.update({key: value})
            old_header.append(row[headers_header[0]]) #AIS-F fields
        _logger.info("header: %s" % field_map.keys())
        _logger.info("old_header: %s" % old_header)
        reader = ReadCSV(path, old_header) 
        self.create_partner_from_row(reader.parse(field_map), transformations)
    
    @api.model
    def create_partner_from_row(self, rows, transformations):
       
        for row in rows:
            create = True
            external_xmlid = ""
            keys_to_delete = []

            for key in row.keys():
                if row[key] == '(null)' or row[key] == '':
                    keys_to_delete.append(key)
            for i in range(len(keys_to_delete)):
                row.pop(keys_to_delete[i], None)
            
            keys_to_delete = [] 
            if 'name' not in row:
                row.update({'name' : row['customer_id']})

            if 'country_id' not in row or row['country_id'] == 'SE' or row['country_id'].lower() == 'sverige':
                country_id = self.env['ir.model.data'].xmlid_to_res_id('base.se')
                row.update({'country_id' : country_id})
            else: 
                _logger.info("Skipping partner, wrong country %s" % row['country_id'])
                create = False

            if 'state_id' in row:
                if row['state_id'] != '0':
                    state_xmlid = "base.state_se_%s" % row['state_id']
                    state_id = self.env['ir.model.data'].xmlid_to_res_id(state_xmlid)
                    row.update({'state_id' : state_id})
                else:
                    row.pop('state_id', None)

            for key in row.keys():
                if key in transformations:
                    transform = transformations[key]
                    if transform == 'skip':
                        create = False
                        _logger.info("Skipping partner, contains skipping flag %s" % row[transformations[key]])
                        break
                    elif transform == 'skip_if_u':
                        if row[key].lower() == 'u':
                            create = False
                            _logger.info("Skipping partner, contains U in ORGTYP %s" % row[transformations[key]])
                            break
                    elif transform == 'skip_if_j':
                        if row[key].lower() == 'j':
                            create = False
                            _logger.info("Skipping partner, contains J in RADERAD %s" % row[transformations[key]])
                            break
                    if key == 'parent_id': 
                        parent_xmlid_name = "%s%s" % (transform, row[key])
                        parent_xmlid = "%s.%s" % (self.xmlid_module, parent_xmlid_name)
                        _logger.info("parent xmlid: %s" % parent_xmlid)
                        parent_id = self.env['ir.model.data'].xmlid_to_res_id(parent_xmlid)
                        _logger.info("parent res_id: %s" % parent_id)
                        row.update({key: parent_id})   
                    # elif key == 'postal_address_id':
                    #     xmlid_name = "%s%s" % (transform, row['external_id'])
                    #     postal_address_xmlid = "%s.%s" % (self.xmlid_module,xmlid_name)
                    #     xmlid_name = "%s%s" % (transform, row['postal_address_state_id'])
                    #     postal_address_state_id_xmlid = "%s.%s" % (self.xmlid_module, xmlid_name)
                    #     row.update({'postal_address_state_id': postal_address_state_id_xmlid})
                    #     postal_address = {
                    #         'street': row.pop('postal_address_street', None),
                    #         'zip': row.pop('postal_address_zip', None),
                    #         'city': row.pop('postal_address_city', None),
                    #         'state_id' : row.pop('postal_address_state_id', None)
                    #     }
                    #     postal_address_partner = self.env['res.partner'].create(postal_address)
                    #     self.env['ir.model.data'].create({
                    #         'name': postal_address_xmlid.split('.')[1],
                    #         'module': postal_address_xmlid.split('.')[0],
                    #         'model': postal_address_partner._name,
                    #         'res_id': postal_address_partner.id
                    #         }) #creates an external id in the system for the partner.
                    elif key == 'external_id':
                        xmlid_name = "%s%s" % (transform, row[key])
                        external_xmlid = "%s.%s" % (self.xmlid_module, xmlid_name)
                        keys_to_delete.append(key)
            
            keys_to_delete = keys_to_delete + ['skip', 'skip2']
            if create:
                for i in range(len(keys_to_delete)):
                    row.pop(keys_to_delete[i], None)
                _logger.info("creating row %s" % row)

                partner = self.env['res.partner'].create(row)
                self.env['ir.model.data'].create({
                                'name': external_xmlid.split('.')[1],
                                'module': external_xmlid.split('.')[0],
                                'model': partner._name,
                                'res_id': partner.id
                                }) #creates an external id in the system for the partner.


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
        field_map = {}
        for i in range(len(self.header)):
            field_map.update({self.header[i] : self.header[i]})

        csvIter = CSVIterator(self.data,len(self.data), self.header, field_map)
        pairs = []
        while csvIter.hasNext():
            #_logger.info("appending header row %s" % csvIter.getRow())
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
                #_logger.info("Updating row %s : %s" % (self.header[i], self.data[self.row][self.field_map[self.header[i]]]))
                r.update({self.header[i] : self.data[self.row][self.field_map[self.header[i]]]})

        return r

     
