# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "DAFA MVP 2.0 Install all modules ",
    "summary": "Adds more to DAFA MVP 1.0 Install all modules",
    "version": "12.0.1.1.2",
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
        v12.0.1.1.1  - outplacement_partner_ssn is moved into outplacment-module\n
        v12.0.1.1.2  - api_odoo_xmlrpc is decpreciated because it sync errors\n
    
        Branch Dev-12.0-Fenix-Sprint-02 fallback 12.0
# Vertel
"odoo-account||https://github.com/vertelab/odoo-account.git" 
"odoo-af||https://github.com/vertelab/odoo-af.git"
"odoo-api||https://github.com/vertelab/odoo-api.git" 
"odoo-auth||https://github.com/vertelab/odoo-auth.git" # New branch Dev-12.0-Fenix-Sprint-02 based on Dev-12.0
"odoo-base||https://github.com/vertelab/odoo-base.git"
# "odoo-contract|master|https://github.com/vertelab/odoo-contract.git"
"odoo-edi||https://github.com/vertelab/odoo-edi.git" # New branch Dev-12.0-Fenix-Sprint-02 based on Dev-12.0
"odoo-hr||https://github.com/vertelab/odoo-hr.git"
# "odoo-imagemagick||https://github.com/vertelab/odoo-imagemagick.git" # Not used in DAFA
"odoo-l10n_se|12.0|https://github.com/vertelab/odoo-l10n_se.git" # Need to explicitly say 12.0 else it will use the default branch Dev-12.0-Fenix-Sprint-02. We want 12.0 for the moment
"odoo-mail||https://github.com/vertelab/odoo-mail.git"
"odoo-outplacement||https://github.com/vertelab/odoo-outplacement.git"
"odoo-project||https://github.com/vertelab/odoo-project.git"
"odoo-sale||https://github.com/vertelab/odoo-sale.git"
"odoo-server-tools||https://github.com/vertelab/odoo-server-tools.git" # New branch Dev-12.0-Fenix-Sprint-02 based on Dev-12.0
"odoo-user-mail||https://github.com/vertelab/odoo-user-mail.git"
"odoo-web||https://github.com/vertelab/odoo-web.git" # New branch Dev-12.0-Fenix-Sprint-02 based on Dev-12.0
# "odoo-website||https://github.com/vertelab/odoo-website.git"

# Use Vertel versions of OCA modules
"odooext-oca-web||https://github.com/vertelab/web.git"
"odooext-oca-server-auth||https://github.com/vertelab/server-auth.git" # New branch Dev-12.0-Fenix-Sprint-02 based on Dev-12.0

# OCA
"odooext-oca-contract||https://github.com/OCA/contract.git" 
"odooext-oca-hr||https://github.com/OCA/hr.git"
"odooext-oca-mis-builder||https://github.com/OCA/mis-builder.git"
"odooext-oca-partner-contact||https://github.com/OCA/partner-contact.git"
"odooext-oca-reporting-engine||https://github.com/OCA/reporting-engine.git"
"odooext-oca-server-ux||https://github.com/OCA/server-ux.git"
"odooext-oca-social||https://github.com/OCA/social.git"
"odooext-oca-timesheet||https://github.com/OCA/timesheet.git"





""",
    "depends": [
    # Modules for DAFA MVP2:
        # "api_odoo_xmlrpc",                   # dependency to base_setup (adds sync to an other Odoo-server) Depreciated until further notice
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
        "outplacement_invoice",             # dependency to outplacement, account
        "partner_desired_jobs",             # depenedncy to base, hr_skill, res_ssyk, res_sun
        "partner_education_views",          # dependency to contacts
        "res_joint_planning_af",             # dependency to outplacement,
        "sale_outplacement",                # dependancy to outplacement, sale, (sale_managment), res_joint_planning_af, sale_suborder_ipf_server, l10n_se, project
        "sale_suborder_ipf_server",         # dependancy to outplacement, web
        "sale_management",

    ],
    "application": "False",
    "installable": "True",
}
