# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "IPF AIS BOS",
    "summary": "AF to IPF AIS BOS Regelverk",
    "version": "12.0.0.0.1",
    "author": "Arbetsförmedlingen",
    "license": "AGPL-3",
    'description': """
Module for BOS KROM
================================================================================================
Jiras from EDI platform \n
v12.0.2.0.0 AFC-1950 - Implemented new version of API \n
v12.0.2.0.1 AFC-1950 - Replaced match_area and updated index file \n
v12.0.2.0.2 AFC-2415 - Added a cron job \n
Jiras from IPF platform \n
v12.0.2.0.0 AFC-2440 - Implemented new version of API \n
v12.0.2.0.1 AFC-2489 - Placed field under label for better reading \n
""",
    "website": "https://arbetsformedlingen.se/",
    "category": "Tools",
    "depends": ["partner_view_360",
                "af_ipf", ],
    "external_dependencies": [],
    "data": [
        "views/partner_views.xml",
        "data/ipf_data.xml",
    ],
    "application": True,
    "installable": True,
}
