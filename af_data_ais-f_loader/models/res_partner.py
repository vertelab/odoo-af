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

from odoo.tools import config

import csv
import os
import tempfile


# TODO:
# koppla samman visitation address med parent_id
# fixa expected singleton error

class ResPartner(models.Model):
    _inherit = "res.partner"

    xmlid_module="__ais_import__"

    @api.model
    def create_jobseekers(self):     
        headers_header = ['ARBETSSOKANDE.csv', 'Notering',  'Trans', 'Odoo']
        path = os.path.join(config.options.get('data_dir'), 'AIS-F/arbetssokande.csv')
        path = "usr/share/odoo-af/af_data_ais-f_loader/data/test_dumps/arbetssokande.csv" #testing purposes only
        header_path = "usr/share/odoo-af/af_data_ais-f_loader/data/arbetssokande_mapping.csv"
        self.create_partners(headers_header, path, header_path)    

    @api.model
    def create_contact_persons(self):     
        headers_header = ['kontaktperson.csv', 'Notering',  'Trans', 'Odoo']
        path = os.path.join(config.options.get('data_dir'), 'AIS-F/kontaktperson.csv')
        path = "usr/share/odoo-af/af_data_ais-f_loader/data/test_dumps/kontaktperson.csv" #testing purposes only
        header_path = "usr/share/odoo-af/af_data_ais-f_loader/data/kontaktperson_mapping.csv"
        self.create_partners(headers_header, path, header_path)

    @api.model
    def create_employers(self):     
        headers_header = ['arbetsgivare.csv', 'Notering',  'Trans', 'Odoo']
        path = os.path.join(config.options.get('data_dir'), 'AIS-F/arbetsgivare.csv')
        path = "usr/share/odoo-af/af_data_ais-f_loader/data/test_dumps/arbetsgivare.csv" #testing purposes only
        header_path = "usr/share/odoo-af/af_data_ais-f_loader/data/arbetsgivare_mapping.csv"
        self.create_partners(headers_header, path, header_path)

    @api.model
    def create_organisations(self):     
        headers_header = ['organisation.csv', 'Notering', 'Trans', 'Odoo']
        path = os.path.join(config.options.get('data_dir'), 'AIS-F/organisation.csv')
        path = "usr/share/odoo-af/af_data_ais-f_loader/data/test_dumps/organisation.csv" #testing purposes only
        header_path = "usr/share/odoo-af/af_data_ais-f_loader/data/organisation_mapping.csv"
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
            # if row['Odoo2'] != '' and "!" not in row['Odoo2']:
            #     field_map.update({row['Odoo2']: row[headers_header[0]]}) 
            if row['Trans'] != '':
                key = row['Trans'].split(",")[0]
                value = row['Trans'].split(",")[1]
                transformations.update({key: value})
            old_header.append(row[headers_header[0]]) #AIS-F fields
        #_logger.info("header: %s" % field_map.keys())
        #_logger.info("old_header: %s" % old_header)
        reader = ReadCSV(path, old_header) 
        self.create_partner_from_rows(reader.parse(field_map), transformations)
    
    @api.model
    def create_partner_from_rows(self, rows, transformations):
        ids = []
        for row in rows:
            create = True
            external_xmlid = ""
            keys_to_delete = []
            keys_to_update = []
            visitation_address = {}
            visitation_address_transformations = {}

            for key in row.keys():
                if row[key] == '(null)' or row[key] == '':
                    keys_to_delete.append(key)
            for i in range(len(keys_to_delete)):
                row.pop(keys_to_delete[i], None)
            
            keys_to_delete = [] 

            for key in row.keys():
                if key not in transformations and isinstance(row[key], str):
                    if row[key].lower() == "j":
                        keys_to_update.append({key: "True"})
                    elif row[key].lower() == "n":
                        keys_to_update.append({key: "False"})

            for key in row.keys():
                if key in transformations:
                    transform = transformations[key]
                    if transform == 'skip':
                        create = False
                        #_logger.info("Skipping partner, contains skipping flag %s" % row[transformations[key]])
                        break
                    elif transform == 'skip_if_u':
                        if row[key].lower() == 'u':
                            create = False
                            #_logger.info("Skipping partner, contains U in ORGTYP %s" % row[transformations[key]])
                            break
                    elif transform == 'skip_if_j':
                        if row[key].lower() == 'j':
                            create = False
                            #_logger.info("Skipping partner, contains J in RADERAD %s" % row[transformations[key]])
                            break
                    if key == 'parent_id': 
                        parent_xmlid_name = "%s%s" % (transform, row[key])
                        parent_xmlid = "%s.%s" % (self.xmlid_module, parent_xmlid_name)
                        #_logger.info("parent xmlid: %s" % parent_xmlid)
                        parent_id = self.env['ir.model.data'].xmlid_to_res_id(parent_xmlid)
                        #_logger.info("parent res_id: %s" % parent_id)
                        if not parent_id:
                            _logger.error("Could not find parent id %s, not adding to %s" % (row[key], row['external_id']))
                        else:
                            row.update({key: parent_id})
                    elif key == 'visitation_address_id':
                        if create:
                            visitation_address = {
                                'external_id': row['external_id'],
                                'name' : "%s, %s" % (row[key] ,row['external_id']),
                                'street' : row[key], #visitation_address_id contains street field for visitation address
                                'type' : 'visitation address'
                                }
                            visitation_address_transformations = {'external_id' : transformations[key]} #external id for visitation address = transformation for visitation_address_id + external id of current row 

                            if 'street' not in row and 'state_id' not in row and 'city' not in row and 'zip' not in row:
                                keys_to_update.append({'street' : row[key]})

                            if 'visitation_address_state_id' in row:
                                #visitation_address.update({'state_id' : row['visitation_address_state_id']})
                                keys_to_delete.append('visitation_address_state_id')
                                if 'visitation_address_state_id' in transformations:
                                    visitation_address_transformations.update({'state_id' : transformations['visitation_address_state_id']})
                                if ('street' not in row and 'state_id' not in row) or ('street' in row and row['street'] == row[key] and 'state_id' not in row):
                                    keys_to_update.append({'state_id' : row['visitation_address_state_id']})
                            if "visitation_address_city" in row:
                                visitation_address.update({'city' : row['visitation_address_city']})
                                keys_to_delete.append('visitation_address_city')
                                if 'visitation_address_city' in transformations:
                                    visitation_address_transformations.update({'city' : transformations['visitation_address_city']})
                                if ('street' not in row and 'city' not in row) or ('street' in row and row['street'] == row[key] and 'city' not in row): #
                                    keys_to_update.append({'city' : row['visitation_address_city']})

                            if 'visitation_address_zip' in row:
                                visitation_address.update({'zip' : row['visitation_address_zip']})
                                keys_to_delete.append('visitation_address_zip')
                                if 'visitation_address_zip' in transformations:
                                    visitation_address_transformations.update({'zip' : transformations['visitation_address_zip']})
                                if 'street' not in row and 'zip' not in row or ('street' in row and row['street'] == row[key] and 'zip' not in row) : 
                                    keys_to_update.append({'zip' : row['visitation_address_zip']})

                            if 'visitation_address_country_id' in row:
                                visitation_address.update({'country_id' : row['visitation_address_country_id']})
                                keys_to_delete.append('visitation_address_country_id')
                            #_logger.info("visitation address dict: %s" % visitation_address)
                            keys_to_delete.append(key)
                            #for visitation_address_id in self.create_partner_from_rows([visitation_address], visitation_address_transformations):
                            #   row.update({key : visitation_address_id}) 

                    elif key == 'external_id':
                        if transform == "part_org_" or transform == "part_emplr_" or transform == "part_cct_":
                            keys_to_update.append({'is_employer' : True})
                            if transform == "part_org_" or transform == "part_emplr_":
                                keys_to_update.append({'is_company' : True})
                        elif transform == "part_jbskr_":
                            #_logger.info("is jobseeker should be set to true")
                            keys_to_update.append({'is_jobseeker' : True})
                        xmlid_name = "%s%s" % (transform, row[key])
                        #_logger.info("spliting external xmlid %s" % external_xmlid)
                        external_xmlid = "%s.%s" % (self.xmlid_module, xmlid_name)
                        keys_to_delete.append(key)

            for i in range(len(keys_to_update)):
                row.update(keys_to_update[i])
                #_logger.info("row updated with %s, now %s" % (keys_to_update[i], row) )
            
            if ('name' not in row and 'lastname' not in row and 'firstname' not in row and 'type' not in row) or ('name' not in row and 'lastname' not in row and 'firstname' not in row and row['type'] == 'contact'):
                
                row.update({'name' : row['external_id']})

            if 'country_id' not in row or row['country_id'] == 'SE' or row['country_id'].lower() == 'sverige':
                country_id = self.env['ir.model.data'].xmlid_to_res_id('base.se')
                row.update({'country_id' : country_id})
            else: 
                _logger.warning("Skipping partner, wrong country %s" % row['country_id'])
                create = False

            if 'state_id' in row:
                if row['state_id'] != '0':
                    state_xmlid = "base.state_se_%s" % row['state_id']
                    state_id = self.env['ir.model.data'].xmlid_to_res_id(state_xmlid)
                    if state_id != False:
                        row.update({'state_id' : state_id})
                    else:
                        _logger.warning("state_id base.state_se_%s not found, leaving state id for %s empty" %(row['state_id'],row['external_id']))
                        row.pop('state_id', None)
                else:
                    _logger.warning("state_id is 0 for %s, leaving empty" % row['external_id'])
                    row.pop('state_id', None)
            
            keys_to_delete = keys_to_delete + ['skip', 'skip2']
            id_check = self.env['ir.model.data'].xmlid_to_res_id(external_xmlid)
            if id_check != False:
                create = False
                _logger.warning("external id already in database, skipping")
            if create:
                for i in range(len(keys_to_delete)):
                    row.pop(keys_to_delete[i], None)
                #_logger.info("creating row %s" % row)
                #_logger.info("creating external id: %s" % external_xmlid)                    
                
                partner = self.env['res.partner'].create(row)

                #_logger.info("visitation address dict before create: %s" % visitation_address)
                if visitation_address != {}:
                    #_logger.info("CREATING VISITATION ADDRESS")
                    visitation_address.update({'parent_id' : partner.id})
                    self.create_partner_from_rows([visitation_address], visitation_address_transformations)
                #self.env['res.partner'].update() #add visitation_address id to partner
                self.env['ir.model.data'].create({
                                'name': external_xmlid.split('.')[1],
                                'module': external_xmlid.split('.')[0],
                                'model': partner._name,
                                'res_id': partner.id
                                }) #creates an external id in the system for the partner.
                
                ids.append(partner.id)
            else:
                _logger.waring("Did not create row %s" % row)

        return ids
         


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
            _logger.error(u'Could not read CSV file at path %s' % path)
            raise ValueError(e)
        for i in range(len(self.header)):
            if not self.header[i] in self.data[0].keys(): 
                _logger.error(u'Row 0 could not find "%s"' % self.header[i])
                raise ValueError("Missing column '%s', columns found: %s" % (self.header[i], list(self.data[0].keys())))

    def parse(self, field_map):
        csvIter = CSVIterator(self.data,len(self.data), list(field_map.keys()), field_map)
        pairs = []
        while csvIter.hasNext():
            #_logger.info("appending row %s" % csvIter.getRow())
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

     
