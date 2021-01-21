# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "'BM1 Install all modules",
    "version": "12.0.1.0.1",
    "author": "Vertel AB",
    "description": """
        This module installs all modules for Book Meeting 1.0 (Kundbild) at one go. \n
        Please see the depend-tab (with debug-mode) for a list \n
        See https://confluence.ams.se/pages/viewpage.action?pageId=69921599 for a full list \n
        \n
		v12.0.1.0.1  - changed version number to four digits \n
        \n
    """,
    
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        "af_install_modules_CRM1", 	# Depend to all CRM-modules to simplify install later.
		"calendar", 				#
        "calendar_af", 				#
        "calendar_af_360", 			# 
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

