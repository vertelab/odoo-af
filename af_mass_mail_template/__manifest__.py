{
    "name": "Replaced - AF Mass Mailing Template",
    "summary": "AF Mass Mailing Template Design",
    "version": "12.0.1.1.0",
    "category": "Email Marketing",
	"description": """
	 v12.0.0.1 AFC-86  Add Mass mailing template for AF newsletters.\
	 Replace by: odoo-mail/mail_mass_mail_template_af
    """,
    "license": "AGPL-3",
    "author": "Vertel AB",
    "depends": [
        "mass_mailing"
    ],
    'data': [
        "data/mail_template.xml",
    ],
    'installable': False,
}
