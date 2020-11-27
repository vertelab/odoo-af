{
    'name': 'HR 360 View',
    'summary': """
        A dashboard for employees to search for job seekers.
        """,
    'version': '12.0.0.8',
    'category': 'Human resources',
    'description': """
Jiras
===============================================================================
v12.0.0.7 - The "Breadcrumb" does not lead back to the start\n
v12.0.0.6 AFC-1247 - change from Handläggaryta to Jobbsekers in Breadcrumbs\n
v12.0.0.5 AFC-1197 - Anslut mot API:et för att fråga med personnummer och få tillbaka ett kundnr. Byt så att "Sökning vid Myndighetens behov" använder "Mitt kontos Kundnr" istället för "SökandID" 
v12.0.0.4 AFC-0715 - Lade till beroende på Firstname Extension som döljer förnamn-efternamn-fälten i visningsläge. \n
v12.0.0.3 AFC-0715 - Lagt till rubrik på vyn för Arbetsyta.\n
v12.0.0.2 AFC-0713 - Bytt namn från Handläggaryta till Arbetsyta enligt beslut från Införandegruppen. Dolt menyn HR 360.\n
v12.0.0.1 AFC-0667 - HR 360 View Module. Lägger till huvudsida för handläggare med sökyta samt flikar med uppgifter centrerade från handläggaren. \n
v12.0.1.1 AFC-0185, 199 \n

""",
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': [
        'hr',
        'partner_view_360',
        # 'partner_af_case',
        # 'partner_daily_notes', removed dependency
        'hr_employee_firstname_extension',
        'af_ipf',
    ],
    'data': [
        # 'views/menu.xml',
        'views/hr_view.xml',
        'wizard/hr_employee_search_wizard.xml'
    ],
    'installable': True,
}
