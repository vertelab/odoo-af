# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Af Install all modules",
    "version": "12.0.1.2",
    "author": "Vertel AB",
    "description": """
        This module installs all AF-modules at one go.\n
        Should NOT be changed.\n
        
        This module maintained here: 
         https://github.com/vertelab/odoo-af/tree/Dev-12.0-Fenix-Sprint-02/af_install_modules\n
         
        Please see the depend-tab (with debug-mode) for a list\n
        \n
         v12.0.1.2  - changed version number to four digits\n
         \n
    """,
    
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        "af_backend_tema", 
        #"contacts", 
        "partner_firstname", 
        #"hr", 
        "hr_org_chart",
        #"calendar", 
        "hr_360_view",
        #"partner_view_360", 
        "partner_kpi_data", 
        "res_drivers_license",
        "res_sni",
        #"res_ssyk",
        #"res_sun",
        "partner_daily_notes",
        "partner_desired_jobs",
        #"partner_af_case", #remove
        "test_data_demo_sv",
        "edi_af_appointment",
        #"calendar_af",
        "help_online",
        #"af_security",
        #"contact_links",
            ],

    "application": False,
    "installable": False,
}

