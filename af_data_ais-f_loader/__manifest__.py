# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "AIS-F Data Loader",
    "version": "12.0.1.3",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        "hr",
        "calendar",
        # "partner_view_360",
        "partner_kpi_data",
        "partner_daily_notes",
        # "partner_desired_jobs",
    ],
    "data": [
        # "data/res.country.state.csv",
        "data/res_partner.xml",
    ],
    "application": False,
    "installable": True,
}
