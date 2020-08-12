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
import gc


# TODO:
# Läs given address först, gör så att det går att läsa en rad i taget men båda tillsammans
# 

class ResPartner(models.Model):
    _inherit = "res.partner"

    xmlid_module="__ais_import__"

    @api.model
    def create_jobseekers(self):     
        headers_header = ['arbetssokande.csv', 'Notering',  'Trans', 'Odoo']
        path = os.path.join(config.options.get('data_dir'), 'AIS-F/arbetssokande.csv')
        path = "usr/share/odoo-af/af_data_ais-f_loader/data/test_dumps/arbetssokande.csv" #testing purposes only
        header_path = "usr/share/odoo-af/af_data_ais-f_loader/data/arbetssokande_mapping.csv"
        self.create_partners(headers_header, path, header_path)

        headers_header_adr = ['sok_adress.csv', 'Notering',  'Trans', 'Odoo']
        path_adr = os.path.join(config.options.get('data_dir'), 'AIS-F/sok_adress.csv')
        path_adr = "usr/share/odoo-af/af_data_ais-f_loader/data/test_dumps/sok_adress.csv" #testing purposes only
        header_path_adr = "usr/share/odoo-af/af_data_ais-f_loader/data/sok_adress_mapping.csv"
        self.create_partners(headers_header_adr, path_adr, header_path_adr)


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

        headers_header_sni = ['arbetsgivareSNI.csv', 'Notering', 'Trans', 'Odoo']
        path_sni = os.path.join(config.options.get('data_dir'), 'AIS-F/arbetsgivareSNI.csv')
        path_sni = "usr/share/odoo-af/af_data_ais-f_loader/data/test_dumps/arbetsgivareSNI.csv" #testing purposes only
        header_path_sni = "usr/share/odoo-af/af_data_ais-f_loader/data/arbetsgivareSNI_mapping.csv"
        self.create_partners(headers_header_sni, path_sni, header_path_sni)

        headers_header_ssyk = ['ssyk.csv', 'Notering', 'Trans', 'Odoo']
        path_ssyk = os.path.join(config.options.get('data_dir'), 'AIS-F/ssyk.csv')
        path_ssyk = "usr/share/odoo-af/af_data_ais-f_loader/data/test_dumps/ssyk.csv" #testing purposes only
        header_path_ssyk = "usr/share/odoo-af/af_data_ais-f_loader/data/ssyk_mapping.csv"
        self.create_partners(headers_header_ssyk, path_ssyk, header_path_ssyk)

    @api.model
    def create_organisations(self):     
        headers_header = ['organisation.csv', 'Notering', 'Trans', 'Odoo']
        path = os.path.join(config.options.get('data_dir'), 'AIS-F/organisation.csv')
        path = "usr/share/odoo-af/af_data_ais-f_loader/data/test_dumps/organisation.csv" #testing purposes only
        header_path = "usr/share/odoo-af/af_data_ais-f_loader/data/organisation_mapping.csv"
        self.create_partners(headers_header, path, header_path)
        
        headers_header_kpi = ['kpi.csv', 'Notering', 'Trans', 'Odoo']
        path_kpi = os.path.join(config.options.get('data_dir'), 'AIS-F/kpi.csv')
        path_kpi = "usr/share/odoo-af/af_data_ais-f_loader/data/test_dumps/kpi.csv" #testing purposes only
        header_path_kpi = "usr/share/odoo-af/af_data_ais-f_loader/data/kpi_mapping.csv"
        self.create_partners(headers_header_kpi, path_kpi, header_path_kpi)

        headers_header_sni = ['organisationSNI.csv', 'Notering', 'Trans', 'Odoo']
        path_sni = os.path.join(config.options.get('data_dir'), 'AIS-F/organisationSNI.csv')
        path_sni = "usr/share/odoo-af/af_data_ais-f_loader/data/test_dumps/organisationSNI.csv" #testing purposes only
        header_path_sni = "usr/share/odoo-af/af_data_ais-f_loader/data/organisationSNI_mapping.csv"
        self.create_partners(headers_header_sni, path_sni, header_path_sni)


    #TODO: 
    # För varje adress sök upp partner utifrån external_id, lägg på address
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
                #_logger.info("transformations %s"%row['Trans'])
                key = row['Trans'].split(",")[0]
                value = row['Trans'].split(",")[1]
                transformations.update({key: value})
            old_header.append(row[headers_header[0]]) #AIS-F fields
        #_logger.info("old_header: %s" % old_header)
        reader = ReadCSV(path, old_header)
        iterations = 0
        #_logger.info("get_data: %s" % next(reader.get_data()))
        #reader.seek_zero()
        for row in reader.get_data():
            #_logger.info("row: %s" % row)
            r = {}
            header = list(field_map.keys())
            #_logger.info("header: %s" % header)
            for i in range(len(header)):
                if header[i] in field_map:
                    #_logger.info("header %s: %s" % (i, row[field_map[header[i]]]))
                    r.update({header[i] : row[field_map[header[i]]]})
            #_logger.info("creating row %s" %r)
            self.create_partner_from_row(r, transformations)
            iterations += 1
            if iterations > 500:
                self.env.cr.commit()
               #_loger.info("commit")
                iterations = 0
        reader.close()
        
    
    @api.model
    def create_partner_from_row(self, row, transformations):
        #TODO: läs given address först, skapa den och sen lägg på fältet given_address_id = xmlid_to_res_id
                
        #_logger.info("row: %s" % row)
        transformed_row_and_id = self.transform(row, transformations)
        if transformed_row_and_id != {}:
            #_logger.info('transformed_row_and_id: %s' % transformed_row_and_id)
            external_xmlid = transformed_row_and_id['external_xmlid']
            transformed_row = transformed_row_and_id['row']
            secondary_address = transformed_row_and_id['secondary_address']
            secondary_address_transformations = transformed_row_and_id['secondary_address_transformations']
                
            
           #_logger.info("creating partner: %s" % transformed_row)

            transformed_row.pop('state_id', None)
            transformed_row.pop('education_level', None)
            transformed_row.pop('country_id', None)
            transformed_row.pop('jobseeker_category', None)
            
            partner = self.env['res.partner'].create(transformed_row)

            #_logger.info("visitation address dict before create: %s" % visitation_address)
            if secondary_address != {}:
                #_logger.info("CREATING VISITATION ADDRESS")
                secondary_address.update({'parent_id' : partner.id})
                self.create_partner_from_row(secondary_address, secondary_address_transformations)
            #self.env['res.partner'].update() #add visitation_address id to partner
            self.env['ir.model.data'].create({
                            'name': external_xmlid.split('.')[1],
                            'module': external_xmlid.split('.')[0],
                            'model': partner._name,
                            'res_id': partner.id
                            }) #creates an external id in the system for the partner.
        
        else:
            _logger.warning("Did not create row %s" % row)
         
    @api.model
    def create_kpi_from_row(self, row):
        _logger.info("got to create kpi method")
        external_xmlid = '%s%s' % (self.xmlid_module, row['external_id'])
        external_id = row['external_id']
        row.pop('external_id', None)
        id_check = self.env['ir.model.data'].xmlid_to_res_id(external_xmlid)
        if not id_check:
            _logger.info("creating kpi: %s" % row)
            kpi = self.env['res.partner.kpi'].create(row)

            self.env['ir.model.data'].create({
                                'name': external_id,
                                'module': self.xmlid_module,
                                'model': kpi._name,
                                'res_id': kpi.id
                                })
    
        
    # @api.model #ska använda api istället, om det inte blir api, flytta till separat modul som körs efteråt
    # def create_daily_note_from_row(self, row):
    #     external_xmlid = '%s%s' % (self.xmlid_module, row['external_id'])
    #     external_id = row['external_id']
    #     row.pop('external_id', None)
    #     id_check = self.env['ir.model.data'].xmlid_to_res_id(external_xmlid)
    #     if id_check != False:
    #         kpi = self.env['res.partner.notes'].create(row)

    #         self.env['ir.model.data'].create({
    #                             'name': external_id,
    #                             'module': self.xmlid_module,
    #                             'model': kpi._name,
    #                             'res_id': kpi.id
    #                             })

    @api.model
    def create_desired_jobs_from_row(self, row):
        external_xmlid = '%s%s' % (self.xmlid_module, row['external_id'])
        external_id = row['external_id']
        row.pop('external_id', None)
        id_check = self.env['ir.model.data'].xmlid_to_res_id(external_xmlid)
        if id_check != False:
            _logger.info("creating desired job: %s" % row)

            job = self.env['res.partner.jobs'].create(row)

            self.env['ir.model.data'].create({
                                'name': external_id,
                                'module': self.xmlid_module,
                                'model': job._name,
                                'res_id': job.id
                                })

    @api.model
    def transform(self, row, transformations):
        create = True
        external_xmlid = ""
        keys_to_delete = []
        keys_to_update = []
        secondary_address = {}
        secondary_address_transformations = {}
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

        if 'type' not in row: #new
            row['type'] = 'contact'

        for key in row.keys():
            if key in transformations:
                transform = transformations[key]
                if transform == 'skip':
                    create = False
                    _logger.warning("Skipping partner, contains skipping flag %s" % row[transformations[key]])
                    break
                elif transform == 'skip_if_u':
                    if row[key].lower() == 'u':
                        create = False
                        _logger.warning("Skipping partner, contains U in ORGTYP")
                        break
                elif transform == 'skip_if_j':
                    if row[key].lower() == 'j':
                        create = False
                        _logger.warning("Skipping partner, contains J in RADERAD" )
                        break
                if key == 'partner_id':
                    if 'fiscal_year' in row:
                        
                        fiscal_year_date = "%s-%s-01" % (row['fiscal_year'][:4], row['fiscal_year'][4:6])
                        partner_id = self.env['res.partner'].search([('company_registry', '=', row['partner_id'])]).id
                        self.create_kpi_from_row({
                            'external_id': "%s%s" % (transformations['external_id'],row['external_id']), 
                            'partner_id': partner_id,
                            'fiscal_year': fiscal_year_date,
                            'profit': row['profit'],
                            'turnover': row['turnover'],
                            'employees': row['employees']
                            })
                        create = False
                    else:
                        partner_xmlid_name = "%s%s" % (transform, row[key])
                        partner_xmlid = "%s.%s" % (self.xmlid_module, partner_xmlid_name)
                        partner_id = self.env['ir.model.data'].xmlid_to_res_id(partner_xmlid)
                        
                        partner = self.env['res.partner'].search_read([('id', '=', partner_id)], ['street', 'street2', 'city', 'zip'])[0]
        
                        if 'ssyk_id' in row:
                            ssyk_xmlid = "res_ssyk.ssyk_%s" % row['ssyk_id']
                            ssyk_id = self.env['ir.model.data'].xmlid_to_res_id(ssyk_xmlid)
                            if ssyk_id != False:
                                self.env['res.partner'].browse(partner_id).write({'ssyk_ids' : [(4,ssyk_id)]})
                            else:
                                _logger.warning("ssyk %s not found, skipping" % row['ssyk_id'])
                            
                            create = False

                        if 'sni_id' in row:
                            sni_xmlid = "res_sni.sni_%s" % row['sni_id']
                            sni_id = self.env['ir.model.data'].xmlid_to_res_id(sni_xmlid)
                            if sni_id != False:
                                self.env['res.partner'].browse(partner_id).write({'sni_ids' : [(4,sni_id)]})
                            else:
                                _logger.warning("sni %s not found, skipping" % row['sni_id'])
                            create = False

                        if 'type' in row:
                            if row['type'].lower() == 'egen_angiven':
                                partner.update({'type': 'given address', 'parent_id': partner['id'], 'external_id': '%s_%s' % (row['external_id'],row['id'])})
                                partner.pop('id', None)
                                self.create_partner_from_row(partner, {'external_id': transformations['external_id'], 'parent_id': transformations['partner_id']})
                                #skapa och koppla med parent_id

                            elif row['type'].lower() == 'folkbokforing': 
                                partner['street'] = row['street']
                                if 'street2' in row:
                                    partner['street2'] = row['street2']
                                if 'zip' in row:                               
                                    partner['zip'] = row['zip']
                                if 'city' in row:
                                    partner['city'] = row['city']
                                self.env['res.partner'].browse(partner_id).write({
                                        'street': partner['street'],
                                        'street2': partner['street2'],
                                        'zip': partner['zip'],
                                        'city': partner['city']
                                        })  
                            elif row['type'].lower() == 'egen_utlandsk':
                                _logger.warning("foreign address on jobseeker, skipping")
                            create = False
                            keys_to_delete.append('type')
                if key == 'parent_id': 
                    parent_xmlid_name = "%s%s" % (transform, row[key])
                    parent_xmlid = "%s.%s" % (self.xmlid_module, parent_xmlid_name)
                    #_logger.info("parent xmlid: %s" % parent_xmlid)
                    parent_id = self.env['ir.model.data'].xmlid_to_res_id(parent_xmlid)
                    #_logger.info("parent res_id: %s" % parent_id)
                    if parent_id == False:
                        keys_to_delete.append(key)
                        _logger.error("Could not find parent id %s, not adding to %s" % (row[key], row['external_id']))
                    else:
                        row.update({key: parent_id})
                elif key == 'visitation_address_id':
                    if create:
                        visitation_address = {
                            'external_id': row['external_id'],
                            'name' : "",
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
                        keys_to_update.append({'is_jobseeker' : True})
                    xmlid_name = "%s%s" % (transform, row[key])
                    #_logger.info("spliting external xmlid %s" % external_xmlid)
                    external_xmlid = "%s.%s" % (self.xmlid_module, xmlid_name)
                    keys_to_delete.append(key)

        for i in range(len(keys_to_update)):
            row.update(keys_to_update[i])
            #_logger.info("row updated with %s, now %s" % (keys_to_update[i], row) )
        
        if create and (('name' not in row and 'lastname' not in row and 'firstname' not in row and 'type' not in row) or ('name' not in row and 'lastname' not in row and 'firstname' not in row and row['type'] == 'contact')):
            row.update({'name' : row['external_id']})

        if 'country_id' not in row or row['country_id'] == 'SE' or row['country_id'].lower() == 'sverige':
            country_id = self.env['ir.model.data'].xmlid_to_res_id('base.se')
            row.update({'country_id' : country_id})
        else: 
            _logger.warning("Skipping partner, wrong country %s" % row['country_id'])
            create = False

        if 'state_id' in row:
            if row['state_id'] != '0':
                if len(row['state_id']) == 3:
                    state_xmlid = "base.state_se_0%s" % row['state_id']
                else:
                    state_xmlid = "base.state_se_%s" % row['state_id']
                state_id = self.env['ir.model.data'].xmlid_to_res_id(state_xmlid)
                if state_id != False:
                    row.update({'state_id' : state_id})
                else:
                    _logger.warning("state_id base.state_se_%s not found, leaving state_id for %s empty" %(row['state_id'],row['external_id']))
                    row.pop('state_id', None)
            else:
                _logger.warning("state_id is 0 for %s, leaving empty" % row['external_id'])
                row.pop('state_id', None)
        
        if 'sun_id' in row:
            if row['sun_id'] != '0':
                sun_xmlid = "res_sun.sun_%s" % row['sun_id']
                sun_id = self.env['ir.model.data'].xmlid_to_res_id(sun_xmlid)
                if sun_id != False:
                    row.update({'sun_id' : sun_id})
                else:
                    _logger.warning("sun_id sun_%s not found, leaving sun_id for %s empty" %(row['sun_id'],row['external_id']))
                    row.pop('sun_id', None)
                          
        if 'education_level' in row:
            if row['education_level'] != '0':
                education_level_xmlid = "res_sun.education_level_%s" % row['education_level']
                education_level = self.env['ir.model.data'].xmlid_to_res_id(education_level_xmlid)
                if education_level != False:
                    row.update({'education_level' : education_level})
                else:
                    _logger.warning("education_level sun_%s not found, leaving education_level for %s empty" %(row['education_level'],row['external_id']))
                    row.pop('education_level', None)
            else:
                _logger.warning("education_level is 0 for %s, leaving empty" % row['external_id'])
                row.pop('education_level', None)
        
        for key in row.keys():
            if "skip" in key:
                keys_to_delete.append(key)
       #_logger.info("keys to delete: %s" % keys_to_delete)
        for i in range(len(keys_to_delete)):
                row.pop(keys_to_delete[i], None)
        id_check = self.env['ir.model.data'].xmlid_to_res_id(external_xmlid)
        if id_check != False:
            create = False
            _logger.warning("external id already in database, skipping")
        
       #_loger.info('create?: %s' % create)
        if create:
            return {'row': row, 
                    'external_xmlid': external_xmlid, 
                    'secondary_address': secondary_address, 
                    'secondary_address_transformations': secondary_address_transformations,
                    }
        else:
            return {}


class ReadCSV(object):
    def __init__(self, path, header): 
        self.header = header
        try:
            #rows = []
            self.f = open(path)
            self.f.seek(0)
            reader = csv.DictReader(self.f,delimiter=",")
            #for row in reader:
            #    rows.append(row)
            
            
            self.data = reader
        except IOError as e:
            _logger.error(u'Could not read CSV file at path %s' % path)
            raise ValueError(e)
        
        row = next(self.data)
        self.f.seek(0)
        next(self.data)
        for i in range(len(self.header)):
            if not self.header[i] in row.keys(): 
                _logger.error(u'Row 0 could not find "%s"' % self.header[i])
                raise ValueError("Missing column '%s', columns found: %s" % (self.header[i], list(row.keys())))
        
    
    def get_data(self):
        return self.data
    def get_header(self):
        return self.header
    def close(self):
        self.f.close()
    def seek_zero(self):
        self.f.seek(0)

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
        rows = []
        self.seek_zero()
        for row in self.data:
            rows.append(row)
        self.seek_zero()
        csvIter = CSVIterator(rows,len(rows), self.header, field_map)
        pairs = []
        while csvIter.hasNext():
            csvIter.next()
            #_logger.info("appending header row %s" % csvIter.getRow())
            pairs.append(csvIter.getRow())
            
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
        return self.row <= self.rows

    def getRow(self):
        r = {}
        for i in range(len(self.header)):
            if self.header[i] in self.field_map:
                #_logger.info("Updating row nr %s of %s %s : %s" % (self.row, self.rows, self.header[i], self.data[self.row][self.field_map[self.header[i]]]))
                r.update({self.header[i] : self.data[self.row][self.field_map[self.header[i]]]})

        return r

     
