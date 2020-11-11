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

import gc
import tempfile
import os
import csv
from odoo.tools import config
from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class CalendarOccasion(models.Model):
    _inherit = "calendar.appointment"

    xmlid_module = "__adoxa_import__"

    @api.model
    def create_occasions(self):
        headers_header = ['occasions.csv', 'Notering', 'Trans', 'Odoo']
        path = os.path.join(
            config.options.get('data_dir'),
            'Adoxa/occasions.csv')
        # testing purposes only
        path = "/usr/share/odoo-af/af_data_adoxa_loader/data/test_dumps/occasions.csv"
        header_path = "/usr/share/odoo-af/af_data_adoxa_loader/data/occasion_mapping.csv"
        self.create_calendar_objs(headers_header, path, header_path)

    @api.model
    def create_appointments(self):
        headers_header = ['appointments.csv', 'Notering', 'Trans', 'Odoo']
        path = os.path.join(
            config.options.get('data_dir'),
            'Adoxa/appointments.csv')
        # testing purposes only
        path = "/usr/share/odoo-af/af_data_adoxa_loader/data/test_dumps/appointments.csv"
        header_path = "/usr/share/odoo-af/af_data_adoxa_loader/data/appointment_mapping.csv"
        self.create_calendar_objs(headers_header, path, header_path)

    def create_calendar_objs(self, headers_header, path, header_path):
        header_reader = ReadCSV(header_path, headers_header)
        header_rows = header_reader.parse_header()
        old_header = []
        field_map = {}
        transformations = {}
        for row in header_rows:

            if row['Odoo'] != '' and "!" not in row['Odoo']:
                field_map.update({row['Odoo']: row[headers_header[0]]})
            if row['Trans'] != '':
                key = row['Trans'].split(",")[0]
                value = row['Trans'].split(",")[1]
                transformations.update({key: value})
            old_header.append(row[headers_header[0]])  # adoxa fields
        reader = ReadCSV(path, old_header)
        iterations = 0
        for row in reader.get_data():
            r = {}
            header = list(field_map.keys())
            for i in range(len(header)):
                if header[i] in field_map:
                    r.update({header[i]: row[field_map[header[i]]]})
            self.create_occasion_from_row(r, transformations)
            iterations += 1
            if iterations > 500:
                self.env.cr.commit()
                iterations = 0
        reader.close()

    @api.model
    def create_occasion_from_row(self, row, transformations):
        transformed_row_and_id = self.transform(row, transformations)
        if transformed_row_and_id != {}:
            external_xmlid = transformed_row_and_id['external_xmlid']
            transformed_row = transformed_row_and_id['row']
            _logger.info("creating row: %s" % transformed_row)
            if 'occasion_ids' in transformed_row:
                obj = self.env['calendar.appointment'].create(transformed_row)

            else:
                obj = self.env['calendar.occasion'].create(transformed_row)

            self.env['ir.model.data'].create({
                'name': external_xmlid.split('.')[1],
                'module': external_xmlid.split('.')[0],
                'model': obj._name,
                'res_id': obj.id
            })  # creates an external id in the system for the partner.

        else:
            _logger.warning("Did not create row %s" % row)

    @api.model
    def transform(self, row, transformations):
        create = True
        external_xmlid = ""
        keys_to_delete = []
        keys_to_update = []
        for key in row.keys():
            if row[key] == '(null)' or row[key] == '':
                keys_to_delete.append(key)
        for i in range(len(keys_to_delete)):
            row.pop(keys_to_delete[i], None)
        keys_to_delete = []

        for key in row.keys():
            if key in transformations:
                transform = transformations[key]

                if key == 'external_id':
                    xmlid_name = "%s%s" % (transform, row[key])
                    external_xmlid = "%s.%s" % (self.xmlid_module, xmlid_name)
                    keys_to_delete.append(key)
                elif key == 'partner_id':
                    ipf = self.env.ref('af_ipf.ipf_endpoint_customer').sudo()
                    res = ipf.call(customer_id=row[key])
                    pnr = None
                    if res:
                        pnr = res.get('ids', {}).get('pnr')
                        if pnr:
                            pnr = '%s-%s' % (pnr[:8], pnr[8:12])
                    if pnr:
                        partner = self.env['res.partner'].search(
                            [('social_sec_nr', '=', pnr)])
                        if len(partner) > 0:
                            row[key] = partner[0].id
                        else:
                            _logger.warn(
                            "could not find jobseeker corresponding to %s" %
                            pnr)
                            row[key] = False
                        
                    else:
                        _logger.warn(
                            "could not find person corresponding to %s, skipping" %
                            row[key])
                        create = False
                elif key == 'occasion_idss':
                    xmlid = "%s.%s%s" % (
                        self.xmlid_module, transform, row[key])
                    occasion_ids = self.env['ir.model.data'].xmlid_to_res_id(
                        xmlid)
                    row[key] = [(6, 0, [occasion_ids])]
                elif key == 'start' or key == 'stop':
                    row[key] = "%s %s" % (row['date'].split(' ')[0], row[key])
                elif key == 'duration_selection':
                    if row['duration'] == "60":
                        row[key] = "1 hour"
                    elif row['duration'] == "30":
                        row[key] = "30 minutes"
                    else:
                        create = False
                elif key == 'type_id':
                    # Meeting type 23 is deprecated and replaced with meeting type 26,
                    # see calendar_af/data/calendar.appointment.type.csv for
                    # descriptions of the meeting types
                    if row[key] == "23":
                        row[key] == "26"
                    type_id = self.env['calendar.appointment.type'].search(
                        [('ipf_num', '=', row[key])])
                    if type_id:
                        row[key] = type_id.id
                        row['name'] = type_id.name
                    else:
                        create = False
                elif key == 'state':
                    if 'occasion_ids' in row:
                        translation_dict = {
                            'NULL': 'confirmed',
                            '1': 'done',
                            '2': 'done',
                        }
                    else:
                        translation_dict = {
                            'NULL': 'request',
                            '6': 'ok',
                            '7': 'fail',
                        }
                    row[key] = translation_dict[row[key]]
                elif key == 'location_id': #location is found through user_id.location_id, this might be needed in the future
                    row[key] = self.env['hr.location'].search([('location_code', '=', row[key])]).id
                    keys_to_delete.append(key)
                elif key == 'user_id':
                    row[key] = self.env['res.users'].search(
                        [('login', '=', row[key])]).id
                elif key == 'additional_booking':
                    translation_dict = {
                        'Ja': True,
                        'Nej': False,
                    }
                    row[key] = translation_dict[row[key]]


                keys_to_delete.append("date")

        for i in range(len(keys_to_update)):
            row.update(keys_to_update[i])

        for key in row.keys():
            if "skip" in key:
                keys_to_delete.append(key)
        for i in range(len(keys_to_delete)):
            row.pop(keys_to_delete[i], None)
        id_check = self.env['ir.model.data'].xmlid_to_res_id(external_xmlid)
        if id_check:
            create = False
            _logger.warning("external id already in database, skipping")

        if create:
            return {
                'row': row,
                'external_xmlid': external_xmlid
            }
        else:
            return {}


class ReadCSV(object):
    def __init__(self, path, header):
        self.header = header
        try:
            self.f = open(path)
            self.f.seek(0)
            reader = csv.DictReader(self.f, delimiter=",")
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
                raise ValueError(
                    "Missing column '%s', columns found: %s" %
                    (self.header[i], list(
                        row.keys())))

    def get_data(self):
        return self.data

    def get_header(self):
        return self.header

    def close(self):
        self.f.close()

    def seek_zero(self):
        self.f.seek(0)

    def parse(self, field_map):
        csvIter = CSVIterator(
            self.data, len(
                self.data), list(
                field_map.keys()), field_map)
        pairs = []
        while csvIter.hasNext():
            pairs.append(csvIter.getRow())
            csvIter.next()
        return pairs

    def parse_header(self):
        field_map = {}
        for i in range(len(self.header)):
            field_map.update({self.header[i]: self.header[i]})
        rows = []
        self.seek_zero()
        for row in self.data:
            rows.append(row)
        self.seek_zero()
        csvIter = CSVIterator(rows, len(rows), self.header, field_map)
        pairs = []
        while csvIter.hasNext():
            csvIter.next()
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
                r.update({self.header[i]: self.data[self.row]
                          [self.field_map[self.header[i]]]})

        return r
