# -*- coding: utf-8 -*-


from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError, ValidationError

class HrContract(models.Model):
    _inherit = 'hr.contract'


    risk_id = fields.Many2one('hr.risk', string='Risk')
    state = fields.Selection([
        ('draft', 'New'),
        ('open', 'Activo'),
        ('close', 'Liquidado'),
    ], string='Status', group_expand='_expand_states', copy=False,
       tracking=True, help='Status of the contract', default='draft')
    entity_ids = fields.One2many('hr.company.ss', 'contract_id', string='Entidad')