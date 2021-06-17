
This module maintained here:
         https://github.com/vertelab/odoo-af/tree/Dev-12.0-Fenix-Sprint-02/af_install_modules_dafa_mvp1

Versions
========

This module installs all Dafa MVP1-modules at one go.

Please see the depend-tab (with debug-mode) for a list of which modules are installed.

1.    v12.0.1.1  - First release
2.    v12.0.1.2  - Updates in the list
3.    v12.0.1.3  - Added Auth_user_rights_wizard and CIAM-modules, corrected spelling of auth_timeout
4.    v12.0.1.4  - Removed items outside of MVP1
5.    v12.0.1.5  - Added more modules
6.    v12.0.1.6  - Removed auth_login
7.    v12.0.1.7  - Added my customer_tab and hr_holidays
8.    v12.0.1.8  - Disableded Matomo due to bug. Disabled hr_org_chart since Emma did not want it.
9.    Once the module is installed, please de-install it to avoid depencency-problems.
10.   v12.0.1.0.9  - Added new version-numbers-standard. Added hr_af_holidays.
11.   v12.0.1.0.10  - Added list of Repos that needs to be installed.
12.   v12.0.1.0.11  - AFC-1666 added partner_flip_firstname.
13.   v12.0.1.1.1  - Consolidation of MVP1 and MVP2 into DAFA 1.0
14.   v12.0.1.1.2  - test of version bump
15.   v12.0.1.1.3  - Moved manifest description to rst file to avoid module description conflicts

# Vertel Repositories
=====================

1. "odoo-account||https://github.com/vertelab/odoo-account.git"
2. "odoo-af||https://github.com/vertelab/odoo-af.git"
3. "odoo-api||https://github.com/vertelab/odoo-api.git"
4. "odoo-auth||https://github.com/vertelab/odoo-auth.git" # New branch Dev-12.0-Fenix-Sprint-02 based on Dev-12.0
5. "odoo-base||https://github.com/vertelab/odoo-base.git"
6. #"odoo-contract|master|https://github.com/vertelab/odoo-contract.git"
7. "odoo-edi||https://github.com/vertelab/odoo-edi.git" # New branch Dev-12.0-Fenix-Sprint-02 based on Dev-12.0
8. "odoo-hr||https://github.com/vertelab/odoo-hr.git"
9. "odoo-l10n_se|12.0|https://github.com/vertelab/odoo-l10n_se.git" # Need to explicitly say 12.0 else it will use the default branch Dev-12.0-Fenix-Sprint-02. We want 12.0 for the moment
10. "odoo-mail||https://github.com/vertelab/odoo-mail.git"
11. "odoo-outplacement||https://github.com/vertelab/odoo-outplacement.git"
12. "odoo-project||https://github.com/vertelab/odoo-project.git"
13. "odoo-sale||https://github.com/vertelab/odoo-sale.git"
14. "odoo-server-tools||https://github.com/vertelab/odoo-server-tools.git" # New branch Dev-12.0-Fenix-Sprint-02 based on Dev-12.0
15. "odoo-user-mail||https://github.com/vertelab/odoo-user-mail.git"
16. "odoo-web||https://github.com/vertelab/odoo-web.git" # New branch Dev-12.0-Fenix-Sprint-02 based on Dev-12.0
17. #"odoo-website||https://github.com/vertelab/odoo-website.git"

# Use Vertel versions of OCA modules
====================================
1. "odooext-oca-web||https://github.com/vertelab/web.git"
2. "odooext-oca-server-auth||https://github.com/vertelab/server-auth.git" # New branch Dev-12.0-Fenix-Sprint-02 based on Dev-12.0

# OCA
=====

1. "odooext-oca-contract||https://github.com/OCA/contract.git"
2. "odooext-oca-hr||https://github.com/OCA/hr.git"
3. "odooext-oca-mis-builder||https://github.com/OCA/mis-builder.git"
4. "odooext-oca-partner-contact||https://github.com/OCA/partner-contact.git"
5. "odooext-oca-reporting-engine||https://github.com/OCA/reporting-engine.git"
6. "odooext-oca-server-ux||https://github.com/OCA/server-ux.git"
7. "odooext-oca-social||https://github.com/OCA/social.git"
8. "odooext-oca-timesheet||https://github.com/OCA/timesheet.git"