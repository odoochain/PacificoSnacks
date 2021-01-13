# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare
from odoo.tools.misc import formatLang
from dateutil.relativedelta import relativedelta


class AccountMove(models.Model):
    _name = 'account.move_fiscal'

    ref_fiscal = fields.Char(string='Referencia')
    date_fiscal = fields.Date(string='Fecha de Depreciacion')
    asset_remaining_value_fiscal = fields.Float(string='Valor Depreciable')
    asset_depreciated_value_fiscal = fields.Float(string='Amortizacion Acumulada')
    asset_id = fields.Many2one('account.asset')
    amount_total = fields.Float(string='Amortizacion')


