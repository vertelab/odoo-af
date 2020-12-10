# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Af CRM 1.0 Install all modules ",
    "version": "12.0.1.2",
    "author": "Vertel AB",
    "description": """
	This module installs all AF-modules at one go.\n
	\n
	Please see the depend-tab (with debug-mode) for a list of which modules are installed.\n
	\n
	v12.0.1.1  - First release\n
	v12.0.1.2  - First release\n
	Once the module is installed, please de-install it to avoid depencency-problems.\n
	\n
	""",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        # These modules needs to be installed for Customer Card functionality
	"af_core_menu_disabling", # will be repolaced by web_core_menu_disabling
        "af_hide_top_todo_icons",  # will be replaced by web_hide-top-todo-icons
        "af_security_rules",  # should be replaced later
        "af_statistics",
	"audit_logger",
        "auth_saml_ol_groups",
        "auth_signup",
        "auth_saml_af",
        "auth_timeout",
        "contact_links",
        "edi_af_aisf_rask_get_jobseeker",
        "edi_af_aisf_rask",
        "edi_af_aisf_trask",
        "edi_af_facility",
        "edi_af_krom_postcode",
        "edi_af_officer",
        "edi_af_bar_arbetsuppgifter",
        "ipf_ais_a",
        "ipf_planning",
        "hr_360_view",
	"hr_org_chart",
        "hr_employee_firstname",
	# "module_chart", #the module displays a graphical view of the modules dependencies
        "partner_view_360",
        "partner_mq_ipf",
        "web_a11y_filter_view", # adds descriptions to create and edit-buttons
	"web_backend_theme_af",
        "web_autocomplete_off",
	# "web_core_menu_disabling", # new module to replace af_core_menu_disabling
	"web_gui_disabeling_af", # disables 
	# "web_hide-about-user-settings", # module that hides the users-page in the top right corner.
	# "web_hide-top-todo-icons", # module that hides the icon for the todo-items.
    ],
    "application": False,
    "installable": True,
}
