# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "DAFA MVP 1.0 Install all modules ",
    "version": "12.0.1.6",
    "author": "Vertel AB",
    "description": """
	This module installs all Dafa MVP1-modules at one go.\n
	\n
	Please see the depend-tab (with debug-mode) for a list of which modules are installed.\n
	\n
	v12.0.1.1  - First release\n
	v12.0.1.2  - Updates in the list\n
	v12.0.1.3  - Added Auth_user_rights_wizard and CIAM-modules, corrected spelling of auth_timeout\n
	v12.0.1.4  - Removed items outside of MVP1 \n
	v12.0.1.5  - Added more modules \n
	v12.0.1.6  - Removed auth_login \n
	Once the module is installed, please de-install it to avoid depencency-problems.\n
	
	\n
	""",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        # These modules needs to be installed for  MVP1 functionality
	"af_statistics",  # will be renamed to web_matomo
	"api_ipf_tlr_client", # adds api to be used for fetching company-details from TLR
	"auth_saml_ol_groups",
        "auth_saml_af",
	"auth_user_rights_wizard", # adds functionality to assign user-credentials to coaches.
        "audit_logger",
        # "auth_timeout",  # Disabled due to conflict with auth_saml_ol AFC-1547
        "hr_departments_partner",
	"hr_user_ciam_update", # adds users to the CIAM-server
        "hr_employee_firstname", # is required by hr_employee_firstname_extension
	"hr_employee_firstname_extension", # is dependent on hr_employee_firstname
        "hr_employee_legacy_id",  # OCA
        # "hr_employee_views_fenix",
	# "hr_employee_views_user-credentials-tab", - depreciated. Replaced by user-create-wizard.	    
	"hr_office", #Adds
	"hr_org_chart",
	"partner_tlr_update",
        "web_a11y_filter_view", # adds description to create and edit buttons
        "web_a11y_report",      # adds a report with status of the Accessibility-status
        "partner_legacy_id",	# adds a field used to store the TLR lev_id and the employees id in other salary-systems.
        # "web_autocomplete_off",
        "web_backend_theme_af",
        "web_dashboard_dafa",
	"web_environment_ribbon", # Adds a ribbon with db- and version info in the left corner.
	    
    ],
    "application": "False",
    "installable": "True",
}
