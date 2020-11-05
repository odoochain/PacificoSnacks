from odoo import fields, models, api
from odoo.exceptions import ValidationError

class documentation (models.Model):
    _name = 'documentation'
    _description = 'Documentos'
    _rec_name = 'document_name'

    document_name = fields.Char('Nombre del documento')
    validity_unit = fields.Integer(default=1, string="Vigencia (unidad)")
    validity_period = fields.Selection([('months', 'Meses'), ('years', 'Años')], string='Vigencia (periodo)',default='years')

    @api.constrains('validity_unit')
    def _validity_unit(self):
        if self.validity_unit > 500:
            raise ValidationError('La unidad de vigencia no puede ser mayor a 500!')
        if self.validity_unit == 0:
            raise ValidationError('La unidad de vigencia no puede ser igual a 0!')









