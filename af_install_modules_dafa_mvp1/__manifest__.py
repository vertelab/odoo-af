# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "DAFA MVP 1.0 Install all modules ",
    "version": "12.0.1.0.11",
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
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        # These modules needs to be installed for  MVP1 functionality
        # "af_statistics",  # will be renamed to web_matomo. Disabled since there is a bug - the menu does not render every time.
        "api_ipf",  # Configuration of API:s that goes towards IPF.
        "api_ipf_tlr_client",  # adds api to be used for fetching company-details from TLR
        "auth_saml_ol_groups",
        "auth_saml_dafa",
        # "auth_saml_af", # wrong saml module for dafa project
        # "auth_session_timeout", # Adds ability to set session inactive timeout as system parameter. There is a conflict with: levavrop
        # adds functionality to assign user-credentials to coaches.
        "auth_user_rights_wizard",
        "audit_logger",
        # "auth_timeout",  # Disabled due to conflict with auth_saml_ol AFC-1547
        "hr_departments_partner",
        "hr_af_holidays",  # Adds non-working-days for Af. Should be name-changed to hr_holidays_af
        "hr_user_ciam_update",  # adds users to the CIAM-server
        "hr_employee_firstname",  # is required by hr_employee_firstname_extension
        "hr_employee_firstname_extension",  # is dependent on hr_employee_firstname
        "hr_employee_legacy_id",  # OCA
        # "hr_employee_views_fenix", # Depricated, renamed to hr_employee_views_dafa
        "hr_employee_views_dafa", # Mostly hides various fields and pages in the hr.employee form
        # "hr_employee_views_user-credentials-tab", - depreciated. Replaced by user-create-wizard.
        # "hr_af_holidays", # dependant on hr_holidays
        "hr_office",  # Adds
        # "hr_org_chart", #Disabled since Emma did not want it.
        # dependant on: partner_legacy_id, partner_firstname, api_ipf_tlr_client, hr_departments_partner
        "partner_flip_firstname",  # Flips first-name and lastname in contact-view.
        "partner_tlr_update",
        # "web_a11y_filter_view", # adds description to create and edit buttons. Disabled since there is a bug
        "web_a11y_report",  # adds a report with status of the Accessibility-status
        # adds a field used to store the TLR lev_id and the employees id in other salary-systems.
        "partner_legacy_id",
        # "web_autocomplete_off",
        "web_backend_theme_af",
        "web_dashboard_dafa",
        # Adds a ribbon with db- and version info in the left corner.
        "web_environment_ribbon",
    ],
    "application": "False",
    "installable": "True",
}
