{
    "name": "AF Mail Client Contact",
    "summary": "AF Mail Client Contact",
    "version": "12.0.0.1",
    "category": "Messaging",
	"description": """
	 v12.0.0.1 AFC-1313 Mail Client Odoo Messaging.
    """,
    "license": "AGPL-3",
    "author": "Vertel AB",
    "depends": [
        "mail", "contacts"
    ],
    'data': [
        "views/contact_mail_view.xml",
    ],
    'installable': True,
}
