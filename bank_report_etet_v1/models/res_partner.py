from odoo import fields, models, api


class Partner(models.Model):
    _inherit = 'res.partner'
    _description = 'Description'

    transaction_type = fields.Selection(string="tipo de transaccion", selection=[('25', 'Pago en Efectivo'), ('27', 'Abono a Cuenta Corriente'),
                                                   ('36', 'Pago Cheque Gerencia'),
                                                   ('37', 'Abono a Cuenta de Ahorros'),
                                                   ('40', 'Efectivo Seguro (visa pagos o tarjeta prepago)')])