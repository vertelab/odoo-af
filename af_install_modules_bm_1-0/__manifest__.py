# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Af Book Meeting 1.0 Install all modules ",
    "version": "12.0.1.2",
    "author": "Vertel AB",
    "description": """
        This module installs all Book Meeting-modules at one go.\n
        \n
        Please see the depend-tab (with debug-mode) for a list of which modules are installed.\n
		See https://confluence.ams.se/pages/viewpage.action?pageId=69921599 for a full list \n
        \n
         v12.0.1.1  - First release\n
		 v12.0.1.2  - Updated version\n
         
		 Once the module is installed, please de-install it to avoid depencency-problems.\n
         \n
    """,
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        # These modules needs to be installed for Book Meeting functionality
		"af_calendar_reports",
        "af_install_modules_CRM1", 	# Depend to all CRM-modules to simplify install later.
		"hr_af_holidays",
		"calendar", 				#
        "calendar_af", 				#
        "calendar_af_360", 			# 
        "calendar_af_report",
		"edi_af_appointment",		#
		"edi_af_as_notes", 			#
		"hr_skill", 				#		
		"ipf_planning", 			#
        "partner_daily_notes", 		# 
		"parnter_daily_notes_edi", 	# 
    ],
    "application": False,
    "installable": True,
}
