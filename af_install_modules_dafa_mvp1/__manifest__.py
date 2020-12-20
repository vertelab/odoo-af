# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "DAFA MVP 1.0 Install all modules ",
    "version": "12.0.1.8",
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
	v12.0.1.7  - Added my customer_tab and hr_holidays \n
	v12.0.1.8  - Disableded Matomo due to bug. Disabled hr_org_chart since Emma did not want it.\n
	Once the module is installed, please de-install it to avoid depencency-problems.\n
	
	\n
	""",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        # These modules needs to be installed for  MVP1 functionality
	# "af_statistics",  # will be renamed to web_matomo. Disabled since there is a bug - the menu does not render every time.
	"api_ipf",  # Configuration of API:s that goes towards IPF.
	"api_ipf_tlr_client", # adds api to be used for fetching company-details from TLR
	"auth_saml_ol_groups",
        "auth_saml_af",
	"auth_user_rights_wizard", # adds functionality to assign user-credentials to coaches.
        "audit_logger",
        # "auth_timeout",  # Disabled due to conflict with auth_saml_ol AFC-1547
        "hr_departments_partner",
	"hr_user_ciam_update", # adds users to the CIAM-server
        "hr_employee_customers_tab", # adds my-customers-tab-to-employee-view
	"hr_employee_firstname", # is required by hr_employee_firstname_extension
	"hr_employee_firstname_extension", # is dependent on hr_employee_firstname
        "hr_employee_legacy_id",  # OCA
        # "hr_employee_views_fenix",
	# "hr_employee_views_user-credentials-tab", - depreciated. Replaced by user-create-wizard.	    
	# "hr_af_holidays", # dependant on hr_holidays
	"hr_office", #Adds
	# "hr_org_chart", #Disabled since Emma did not want it.
	"partner_tlr_update", 	# dependant on: partner_legacy_id, partner_firstname, api_ipf_tlr_client, hr_departments_partner
        # "web_a11y_filter_view", # adds description to create and edit buttons. Disabled since there is a bug 
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
