# -*- coding: utf-8 -*-
{
    'name': "Suivi des dossiers d'immigration",
    'summary': "",
    'description': """  """
                   """ . """,

    'author': "HyD Freelance",
    'website': "http://",
    'category': u'Other',
    'version': '15.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['project', 'task_check_list'],

    # always loaded
    'data': [
            # data
            # views
            # "views/templates.xml",
            "views/project_task_type_views.xml",
            "views/project_task_views.xml",
            "views/project_views.xml",
            # "views/external_layout_hygiene.xml",
            # "views/res_company_views.xml",
            # "views/report_saledetails_views.xml",
            # wizards
            "wizards/add_expense_task_views.xml",
            # workflow
            # security
            "security/ir.model.access.csv",
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
