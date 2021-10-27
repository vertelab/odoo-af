# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Af Error Reporting",
    "summary": "Arbetsförmedlingen error reporting for CRM",
    "version": "12.0.0.1.2",
    "category": "Utility",
    "description": """
    Jira
===================================================================== \n
    V12.0.0.1.0 AFC-2807: Added button for error reporting \n
    V12.0.0.1.1 AFC-2903: Added translation for module
    V12.0.0.1.2 AFC-3002: Fixed problem when user opens link  \n
    """,
    "author": "Arbetsförmedlingen",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        'base',
    ],
    "data": [
        'views/assets.xml',
    ]
}
