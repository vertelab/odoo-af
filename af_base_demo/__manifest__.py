# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "AF Translation of Data Demo Sv",
    "version": "12.0.1.2",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        "contacts",
        "hr",
        "calendar",
        # "project", -> No need for this demo any more
    ],

    "data": [
        "data/calendar.event.type.csv",
        "data/hr.employee.category.csv",
        "data/resource.calendar.csv",
        # "data/hr.job.csv", -> Module not found
        "data/hr.department.csv",
        "data/res.partner.csv",
        "data/hr.employee.csv",
        "data/calendar.event.csv",
        # "data/project.project.csv", -> No need for this demo any more
        # "data/project.task.csv", -> No need for this demo any more
    ],
    "application": False,
    "installable": True,
}
