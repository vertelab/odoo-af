# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2019- Vertel AB (<http://vertel.se>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
'name': 'Project Issue Sudo',
'version': '0.1',
'summary': 'Login as a customer',
'category': 'project',
'description': """Login and reproduce an error that has been reported by a customer.
    * List users connected to a project.issue
    * Change current user-id using a button
    * Change current user to a user that is employee is not possible

""",
'author': 'Vertel AB',
'website': 'http://www.vertel.se',
'depends': ['project',],
'data': ['project_issue_view.xml',],
'installable': True,
}
