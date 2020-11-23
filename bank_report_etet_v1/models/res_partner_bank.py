from odoo import fields, models, api


class res_partner_bank(models.Model):
    _inherit = 'res.partner.bank'
    _description = 'Tipos de cuenta'

    account_type = fields.Selection(string="Tipo de Cuenta", selection=[('1', 'Ahorros'), ('2', 'Corriente')])
