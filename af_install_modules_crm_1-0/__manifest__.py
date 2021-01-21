# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Af CRM 1.0 Install all modules ",
    "version": "12.0.1.0.4",
    "author": "Vertel AB",
    "description": """
	This module installs all AF-modules at one go.\n
	\n
	Please see the depend-tab (with debug-mode) for a list of which modules are installed.\n
    See https://confluence.ams.se/pages/viewpage.action?pageId=69921599 for a full list \n
    \n	
	\n
	v12.0.1.1  - First release\n
	v12.0.1.2  - First release\n
	v12.0.1.3   Disabled auth_timeout due to conflict with auth_saml_ol AFC-1547\n
	v12.0.1.0.4  -  Updated list and changed version number to four digits \n	
	\n
	Once the module is installed, please de-install it to avoid depencency-problems.\n
	\n
	""",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        # These modules needs to be installed for Customer Card functionality
        "af_core_menu_disabling", # will be repolaced by web_core_menu_disabling
		"af_gui_disabeling",		# Hides Odoo-settings in upper right corner
        "af_hide_top_todo_icons",  # will be replaced by web_hide-top-todo-icons
        "af_hide_top_todo_icons",	# Hides Todo-icons in right top corner
		"af_saml_af",				# Login-module for SAML authentification
		"auth_saml_ol",				#
		"auth_saml_create_user",	#
		"af_security",				# Module for the security settings for AF

        "af_security_rules",  # should be replaced later
        "af_statistics",
        "audit_logger",
        "auth_saml_ol_groups",
        "auth_signup",
        "auth_saml_af",
        # "auth_timeout",  # Disabled due to conflict with auth_saml_ol AFC-1547
        #"contact_links", 			# temporary removed due to a bug
        "edi_af_aisf_rask",
        "edi_af_aisf_rask_get_jobseeker",
        "edi_af_aisf_trask",
        "edi_af_bar_arbetsuppgifter", #
        "edi_af_facility",
        "edi_af_krom_postcode",
        "edi_af_officer",
        "edi_af_bar_arbetsuppgifter",
        "edi_route", 				# Central Module with settings to Af IPF
        "hr_360_view",
        "hr_employee_firstname",
		"hr_employee_first_name_extension", #
		"hr_office", 				#
        # "hr_org_chart",
		"ipf_ais_a", 				# Used to integrate to AIS-Å
        "ipf_planning",

        # "module_chart", #the module displays a graphical view of the modules dependencies
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
        "web_a11y_filter_view", # adds descriptions to create and edit-buttons
		#"web_backend_theme_af", 	# module for backendtheme developed in DAFA
        "web_autocomplete_off",
        # "web_core_menu_disabling", # new module to replace af_core_menu_disabling
        "web_gui_disabeling_af", # disables 
        # "web_hide-about-user-settings", # module that hides the users-page in the top right corner.
        # "web_hide-top-todo-icons", # module that hides the icon for the todo-items.
    ],
    "application": False,
    "installable": True,
}
