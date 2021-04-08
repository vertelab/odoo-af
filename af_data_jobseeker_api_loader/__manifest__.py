# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "AIS-F Jobseeker Loader",
    "version": "12.0.1.1",
    "description": """

AIS-F Jobseeker Loader
==========================================
calls api to load all jobseekers according to file of customer ids
""",

    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [ 
		"edi_af_aisf_rask_get_jobseeker", 
    ],
    "data": [
        "views/res_partner.xml",
    ],
    "application": False,
    "installable": True,
}
