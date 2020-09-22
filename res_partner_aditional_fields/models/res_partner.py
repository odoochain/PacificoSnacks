

from odoo import fields, models, api


class Partner(models.Model):
    _inherit = 'res.partner'
    _description = 'definicion de campos adicionales para contactos'
    to_print = fields.Char('Datos contacto', compute='_to_print')
    to_days = fields.Integer('Dias en transito')

    day_upload_week = fields.Selection(string='Dia de cargue cliente', selection=[('0', 'domingo'), ('1', 'lunes'),
                                                                          ('2', 'martes'), ('3', 'miercoles'),
                                                                          ('4', 'jueves'), ('5', 'viernes'),
                                                                          ('6', 'sabado')])

