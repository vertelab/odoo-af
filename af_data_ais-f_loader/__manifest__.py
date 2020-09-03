# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "AIS-F Data Loader",
    "version": "12.0.1.2",
    "description": """

AIS-F Data Loader
==========================================
Loads database dumps from AIS-F into odoo \n
Database dump files must be located in AIS-F/filename.csv in 'data_dir' directory defined in odoo.conf\n
There are test dump files located in data/test_dumps\n
v12.0.1.2  - added version -explanation\n
\n
\n
""",

    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        "contacts", 
        "hr", 
        "calendar", 
        #"partner_view_360", 
        "partner_kpi_data", 
        #"res_drivers_license", 
		#"res_sni", 
		#"res_ssyk", 
		#"res_sun", 
		"partner_daily_notes", 
		"partner_desired_jobs",
        "partner_fax",
        "partner_firstname",
        ],
    
    "data": [
        "data/res.country.state.csv",
        "data/res_partner.xml",
    ],
    "application": False,
    "installable": True,
}