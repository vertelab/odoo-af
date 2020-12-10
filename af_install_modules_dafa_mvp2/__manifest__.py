# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "DAFA MVP 2.0 Install all modules ",
    "version": "12.0.1.3",
    "author": "Vertel AB",
    "description": """
	This module installs all Dafa MVP2-modules at one go.\n
	\n
	Please see the depend-tab (with debug-mode) for a list of which modules are installed.\n
	\n
	v12.0.1.1  - First release\n
	Once the module is installed, please de-install it to avoid depencency-problems.\n
	v12.0.1.2  - Uncommented xmlrpc\n
	v12.0.1.3  - Fixed name on api_odoo_xmlrpc\n
	\n
	""",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        # These modules needs to be installed for  MVP2 functionality
        #
        "af_sale_orders", #odoo-af
	"af_sale_filters", #odoo-af
        # "af_sales_report", #odoo-af
	"api_odoo_xmlrpc",
        # "hr_af_holidays", 
	  "hr_employee_customers_tab",
        # "send_mail_nadim", #odoo-mail
        # "mail_oe_chatter_user_groups",
        "outplacement",
	"partner_desired_jobs", #odoo-base
	"project_jobseeker_views",
	"sale_suborder_ipf_client",

    ],
    "application": False,
    "installable": True,
}
