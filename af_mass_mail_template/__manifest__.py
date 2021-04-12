{
    "name": "Moved to odoo-mail AF Mass Mailing Template",
    "summary": "AF Mass Mailing Template Design",
    "version": "12.0.0.1",
    "category": "Email Marketing",
	"description": """
	 v12.0.0.1 AFC-86  Add Mass mailing template for AF newsletters.\n
	 check if this module is worth having. mail_tracking_mass_mailing\n
	 check if this module is worth having. mass_mailing_custom_unsubscribe\n
	 check if this module is worth having. mass_mailing_resend \n
	 check if this module is worth having. partner_email_check \n
	 check if this module is worth having. test_mass_mailing \n
    """,
    "license": "AGPL-3",
    "author": "Vertel AB",
    "depends": [
        "mass_mailing"
    ],
    'data': [
        "data/mail_template.xml",
    ],
    'installable': True,
}
