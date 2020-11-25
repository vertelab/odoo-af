# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Depreciated Af Install all modules",
    "version": "12.0.1.4",
    "author": "Vertel AB",
    "description": """
        Depreciated: \n
		Replaced by: \n
		af_install_modules_bm_1-0\n
		af_install_modules_crm_1-0\n
		af_install_modules_dafa_mvp1\n
		af_install_modules_dafa_mvp2 \n
		\n
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
        "base", 
            ],

    "application": False,
    "installable": True,
}

