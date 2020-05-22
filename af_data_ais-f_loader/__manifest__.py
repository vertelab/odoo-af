# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "AIS-F Data Loader",
    "version": "12.0.1.0.1",
    "description": """

AIS-F Data Loader
==========================================
Loads database dumps from AIS-F into odoo
""",

    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        "contacts", 
        "hr", 
        "calendar", 
        "partner_view_360", 
        "partner_kpi_data", 
        "res_drivers_license", 
		"res_sni", 
		"res_ssyk", 
		"res_sun", 
		"partner_daily_notes", 
		"partner_desired_jobs",
        "partner_fax",
        "partner_firstname",
        ],
    
    "data": [
        "data/res_partner.xml"
    ],
    "application": False,
    "installable": True,
}