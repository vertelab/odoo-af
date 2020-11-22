# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Af Install all modules",
    "version": "12.0.1.3",
    "author": "Vertel AB",
    "description": """
        This module installs all AF-modules at one go.\n
        Should NOT be changed.\n
        Please see the depend-tab (with debug-mode) for a list\n
        \n
         v12.0.1.2  - changed version number to four digits\n
         v12.0.1.3  - updated modules to include Jobseekers and Book-Meetings
         Once the module is installed, please de-install it to avoid depencency-problems.\n
         \n
    """,
    
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        # These modules needs to be installed for Customer Card functionality
        "af_gui_disabeling",
        "af_hide_top_todo_icons",
        "af_backend_tema", # should be replaced with web_backend_theme_af as soon as it is tested
        "af_core_menu_disabling", # should be replaced by 
        "af_security_rules",
        "auth_admin",
        "auth_saml_ol_groups",
        "auth_signup",
        "auth_saml_af",
        "audit_logger",
        "edi_af_officer",
        "res_drivers_license",
        "partner_view_360", 
        "contact_links",
        "partner_daily_notes_edi",
        "partner_mq_ipf",
        "edi_af_aisf_rask_get_jobseeker",
        "edi_af_aisf_rask",
        "edi_af_aisf_trask",
        "edi_af_facility",
        "edi_af_krom_postcode",
        "edi_af_officer",
        "edi_af_bar_arbetsuppgifter",
        "mail_bot", #These might be installed automatically
        "web_autocomplete_off",
        "base_import", #These might be installed automatically
        "bus", #These might be installed automatically
        "ipf_ais_a",
        "ipf_planning",
        "hr_360_view"
        "hr_org_chart",
        "hr_employee_lastnames",
        "edi_af_appointment",
        # 
        # These modules needs to be installed for Book Meeting functionality
        "af_calendar_reports",
        "calendar_af_360",
        "edi_af_appointment",
        "hr_af_holidays", 
            ],

    "application": False,
    "installable": True,
}

