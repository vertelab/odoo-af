{
    "name": "AF Mail Client Employee",
    "summary": "AF Mail Client Employee",
    "version": "12.0.0.1",
    "category": "Messaging",
	"description": """
	 v12.0.0.1 AFC-1313 Mail Client Odoo Employee.
    """,
    "license": "AGPL-3",
    "author": "Vertel AB",
    "depends": [
        "mail", "hr"
    ],
    'data': [
        "views/hr_mail_view.xml",
    ],
    'installable': True,
}
