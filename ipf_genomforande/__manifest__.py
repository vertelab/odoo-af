# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "IPF Genomforande For System",
    "summary": "AF to IPF Genomforande For System integration",
    "version": "12.0.2.0.0",
    "author": "Arbetsförmedlingen",
    "license": "AGPL-3",
    'description': """
Module for showing a jobseeker's cases \n
Jira \n
================================================================================================ \n
This module adds new functionality regarding appointments functionality \n
V12.0.1.0.0 AFC-2019: Visa ärenden från BÄR i CRM \n
V12.0.1.0.1 AFC-2385: Added new column for Program/Insats \n
V12.0.1.0.2 AFC-2448: Added Cases from genomforanden API \n
V12.0.1.0.3 AFC-2743 & AFC-2748: Commented out functionality for Case and adjusted to only show Genomforande \n
V12.0.2.0.0 AFC-3127: Now uses arbetssokande instead of res_partner \n
""",
    "website": "https://arbetsformedlingen.se/",
    "category": "Tools",
    "depends": ["arbetssokande",
                "af_ipf", ],
    "external_dependencies": [],
    "data": [
        "views/genomforande_views.xml",
        "data/genomforande_data.xml",
    ],
    "application": True,
    "installable": True,
}
