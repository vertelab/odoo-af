# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Test Data AF",
    "version": "12.0.1.0.1",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        "contacts", 
        "hr", 
        "calendar", 
        "partner_employee360", 
        "partner_kpi_data", 
        "res_drivers_license", 
		"res_sni", 
		"res_ssyk", 
		"res_sun", 
		"partner_daily_notes", 
		"partner_desired_jobs",
        "partner_fax",
        ],
    
    "data": [
        #"data/res.partner.csv", --> Daniels fil
        #"data/af_office/res.partner.csv", --> Funkar
		#"data/organisationer/res.partner.csv", --> Funkar
		#"data/arbetsg/res.partner.csv", --> Funkar inte
		#"data/arbetsg_2adr/res.partner.csv", --> Funkar inte
		#"data/arbetsg_utl_adr/res.partner.csv", --> mapp finns inte
		#"data/arbetsg_cct/res.partner.csv", --> Funkar inte
		#"data/user_cct/res.partern.csv", --> Funkar
		#"data/arbetsg/res.partner.kpi.csv",
		#"data/arbetsg_sni1/res_sni.csv",
		#"data/arbetsg_sni2/res_sni.csv",
		#"data/arbetsg/desired_jobs.csv",
		#"data/arbetsg/daily_notes.csv",
		#"data/arbetsg_lst_cnt/daily_notes.csv",
		#"data/arbetsg_hr_imp1/hr_employee.csv",
		#"data/arbetsg/res_users.csv",
		#"data/arbetsg_hr_imp2/hr_employee.csv",
    ],
    "application": False,
    "installable": True,
}
