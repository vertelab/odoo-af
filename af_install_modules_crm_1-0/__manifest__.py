# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Af CRM 1.0 Install all modules ",
    "version": "12.0.1.0.6",
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
	v12.0.1.0.5  -  Updates and added repo in comments \n	
	v12.0.1.0.6  -  Disabled af_statistics to speed up theme-loading \n	
	\n
	Once the module is installed, please de-install it to avoid depencency-problems.\n
	\n
	""",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        # These modules needs to be installed for Customer Card functionality
        "af_security",			# Module for the security settings for AF
        "af_security_rules",  		# should be replaced later
        #"af_statistics",		# module to enable Matomo
        "auth_saml_af",			# odoo-af/ Login-module for SAML authentification
        "auth_saml_ol",			#
        "auth_saml_ol_create_user",	# server-auth/
        "auth_saml_ol_groups",		#
        "auth_signup",			#
        # "auth_timeout",  		# odoo-auth/ Disabled due to conflict with auth_saml_ol AFC-1547
        "audit_logger",			# odoo-server-tools/ Adds JSON-Formated logging
        #"contact_links", 		# odoo-af/ temporary removed due to a bug
        "edi_af_aisf_rask",		# odoo-edi/
        "edi_af_aisf_rask_get_jobseeker", # odoo-edi/
        "edi_af_aisf_trask",		# odoo-edi/
        "edi_af_bar_arbetsuppgifter", 	# odoo-edi/
        "edi_af_facility",		# odoo-edi/
        "edi_af_krom_postcode",		# odoo-edi/
        "edi_af_officer",		# odoo-edi/
        "edi_route", 			# odoo-edi/ Central Module with settings to Af IPF
        "hr_360_view",			# odoo-af/
        "hr_employee_firstname",	# OCA
        "hr_employee_firstname_extension", # odoo-hr
        "hr_office", 			# odoo-hr
        # "hr_org_chart",		# OCA
        "ipf_ais_a", 			# Used to integrate to AIS-Å
        "ipf_planning",			# odoo-af/
        # "module_chart", 		# odoo-base/ The module displays a graphical view of the modules dependencies
        "partner_desired_jobs",		# odoo-base/
        "partner_fax", 			# OCA Adds fax-number for AG
        "partner_firstname", 		# OCA
        # "partner_kpi_data", 		# odoo-base/ Needed only for AG 1.0
	"partner_flip_firstname",	# odoo-base/ Flips firstname and lastname
        "partner_mq_ipf", 		# odoo-base/ Listens for changes in AIS-F
        "res_drivers_license",		# odoo-base/
        "res_sni",			# odoo-base/
        "res_ssyk",			# odoo-base/
        "res_sun",			# odoo-base/
        "partner_view_360", 		# odoo-base/
        # "web_a11y_af", 		# ?
        # "web_a11y_create-buttons", 	# odoo-web/ adds descriptions to create and edit-buttons
        "web_backend_theme_af", 	# odoo-web/ module for backendtheme developed in DAFA
        # "web_autocomplete_off",	# ?
        # "web_core_menu_disabling", 	# new module to replace af_core_menu_disabling
        "web_gui_disabeling_af", 	# odoo-web/ disables
        # "web_hide-about-user-settings", # module that hides the users-page in the top right corner.
        # "web_hide-top-todo-icons", 	# module that hides the icon for the todo-items.
    ],
    "application": False,
    "installable": True,
}
