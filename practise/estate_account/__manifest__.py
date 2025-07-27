{
    "name": "Estate Account",
    "version": '1.0',
    "category": "Extra Tools",
    "license": "AGPL-3",
    "summary": "Estate Account",
    'description': """
       Base Estate Account
    """,
    "author": "Manoj Parmar",
    "maintainers": ["Manoj Parmar"],
    "website": "www.abc.com",
    "depends": ['base', 'estate', 'account'],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        # "data/.xml",
        # "report/.xml",
        # "wizard/.xml",
        "views/res_company_views.xml",
    ],
    "installable": True,
    'auto_install': False,
    "application": True,
}