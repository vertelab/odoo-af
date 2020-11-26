# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
	"name": "Af Dava MVP 2.0 Install all modules ",
	"version": "12.0.1.1",
	"author": "Vertel AB",
	"description": """
	This module installs all Dafa MVP2-modules at one go.\n
	\n
	Please see the depend-tab (with debug-mode) for a list of which modules are installed.\n
	\n
	v12.0.1.1  - First release\n
	Once the module is installed, please de-install it to avoid depencency-problems.\n
	\n
	""",
    
	"license": "AGPL-3",
	"website": "https://vertel.se/",
	"category": "Tools",
	"depends": [
		# These modules needs to be installed for  MVP2 functionality
		#
		#"af_sale_orders",
		#"af_sales_report",
		"hr_af_holidays",
		#"send_mail_nadim",
		#"mail_oe_chatter_user_groups",
		#"project_jobseeker_views",
		#"api_project_odoo_xmlrpc",
	],
	"application": False,
	"installable": True,
}
