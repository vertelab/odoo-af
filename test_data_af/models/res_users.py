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

class ResUsers(models.Model):
    _inherit = "res.users"
#    def create_users(self):
#        ReadCSV("/usr/share/odoo-af/test_data_af/data/arbetsg/res.users.csv")
    @api.model
    def test(self):
        raise Warning("test")

#    def create_user(self, row):
#        self.env['res.users'].create(row)

    #create a record using data from csv

#class ReadCSV(object):
#    def __init__(self, path):
#        _logger.error('Parser %s' % path)
#       
#        try:
#            rows = []
#            f = open(path)
#            fp = tempfile.TemporaryFile()
#            fp.write(f)
#            fp.seek(0)
#            reader = csv.DictReader(fp,delimiter=",")
#            for row in reader:
#                rows.append(row)
#            fp.close()
#            self.data = rows
#        except IOError as e:
#            _logger.error(u'Could not read CSV file')
#            raise ValueError(e)
#        _logger.error('%s' % self.data[0].keys())
#        if not self.data[0].keys() == ['id', 'name', 'password']:
#            _logger.error(u'Row 0 was looking for "id", "name", "password"')
#            raise ValueError("File doesn't match the expected format")
#        self.nrows = len(self.data)
#        self.header = []
#        self.statements = []

        

#    def parse(self):
#        a = CSVIterator(self.data,len(self.data),['id', 'name', 'password'])
#        _logger.warn("blablabla: %s" % a)
#        while a.hasNext():
#            ResUsers.create_user(self, a.getRow())
#            a.next()


#class CSVIterator(object):
#    def __init__(self, data, nrows, header, header_row=1):
#        _logger.warn("blablabla: %s" % data)
#        self.nrows = nrows
#        self.row = 0
#        self.data = data
#        self.rows = nrows - 2
#        self.header = header
#        _logger.warn("blablabla: %s" % self.data)

#    def next(self):
#        if self.hasNext():
#            self.row += 1

#    def hasNext(self):
#        return self.row >= self.nrows -1
#    def getRow(self):
#        r = self.data[(self.row)]
#        return {self.header[n]: r[n].value for n in range(len(self.header))}
    
