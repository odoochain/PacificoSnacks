from odoo import fields, models, api

class res_bank(models.Model):
    _inherit = 'res.bank'
    _description = 'Codigos de bancos'

    code_bank = fields.Char(string="Codigo de banco")







