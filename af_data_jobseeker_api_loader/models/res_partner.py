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
from odoo.tools.profiler import profile

_logger = logging.getLogger(__name__)



class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create_jobseekers(self):
        header = ['SOKANDE_ID']
        path = os.path.join(
            config.options.get('data_dir'),
            'AIS-F/arbetssokande.csv')
        path = "/usr/share/odoo-af/af_data_ais-f_loader/data/test_dumps/arbetssokande.csv" # testing purposes only
        self.create_partners_from_api(header, path)

    
    @api.model
    def create_partners_from_api(self, header, path):
        reader = ReadCSV(path, header)
        iterations = 0
        for row in reader.get_data():
            self.env['res.partner'].rask_controller(row[header], '0', '0','0')
            iterations += 1
            if iterations > 500:
                self.env.cr.commit()
                iterations = 0
        reader.close()


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
            #_logger.info("appending row %s" % csvIter.getRow())
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
                r.update({self.header[i]: self.data[self.row]
                          [self.field_map[self.header[i]]]})

        return r
