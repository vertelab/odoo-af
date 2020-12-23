# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "DAFA MVP 2.0 Install all modules ",
    "version": "12.0.1.0.7",
    "category": 'Outplacement',
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
	v12.0.1.5  - Updated modules and projects to install\n
	v12.0.1.6  - Added generic CoA\n	
	v12.0.1.0.7  - Added category Outplacement\n
   
    Branch Dev-12.0-Fenix-Sprint-02 fallback 12.0
    
    #Vertels Odoo-projekts to install 
    odoo-account
    odoo-af
    odoo-api
    odoo-auth
    odoo-base
    odoo-contract
    odoo-edi
    odoo-hr
    odoo-l10n_se
    odoo-outplacement
    odoo-project
    odoo-sale
    odoo-server-tools
    odoo-web

    #OCAs Odoo-projects to install
    odooext-OCA-contract
    odooext-OCA-hr
    odooext-OCA-mis-builder
    odooext-OCA-partner-contact
    odooext-OCA-reporting-engine
    odooext-OCA-server-auth
    odooext-OCA-server-ux
    odooext-OCA-social
    odooext-OCA-timesheet
    odooext-OCA-web


    #Modules for DAFA MVP2:
        
    outplacement
    "outplacement",
    #outplacement_deviation_report	# dependancy to outplacment, 
    "outplacement_joint_planning",	# dependancy to outplacment, 
    "outplacement_order_interpretor",  	# dependancy to outplacment, mail
    "outplacement_partner_education",  	# dependancy to outplacment, res_sun, res_partner_drivers_licenses
    "outplacement_partner_jobs",        # dependancy to outplacment, res_ssyk
    outplacement_invoice
    outplacement_joint_planning
    outplacement_order_interpretor
    outplacement_partner_education
    outplacement_partner_jobs
    outplacement_partner_skills
    outplacement_partner_ssn
    res_joint_planning_af
    sale_outplacement
    hr_timesheet

    
	""",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
    # Modules for DAFA MVP2:
    "outplacement",
    #outplacement_deviation_report	# dependancy to outplacment, 
    "outplacement_joint_planning",	# dependancy to outplacment, 
    "outplacement_order_interpretor",  	# dependancy to outplacment, mail
    "outplacement_partner_education",  	# dependancy to outplacment, res_sun, res_partner_drivers_licenses
    "outplacement_partner_jobs",        # dependancy to outplacment, res_ssyk
    "outplacement_partner_skills",
    "outplacement_partner_ssn",
    "outplacement_invoice",
    "sale_management",
    "sale_outplacement",                # dependancy to sale_managment
    "hr_timesheet",

    ],
    "application": "False",
    "installable": "True",
}
