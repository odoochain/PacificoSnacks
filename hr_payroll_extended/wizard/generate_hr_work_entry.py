# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import date
from datetime import datetime

class GenerateHRWorkEntry(models.TransientModel):
    _name = "generate.hr.work.entry"

    date_start = fields.Date(
        string='Fecha de inicio'
    )
    date_stop = fields.Date(
        string='Fecha final'
    )
    company_id = fields.Many2one('res.company', string='Company', readonly=True, required=True,
                                 default=lambda self: self.env.company)

    employee_id = fields.Many2one('hr.employee', string='Empleado')

    modo = fields.Selection(string="Modo", selection=[('1', 'Por Empleado'), ('2', 'General')], default='1', required=True)

    def generate_work_entry(self):
        if self.modo == '1':
            contract_ids = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)])
        elif self.modo == '2':
            contract_ids = self.env['hr.contract'].search([('state', '=', 'open')])
        time_start = datetime.min.time()
        date_start = datetime.combine(self.date_start, time_start)
        time_stop = datetime.max.time()
        date_stop = datetime.combine(self.date_stop, time_stop)
        vals_list = []
        for contract_id in contract_ids:
            vals_list += contract_id._get_work_entries_values(date_start, date_stop)
            self.env['hr.work.entry'].create(vals_list)
        return {'type': 'ir.actions.act_window_close'}