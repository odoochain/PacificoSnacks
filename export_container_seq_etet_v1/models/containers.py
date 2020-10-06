from odoo import fields, models, api

class Containers (models.Model):
    _name = 'containers'
    _description = 'Modulo de contenedores'

    customers = fields.Many2one('res.partner', string='Cliente')
    code_containers = fields.Char('Codigo del contenedor')

    @api.onchange('customers')
    def _code_containers(self):
        self.code_containers = self.env["ir.sequence"].next_by_code(self.customers.seq_container.code)







