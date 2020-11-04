from odoo import fields, models, api

class documentation (models.Model):
    _name = 'documentation'
    _description = 'Documentos'
    _rec_name = 'document_name'

    document_name = fields.Char('Nombre del documento')
    validity_unit = fields.Integer(default=1, string="Vigencia (unidad)")
    validity_period = fields.Selection([('months', 'Meses'), ('years', 'Años')], string='Vigencia (periodo)',default='years')









