# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Af Book Meeting 1.0 Install all modules ",
    "version": "12.0.1.0.4",
    "author": "Vertel AB",
    "description": """
        This module installs all Book Meeting-modules at one go.\n
         \n
         Please see the depend-tab (with debug-mode) for a list of which modules are installed.\n
         See https://confluence.ams.se/pages/viewpage.action?pageId=69921599 for a full list \n
         \n
         v12.0.1.1  - First release\n
         v12.0.1.2  - Updated version\n
         v12.0.1.0.3 - fixed version and dependencies\n
         v12.0.1.0.4 - added module hr_holidays_leave_repeated\n
         Once the module is installed, please de-install it to avoid depencency-problems.\n
         \n
    """,
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        # These modules needs to be installed for Book Meeting functionality
        "af_install_modules_crm_1-0", 	# Depend to all CRM-modules to simplify install later.
        "hr_af_holidays",		# /odoo-hr
        "calendar", 			# /odoo
        "calendar_af", 			# /odoo-af
        "calendar_af_360", 		# /odoo-af 
        "calendar_af_report",		# /odoo-af
        "edi_af_appointment",		# /odoo-edi
        "edi_af_as_notes", 		# /oeoo-edi
        "hr_skill", 			# /OCA	
        "ipf_planning", 		# /oodo-af
        #"mail_calendar_report_crm",	# /odoo-mail (missing repo in script) This module should be installed to be able to send meeting-notifications
        "partner_daily_notes", 		# /odoo-base
        "partner_daily_notes_edi", 	# /odoo-base
        "hr_holidays_leave_repeated" # /odooext-oca-hr
    ],
    "application": False,
    "installable": True,
}
