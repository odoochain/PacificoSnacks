from odoo import fields, models, api

class Required_documentation (models.Model):
    _name = 'required_documentation'
    _description = 'Documentacion requeridad'

    category_id = fields.Many2one('res.partner.category', column1='partner_id',column2='category_id', string='Categoria')
    documentation_id = fields.Many2many('documentation', string='Documentos')
    _sql_constraints = [
        ('category_id_uniq', 'unique(category_id)', "Ya existe esta categoria!"),
    ]










