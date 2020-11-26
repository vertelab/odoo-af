# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Af Dava MVP 1.0 Install all modules ",
    "version": "12.0.1.2",
    "author": "Vertel AB",
    "description": """
	This module installs all Dafa MVP1-modules at one go.\n
	\n
	Please see the depend-tab (with debug-mode) for a list of which modules are installed.\n
	\n
	v12.0.1.1  - First release\n
	v12.0.1.2  - Updates in the list\n
	
	Once the module is installed, please de-install it to avoid depencency-problems.\n
	
	\n
	""",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        # These modules needs to be installed for  MVP2 functionality
        "auth_saml_ol_groups",
        "auth_saml_af",
        "audit_logger", 
        "audit_timeout", #odoo-auth
        "res_drivers_license",
        "partner_view_360",
        "contact_links", # Dependancy to hr_360_view, that has an old dependency to partner_notes
	# "partner_mq_ipf", This should not be installed automatically, since it consumes a liste of changes
        "edi_af_aisf_rask_get_jobseeker",
        "edi_af_aisf_rask",
        # "edi_af_aisf_trask", #field signature does not exist
        "edi_af_facility",
        "edi_af_krom_postcode",
        "edi_af_officer",
        "hr_org_chart",
        "hr_employee_lastnames",
	# "web_a11y_filter_view",   
	# "web_a11y_report",  
        "web_autocomplete_off",
	"web_backend_theme_af",
        "web_employee_views_fenix",
        "web_employee_views_user-credentials-tab",
        "web_dashboard_fenix",   
    ],
    "application": False,
    "installable": True,
}
