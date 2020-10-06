

from odoo import fields, models, api


class Partner(models.Model):
    _inherit = 'res.partner'
    _description = 'Asociacion de consecutivos por cliente'
    seq_container = fields.Many2one('ir.sequence', string='Secuencias para contenedores')


