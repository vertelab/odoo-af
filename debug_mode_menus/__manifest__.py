# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Depreciated Debug Mode Menus",
    "version": "12.0.1.0.2",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        "mail",
        "contacts",
        "website",
    ],
    "description": """
        This module did some hiding of menues based on the debug-setting.\n
        It is replaced by the module af_core_menu_disabling\n
    """,
    
    "external_dependencies": [
    ],
    "data": [
        'views/debug_mode_menu.xml',

    ],
    "application": False,
    "installable": False,
}
