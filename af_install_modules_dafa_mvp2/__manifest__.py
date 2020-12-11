# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "DAFA MVP 2.0 Install all modules ",
    "version": "12.0.1.4",
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
	v12.0.1.4  - Moved modules about the Jobseeker to MVP2\n
	\n
	""",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        # These modules needs to be installed for  MVP2 functionality
        #
	"af_sale_orders", 	#odoo-af
	"af_sale_filters", 	#odoo-af
        # "af_sales_report",	#odoo-af
	"api_odoo_xmlrpc",
        # "contact_links",  # Dependancy to hr_360_view, that has an old dependency to partner_notes
        # "edi_af_aisf_rask_get_jobseeker",
        # "edi_af_aisf_rask",
        # "edi_af_aisf_trask", 	# field signature does not exist in partner_daily_notes
        # "edi_af_facility",
        # "edi_af_krom_postcode",
        # "edi_af_officer",
        # "hr_af_holidays", 
	"hr_employee_customers_tab",
	# "mail_oe_chatter_user_groups",
	# "outplacement", 	# module to create an envelope around the TLR-activities.
	"outplacement_order_interpretor", # is dependant on project
	# "partner_education_views", # stored in odoo-base
	# "partner_view_360",	# stored in odoo-base
        # "partner_legacy_id",	# stored in odoo-base
        # "partner_mq_ipf", 	# This should not be installed automatically, since it consumes a liste of changes
	# "res_joint_planning_af", # sale_outplacement is dependant on this module
        "sale_outplacement",
	"sale_suborder_ipf_client",
	# "send_mail_nadim", 	#  stored in odoo-mail
        "partner_desired_jobs", # stored in odoo-base
	"project_jobseeker_views",
        # "res_drivers_license",
	"sale_suborder_ipf_client",

    ],
    "application": "False",
    "installable": "True",
}
