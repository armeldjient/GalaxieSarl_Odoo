# -*- coding: utf-8 -*-
{
    'name': "Projet PL services",

    'summary': "Personnalisation Odoo pour le projet pl servicess",

    'description': """  """
                   """ . """,

    'author': "HyD Freelance",
    'website': "http://",
    'category': u'Other',
    'version': '16.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
            # data
            # views
            # "views/templates.xml",
            # "views/external_layout_hygiene.xml",
            # "views/res_company_views.xml",
            # "views/report_saledetails_views.xml",
            "views/inherit_web_login.xml",
            # workflow
            # security
            # "security/ir.model.access.csv",
            # reports
            # "reports/report_paper.xml",
            # "reports/account_move_reports.xml",
            # "reports/facture_a5_report.xml",
    ],

    # only loaded in demonstration mode
    'demo': [],
    'installable': True,
    'images': ['static/images/main_screenshot.png'],
    'assets': {
        # 'point_of_sale.assets': [
        #     'hyd_hygiene/static/src/xml/**/*',
        #     'hyd_hygiene/static/src/js/*',
        # ],
    },
}
