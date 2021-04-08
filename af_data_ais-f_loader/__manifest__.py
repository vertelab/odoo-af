# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "AIS-F Data Loader",
    "version": "12.0.1.5",
    "description": """

AIS-F Data Loader
==========================================
Loads database dumps from AIS-F into odoo \n
Database dump files must be located in AIS-F/filename.csv in 'data_dir' directory defined in odoo.conf\n
There are test dump files located in data/test_dumps\n
v12.0.1.2  - added version -explanation\n
v12.0.1.3  - removed state-partner.csv\n
v12.0.1.4  - replaced loading during install with a server action\n
v12.0.1.5  - Added values for timezone and language when creating users.\n
\n
""",

    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [ 
        "hr", 
        "calendar", 
        "hr_employee_firstname_extension", 
        "partner_daily_notes",
    ],
    "data": [
        "views/res_partner.xml",
    ],
    "application": False,
    "installable": True,
}
