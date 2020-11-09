# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "AF Translation of Data Demo Sv",
    "version": "12.0.1.2",
    "description": """

Test Data Demo Sv
============
This module overridess original demo-data to Swedish demo-data.\n
Guidelines:\n
\tName of the file to import needs to be same name as the name of the export file\n
\tCSV file needs to be comma separeted\n
\tNeither 0 or FALSE in fields can be imported, leave the fields empty\n

PO translation:\n
\thttps://github.com/vertelab/odootools/blob/12.0/odoolangexport.pdf\n
\thttps://www.odoo.com/documentation/12.0/reference/translations.html

v12.0.1.2  - changed version number to four digits\n
           - Moved content of the module from test_data_demo_sv to this module, since the files here contain "translations" of Odoo original demo-data. \n\n
		   - commented away project-data since it is not used anymore\n
""",

    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        "contacts",
        "hr",
        "calendar",
        # "project", -> No need for this demo any more
    ],

    "data": [
        "data/calendar.event.type.csv",
        "data/hr.employee.category.csv",
        "data/resource.calendar.csv",
        # "data/hr.job.csv", -> Module not found
        "data/hr.department.csv",
        "data/res.partner.csv",
        "data/hr.employee.csv",
        "data/calendar.event.csv",
        # "data/project.project.csv", -> No need for this demo any more
        # "data/project.task.csv", -> No need for this demo any more

    ],
    "application": False,
    "installable": True,
}
