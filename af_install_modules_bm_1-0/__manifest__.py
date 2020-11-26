# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Af Book Meeting 1.0 Install all modules ",
    "version": "12.0.1.1",
    "author": "Vertel AB",
    "description": """
        This module installs all Book Meeting-modules at one go.\n
        \n
        Please see the depend-tab (with debug-mode) for a list of which modules are installed.\n
        \n
         v12.0.1.1  - First release\n
         
		 Once the module is installed, please de-install it to avoid depencency-problems.\n
         \n
    """,
    
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        # These modules needs to be installed for Book Meeting functionality
        "af_calendar_reports",
        "calendar_af_360",
        "edi_af_appointment",
        "hr_af_holidays", 
        "partner_daily_notes_edi",
    ],

    "application": False,
    "installable": True,
}

