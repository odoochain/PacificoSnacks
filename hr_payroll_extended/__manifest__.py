# -*- coding: utf-8 -*-

{
    'name': 'Payroll Extended',
    'summary': 'Description',
    'version': '1.1',
    'category': 'Human Resources',
    'website': '',
    'author': '',
    'license': '',
    'application': False,
    'installable': True,
    'depends': [
        'hr',
        'hr_payroll',
        'hr_holidays',
        'analytic',
        ],
    'description': '''

========================

''',    
    'data': [
        'views/hr_payslip_input_type_view.xml',
        'views/hr_payroll_view.xml',
        'views/hr_type_payslip_view.xml',
        'views/hr_payslip_run_view.xml',
        'views/hr_rule_parameter_view.xml',
        'views/hr_leave_view.xml',
        # 'views/hr_payroll_structure_view.xml',
        # 'views/hr_contract_view.xml',
        # 'views/report_contributionregistercust.xml',
        'views/account_analytic_account_view.xml',
        # 'wizard/hr_payroll_contribution_register_report_views.xml',
        'data/data.xml',
        # 'report/report.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': [
    ]
}
