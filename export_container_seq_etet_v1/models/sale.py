from datetime import date, timedelta, datetime

from odoo import fields, models, api

class Sales(models.Model):
    _inherit = 'sale.order'
    _description = 'Asociar contenedor del cliente'

    containers = fields.Many2many('containers', string='Contenedores del cliente')





