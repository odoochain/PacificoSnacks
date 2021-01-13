# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare
from odoo.tools.misc import formatLang
from dateutil.relativedelta import relativedelta


class AccountlocationAsset(models.Model):
    _name = 'account.location_asset'

    location_asset_id = fields.Many2one('account.asset', string='Tipo de activo')

    codigo = fields.Char(string='codigo')
    nombre = fields.Char(string='nombre')
    pais = fields.Many2one('res.country', string='pais')
    ciudad = fields.Many2one('res.city', string='ciudad')
    direccion = fields.Char(string='direccion')








