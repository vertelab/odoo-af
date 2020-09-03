# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Af Install all modules",
    "version": "12.0.1.2",
    "author": "Vertel AB",
    "description": """
        This module installs all AF-modules at one go.\n
        Please see the depend-tab (with debug-mode) for a list\n
        \n
         v12.0.1.2  - changed version number to four digits\n
         \n
    """,
    
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        ##
        "website",
        ## odoo-af
        "af_base_demo",
        "af_bugherd",
        #"af_calendar_report", # module named "zeep"
        "af_data_ais-f_loader",
        "af_demodata",
        # ~ "af_hr_demo",
        "af_module_template",
        # ~ "af_project_demo",
        "af_rest_appointment",
        "af_rest_core",
        "af_security",
        "af_security_rules",
        "af_testdata",
        "calender_timereport",
        "contact_links",
        "hr_360_view",
        "partner_af_case",
        "test_data_af",
        "test_data_demo_sv",
        ## odoo-base
        "daily_notes",
        "hr_skill_ipf",
        "partner_activities",
        "partner_daily_notes",
        "partner_daily_notes_activity",
        # ~ "partner_desiredjob",
        "partner_kpi_data",
        "partner_skills",
        "partner_vcard",
        "partner_view_360",
        "pgpool",
        "res_drivers_license",
        "res_sni",
        "res_ssyk",
        "res_sun",
        "timereport_extra_dimension",
        ## default
        "af_backend_tema", 
        "contacts", 
        "partner_firstname", 
        "hr", 
        "hr_org_chart",
        "calendar", 
        "hr_360_view",
        "partner_view_360", 
        "partner_kpi_data", 
        "res_drivers_license",
        "res_sni",
        "res_ssyk",
        "res_sun",
        "partner_daily_notes",
        "partner_desired_jobs",
        "partner_af_case",
        "hr_360_view", 
        "test_data_demo_sv",
        # ~ "edi_af_appointment",
        "calendar_af",
        "help_online",
        "af_security",
        "contact_links",
            ],
    "application": False,
    "installable": True,
}

