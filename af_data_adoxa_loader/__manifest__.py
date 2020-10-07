# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Adoxa Data Loader",
    "version": "12.0.1.3",
    "description": """

Adoxa Data Loader
==========================================
Loads database dumps from Adoxa into odoo \n
Database dump files must be located in Adoxa/filename.csv in 'data_dir' directory defined in odoo.conf\n
There are test dump files located in data/test_dumps\n
v12.0.1.2  - added version -explanation\n
v12.0.1.3  - removed state-partner.csv\n
\n
\n
""",

    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [ 
        'calendar_af'		
        ],
    
    "data": [
        "data/calendar_appointment.xml",
    ],
    "application": False,
    "installable": True,
}
