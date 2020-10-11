# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "AF IPF Integration",
    "version": "12.0.1.0.0",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "summary": "Module for synchronous integrations to IPF",
	"description": """
Description
================================================================================================
Asök booking management \n
12.0.1.0.0 - AFC-1197 - Lägg till Helger och röda dagar i Resource Leaves.\n
\n
    """,
    "depends": ["af_security"],
    "external_dependencies": {'python': ['requests']},
    "data": [
        "views/ipf_views.xml",
        "data/customer_data.xml",
    ],
    "application": True,
    "installable": True,
}