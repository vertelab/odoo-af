# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "DAFA 1.0 Install all modules ",
    "version": "12.0.1.1.3",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        # These modules needs to be installed for  MVP1 functionality
        "account_period",        # Added period for accounting
        "af_security",           # Security-rules for AF
        # "af_statistics",      # will be renamed to web_matomo. Disabled since there is a bug - the menu does not render every time.
        "api_ipf",                      # Configuration of API:s that goes towards IPF.
        "api_ipf_tlr_client",           # adds api to be used for fetching company-details from TLR
        "audit_logger",                  # Logging module
        "auth_admin",
        "auth_saml_dafa",
        "auth_saml_ol",
        "auth_saml_ol_create_user",
        "auth_saml_ol_groups",
        "auth_signup_fix",
        # "auth_session_timeout",       # Adds ability to set session inactive timeout as system parameter. There is a conflict with: levavrop
        # "auth_timeout",            # Disabled due to conflict with auth_saml_ol AFC-1547
        "auth_user_rights_wizard",
        "base_user_groups_dafa",
        "hr_af_holidays",  # Adds non-working-days for Af. Should be name-changed to hr_holidays_af
        "hr_departments_partner",
        "hr_employee_ciam_client", # CIAM Client for AF project, API module to handle communication between DAFA (formerly called Fenix) and CIAM
        "hr_employee_firstname",  # is required by hr_employee_firstname_extension
        "hr_employee_firstname_extension",  # is dependent on hr_employee_firstname
        "hr_employee_views_dafa",   # hides a lot of fields in the hr_employee-view
        "hr_employee_legacy_id",  # OCA
        "hr_employee_ssn",
        "hr_holidays", # Odoo module for leaves management 
        "hr_office",  # Adds
        # "hr_org_chart", # Disabled since Emma did not want it.
        "hr_outplacement_tab",              # dependancy to hr, outplacment
        "hr_skill",                         # dependancy to hr
        "hr_user_ciam_update",              # adds users to the CIAM-server
        "hr_timesheet",                     # dependancy to hr, analytic, project, uom
        "l10n_se",
        "l10n_se_mis",
        "mail_outplacement_report",
        "mis_builder",
        "monitoring_status",		        # Module from Camptocamp. adds a monitoring value for automatic montitoring. We have a version here https://github.com/vertelab/odoo-base
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
    "application": False,
    "installable": True,
}
