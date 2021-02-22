# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "DAFA 1.0 Install all modules ",
    "version": "12.0.1.1.1",
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
    v12.0.1.0.9  - Added new version-numbers-standard. Added hr_af_holidays.\n	
    v12.0.1.0.10  - Added list of Repos that needs to be installed.\n	
    v12.0.1.0.11  - AFC-1666 added partner_flip_firstname.\n	
    v12.0.1.1.1  - Consolidation of MVP1 and MVP2 into DAFA 1.0\n	    
    \n	
    \n

# Vertel
"odoo-account||https://github.com/vertelab/odoo-account.git" 
"odoo-af||https://github.com/vertelab/odoo-af.git"
"odoo-api||https://github.com/vertelab/odoo-api.git" 
"odoo-auth||https://github.com/vertelab/odoo-auth.git" # New branch Dev-12.0-Fenix-Sprint-02 based on Dev-12.0
"odoo-base||https://github.com/vertelab/odoo-base.git"
# "odoo-contract|master|https://github.com/vertelab/odoo-contract.git"
"odoo-edi||https://github.com/vertelab/odoo-edi.git" # New branch Dev-12.0-Fenix-Sprint-02 based on Dev-12.0
"odoo-hr||https://github.com/vertelab/odoo-hr.git"
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
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        # These modules needs to be installed for  MVP1 functionality
        "account_period",  # Added period for accounting
        "af_security",      # Security-rules for AF
        # "af_statistics",  # will be renamed to web_matomo. Disabled since there is a bug - the menu does not render every time.
        "api_ipf",  # Configuration of API:s that goes towards IPF.
        "api_ipf_tlr_client",  # adds api to be used for fetching company-details from TLR
        "audit_logger",     # Logging module
        "auth_admin",
        "auth_saml_dafa",
        "auth_saml_ol",
        "auth_saml_ol_create_user",
        "auth_saml_ol_groups",
        "auth_signup_fix",
        # "auth_session_timeout", # Adds ability to set session inactive timeout as system parameter. There is a conflict with: levavrop
        # "auth_timeout",  # Disabled due to conflict with auth_saml_ol AFC-1547
        "auth_user_rights_wizard",
        "base_user_groups_dafa",
        "hr_af_holidays",  # Adds non-working-days for Af. Should be name-changed to hr_holidays_af
        "hr_departments_partner",
        "hr_employee_ciam_client", # CIAM Client for AF project, API module to handle communication between DAFA (formerly called Fenix) and CIAM
        "hr_employee_firstname",  # is required by hr_employee_firstname_extension
        "hr_employee_firstname_extension",  # is dependent on hr_employee_firstname
        "hr_employee_legacy_id",  # OCA
        "hr_employee_ssn",
        "hr_holidays", # Odoo module for leaves management 
        "hr_office",  # Adds
        # "hr_org_chart", # Disabled since Emma did not want it.
        "hr_outplacement_tab",              # dependancy to hr, outplacment
        "hr_skill",                         # dependancy to hr
        "hr_user_ciam_update",  # adds users to the CIAM-server
        "hr_timesheet",                     # dependancy to hr, analytic, project, uom
        "l10n_se",
        "l10n_se_mis",
        "mail_outplacement_report",
        "mis_builder",
        "outplacement",                     # dependancy to base, hr, mail
        "outplacement_completion_report_ipf_client",    # dependancy to res_joint_planning_af
        # "outplacement_crmsync",           # Module to be installed at a DAFA server and communicate with outplacement_dafasync" 
        "outplacement_dafa",                # 
        "outplacement_deviation_report",  # dependancy to outplacement, outplacement_deviationreport_ipf_client (which is not ready yet)
        "outplacement_deviationreport_ipf_client",  # dependancy to outplacement, outplacement_deviationreport_ipf_client (which is not ready yet)
        "outplacement_final_report",      # 
        "outplacement_final_report_ipf_client", # 
        "outplacement_final_report_send", # 
        "outplacement_joint_planning",      # dependancy to outplacement, res_joint_planning_af, outplacement_completion_report_ipf_client, project
        "outplacement_order",               # dependancy to outplacement, mail, hr_timesheet, project, task_interpreter_ipf_client
        "outplacement_order_interpreter",   # dependancy to outplacement, mail, hr_timesheet, project, task_interpreter_ipf_client
        "outplacement_partner_af_signature", # 
        "outplacement_partner_education",   # dependancy to outplacement, partner_education
        "outplacement_partner_jobs",        # dependancy to outplacement, partner_desired_jobs
        "outplacement_partner_skills",      # dependancy to outplacement, hr_skill
        "outplacement_invoice",             # dependency to outplacement, account
        "partner_af_signature",             # 
        "partner_desired_jobs",             # depenedncy to base, hr_skill, res_ssyk, res_sun
        "partner_education",                # dependency to contacts
        "partner_firstname",           # Flips first-name and lastname in contact-view.
        "partner_flip_firstname",           # Flips first-name and lastname in contact-view.
        "partner_legacy_id",                # adds a field used to store the TLR lev_id and the employees id in other salary-systems.
        "partner_ssn",
        "partner_tlr_update",
        "res_drivers_license",
        "res_interpreter_gender_preference", # Data repository for interpreter gender preference codes.
        "res_interpreter_language",         # Data repository for interpreter language codes
        "res_interpreter_remote_type",      # Data repository for interpreter type codes.
        "res_interpreter_type",
        "res_joint_planning_af",            # dependency to outplacement,
        "res_ssyk",
        "res_sun",
        "sale_management",                  # Odoo Module to display Sales
        "sale_outplacement",                # dependancy to outplacement, sale, (sale_managment), res_joint_planning_af, sale_suborder_ipf_server, l10n_se, project
        "sale_showorder_ipf_client",
        "sale_suborder_ipf_server",         # dependancy to outplacement, web
        "task_interpreter_ipf_client",      # IntepreatorBookings integration for REST-calls from the client-module to the server-module.
        "web_a11y_create-buttons",           # adds description to create and edit buttons. 
        "web_a11y_report",                  # adds a report with status of the Accessibility-status
        "web_backend_theme_af",
        "web_dashboard_dafa",
        # "web_environment_ribbon",           # Adds a ribbon with db- and version info in the left corner.
        "web_one2many_kanban",
        "web_widget_color",
        
    ],
    "application": "False",
    "installable": "True",
}
