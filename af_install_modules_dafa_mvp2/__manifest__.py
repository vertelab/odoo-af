# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "DAFA MVP 2.0 Install all modules ",
    "summary": "Adds more to DAFA MVP 1.0 Install all modules",
    "version": "12.0.1.1.0",
    "category": 'Outplacement',
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",

    "description": """
        This module adds modules on top of the DAFA MVP1 modueles. It installs all DAFA MVP2-modules at one go.\n
        \n
        Please see the depend-tab (with debug-mode) for a list of which modules are installed.\n
        \n
        v12.0.1.1  - First release. Once the module is installed, please de-install it to avoid upgrade-problems.\n
        v12.0.1.2  - Uncommented xmlrpc\n
        v12.0.1.3  - Fixed name on api_odoo_xmlrpc\n
        v12.0.1.4  - Moved modules about the Jobseeker to MVP2\n
        v12.0.1.5  - Updated modules and projects to install\n
        v12.0.1.6  - Added generic CoA\n    
        v12.0.1.0.7  - Added category Outplacement and new number standard (Odoo version 12.0 and Major, Minor, Patch)\n
        v12.0.1.1.0  - Added a complete list of dependencies to modules\n
    
        Branch Dev-12.0-Fenix-Sprint-02 fallback 12.0
        
        Vertel-project to install 

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

        OCA-projects to install

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
    """,
    "depends": [
    # Modules for DAFA MVP2:
        "api_odoo_xmlrpc"                   # dependency to base_setup (adds sync to an other Odoo-server)
        "hr_skill",                         # dependancy to hr
        "hr_timesheet",                     # dependancy to hr, analytic, project, uom
        "outplacement",                     # dependancy to base, hr, mail 
        "outplacement_completion_report_ipf_client",    # dependancy to res_joint_planning_af
        #"outplacement_deviation_report     # dependancy to outplacement, outplacement_deviationreport_ipf_client (which is not ready yet)
        "outplacement_joint_planning",      # dependancy to outplacement, res_joint_planning_af, outplacement_completion_report_ipf_client, project
        "outplacement_order_interpretor",   # dependancy to outplacement, mail, hr_timesheet, project, task_interpretor_ipf_client
        "outplacement_partner_education",   # dependancy to outplacement, partner_education_views
        "outplacement_partner_jobs",        # dependancy to outplacement, partner_desired_jobs
        "outplacement_partner_skills",      # dependancy to outplacement, hr_skill
        "outplacement_partner_ssn",         # dependency to outplacement, partner_ssn 
        "outplacement_invoice",             # dependency to outplacement, account
        "partner_desired_jobs",             # depenedncy to base, hr_skill, res_ssyk, res_sun
        "partner_education_views",          # dependency to contacts
        "res_joint_planning_af"             # dependency to outplacement,
        "sale_outplacement",                # dependancy to outplacement, sale, (sale_managment), res_joint_planning_af, sale_suborder_ipf_server, l10n_se, project
        "sale_suborder_ipf_server",         # dependancy to outplacement, web

    ],
    "application": "False",
    "installable": "True",
}
