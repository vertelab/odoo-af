{
    'name': 'HR 360 View',
    'summary': """
        A dashboard for employees to search for job seekers.
        """,
    'version': '12.0.2.1.1',
    'category': 'Human resources',
    'description': """
Jiras
===============================================================================
v12.0.0.8.0 AFC-2204 - Renamed variable in po file \n
v12.0.0.7.0          - The "Breadcrumb" does not lead back to the start\n
v12.0.0.6.0 AFC-1247 - change from Handläggaryta to Jobbsekers in Breadcrumbs\n
v12.0.0.5.0 AFC-1197 - Anslut mot API:et för att fråga med personnummer och få tillbaka ett kundnr. Byt så att "Sökning vid Myndighetens behov" använder "Mitt kontos Kundnr" istället för "SökandID" 
v12.0.0.4.0 AFC-0715 - Lade till beroende på Firstname Extension som döljer förnamn-efternamn-fälten i visningsläge. \n
v12.0.0.3.0 AFC-0715 - Lagt till rubrik på vyn för Arbetsyta.\n
v12.0.0.2.0 AFC-0713 - Bytt namn från Handläggaryta till Arbetsyta enligt beslut från Införandegruppen. Dolt menyn HR 360.\n
v12.0.0.1.0 AFC-0667 - HR 360 View Module. Lägger till huvudsida för handläggare med sökyta samt flikar med uppgifter centrerade från handläggaren. \n
v12.0.1.1.0 AFC-0185 - 199 \n
v12.0.1.2.0 AFC-1859 - AFC-1861, AFC-1870 - Added more logic for verification of other_reason field and fixed layout of form. \n
v12.0.1.3.0 AFC-1988 - Better handling of bankid approvals. \n
v12.0.1.4.0 AFC-2097 - misc bugfixes. \n
v12.0.2.0.0 AFC-2260 - Changed error messages. Tried to fix log and version numbers. \n
v12.0.2.1.0 AFC-2230 - Changed txt when a person is not in the database and deleted screen pop-up. \n
v12.0.2.1.1 AFC-2388 - Changed position of search buttons. \n

""",
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': [
        'hr',
        'partner_view_360',
        'hr_employee_firstname_extension',
        'af_ipf',
    ],
    'data': [
        'views/hr_view.xml',
        'wizard/hr_employee_search_wizard.xml'
    ],
    'installable': True,
    'application': False,
}
