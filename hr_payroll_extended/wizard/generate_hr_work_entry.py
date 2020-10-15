# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


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

    def generate_work_entry(self):
        contract_ids = self.env['hr.contract'].search([('state', '=', 'open')])
        type_ids = self.env['hr.work.entry.type'].search([('code', '=', 'WORK100')], limit=1)
        for contract_id in contract_ids:
            work_obj = self.env['hr.work.entry']
            work_id = work_obj.create({
                'employee_id': contract_id.employee_id.id,
                'work_entry_type_id': type_ids.id,
                'state': 'draft',
                'company_id': self.company_id.id,
                'date_start': self.date_start,
                'date_stop': self.date_stop,
                'active': True,
                'name': contract_id.employee_id.name + ' ' + str(self.date_start) + ' - ' + str(self.date_stop)
            })
        return {'type': 'ir.actions.act_window_close'}