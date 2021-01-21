# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "'CRM 1.0 Install all modules",
    "version": "12.0.1.0.1",
    "author": "Vertel AB",
    "description": """
        This module installs all modules for CRM 1.0 (Kundbild) at one go. \n
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
        "af_gui_disabeling",		# Hides Odoo-settings in upper right corner
		"af_hide_top_todo_icons",	# Hides Todo-icons in right top corner
		"af_saml_af",				# Login-module for SAML authentification
		"auth_saml_ol",				#
		"auth_saml_create_user",	#
		"af_security",				# Module for the security settings for AF
		"af_security_rules",		# Module for the security settings for AF
		"af_statistics",			# Module for the security settings for AF
		# "calendar", 				# Needed for BM1.0
        # "calendar_af", 			# Needed for BM1.0
        "contacts", 				# Odoo module to display GUI for contacts
        #"contact_links", 			# temporary removed due to a bug
        "edi_af_ais_rask", 			#
        "edi_af_ais_trask", 		#
        "edi_af_bar_arbetsuppgifter", #
        "edi_af_facility", 			#
        "edi_af_krom_postcode", 	#
        "edi_af_officer", 			#
        "edi_route", 				# Central Module with settings to Af IPF
		"hr_360_view",				# The start-page 
        "hr_af_holidays",			#
		"hr_employee_first_name", 	#
		"hr_employee_first_name_extension", #
		"hr_office", 				#
		"ipf_ais_a", 				# Used to integrate to AIS-Å
		# "hr_org_chart",			# Optional in CRM 1.0
        # "partner_daily_notes", 	# Needed for BM1.0
        "partner_desired_jobs",		#
        "partner_fax", 				# Adds fax-number for AG
        "partner_firstname", 		#
        # "partner_kpi_data", 		# Needed only for AG 1.0
        "partner_mq_ipf", 			# Listens for changes in AIS-F
        "res_drivers_license",
        "res_sni",
        "res_ssyk",
        "res_sun",
		"partner_view_360", 		# 
		"web_a11y_af", 
        "web_autocomplete_off", 
		#"web_backend_theme_af", 	# module for backendtheme developed in DAFA
        "web_core_menu_disabling",  # adds usergroup to disable core menues
		],

    "application": False,
    "installable": True,
}

