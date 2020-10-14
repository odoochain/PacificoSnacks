# -*- coding: utf-8 -*-
# Keware.co - Julián Valdés - Info@keware.co / See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from collections import defaultdict

MAP_INVOICE_TYPE_PARTNER_TYPE = {
    'out_invoice': 'customer',
    'out_refund': 'customer',
    'out_receipt': 'customer',
    'in_invoice': 'supplier',
    'in_refund': 'supplier',
    'in_receipt': 'supplier',
}

MAP_INVOICE_TYPE_PARTNER_TYPE_SUPPLIER = ['in_invoice', 'in_refund', 'in_receipt']


class MassPayment(models.Model):
    _name = 'payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Model to make massive payments of supplier invoices.'

    name = fields.Char(string="Number", readonly=True, copy=False, default=_("Draft"))
    partner_ids = fields.Many2many(comodel_name='res.partner', string='Vendor', required=True)
    invoices_type = fields.Selection(selection=[('customer', 'Customer'), ('supplier', 'Supplier')], string='Type',
                                     required=True, store=True, readonly=True)
    invoices_ids = fields.Many2many(comodel_name='account.move', string='Invoices')
    invoices_customer_ids = fields.Many2many(comodel_name='account.move', relation='invoices_customer_rel',
                                             string='Invoices',
                                             domain=[('type', 'in', ['out_invoice', 'out_refund', 'out_receipt']),
                                                     ('state', '=', 'posted'),
                                                     ('invoice_payment_state', '!=', 'paid')], store=True)
    invoices_supplier_ids = fields.Many2many(comodel_name='account.move', relation='invoices_supplier_rel',
                                             string='Invoices',
                                             domain=[('type', 'in', ['in_invoice', 'in_refund', 'in_receipt']),
                                                     ('state', '=', 'posted'),
                                                     ('invoice_payment_state', '!=', 'paid')], store=True)
    journal = fields.Many2one(comodel_name='account.journal', string='Journal',
                              domain=[('type', 'in', ('bank', 'cash'))])
    amount_total = fields.Float(string='Total Amount', compute='_compute_total_amount')
    payment_date = fields.Date(string='Payment Date')
    payment_method_id = fields.Many2one(comodel_name='account.payment.method', string='Payment Method Type')
    group_payment = fields.Boolean(default=False)
    payments_ids = fields.Many2many(comodel_name='account.payment', string='Payments', store=True)
    state = fields.Selection(selection=[('not_paid', 'Not Paid'), ('paid', 'Paid')], string="State", default='not_paid')

    def _compute_invoice_type_customer(self):
        self.invoices_type = 'customer'
        return {
            'name': _('Payment Customer'),
            'domain': [('invoices_type', '=', 'customer')],
            'res_model': 'payment',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'context': {'default_invoices_type': 'customer'}
        }

    def _compute_invoice_type_supplier(self):
        self.invoices_type = 'supplier'
        return {
            'name': _('Payment Vendors'),
            'domain': [('invoices_type', '=', 'supplier')],
            'res_model': 'payment',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'context': {'default_invoices_type': 'supplier'}
        }

    @api.onchange('invoices_customer_ids', 'invoices_supplier_ids')
    def _compute_invoices_ids(self):
        if self.invoices_type == 'customer':
            self.invoices_ids = [inv.id for inv in self.invoices_customer_ids]
        if self.invoices_type == 'supplier':
            self.invoices_ids = [inv.id for inv in self.invoices_supplier_ids]

    @api.depends("invoices_ids")
    def _compute_total_amount(self):
        """
        Calcule el total de todas las facturas.
        """
        total = 0
        for inv in self.invoices_ids:
            total = total + inv.amount_total
        self.amount_total = total

    @api.onchange("invoices_ids")
    def _change_invoices(self):
        """
        Asigna los proveedores dependiendo de las facturas seleccionadas.
        """
        partner_ids = []
        for inv in self.invoices_ids:
            partner_ids.append(inv.partner_id.id)
        self.partner_ids = partner_ids

    def invoice_payment(self):
        """
        Asigna el nombre del pago y cambia el estado pagado de las facturas.
        Crea pagos según las facturas.
        @author: Jvaldesb - Varuna
        @return: action_vals
        """

        seq_code = "seq.mass_payment.customers" if self.invoices_type == "customer" else "seq.mass_payment.vendors"
        self.name = self.env["ir.sequence"].next_by_code(seq_code)

        payment = self.env['account.payment']
        payments = payment.create(self.get_payments_vals())
        payments.post()

        self.payments_ids = [pay.id for pay in payments]
        self.state = "paid"
        action_vals = {
            'name': _('Payments'),
            'domain': [('id', 'in', payments.ids), ('state', '=', 'posted')],
            'res_model': 'account.payment',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }
        if len(payments) == 1:
            action_vals.update({'res_id': payments[0].id, 'view_mode': 'form'})
        else:
            action_vals['view_mode'] = 'tree,form'
        return action_vals

    def get_payments_vals(self):
        '''
        Calcule los valores de los pagos.
        @return: una lista de valores de pago (diccionario).
        '''
        grouped = defaultdict(lambda: self.env["account.move"])
        for inv in self.invoices_ids:
            if self.group_payment:
                grouped[(inv.commercial_partner_id, inv.currency_id, inv.invoice_partner_bank_id,
                         MAP_INVOICE_TYPE_PARTNER_TYPE[inv.type])] += inv
            else:
                grouped[inv.id] += inv
        return [self._prepare_payment_vals(invoices) for invoices in grouped.values()]

    def _prepare_payment_vals(self, invoices):
        '''
        Cree los valores de pago.
        @param invoices:  Las facturas / facturas a pagar.
        @return: Los valores de pago como diccionario.
        '''
        amount = self.env['account.payment']._compute_payment_amount(invoices, invoices[0].currency_id,
                                                                     self.journal, self.payment_date)
        values = {
            'journal_id': self.journal.id,
            'payment_method_id': self.payment_method_id.id,
            'payment_date': self.payment_date,
            'communication': " ".join(i.invoice_payment_ref or i.ref or i.name for i in invoices),
            'invoice_ids': [(6, 0, invoices.ids)],
            'payment_type': ('inbound' if amount > 0 else 'outbound'),
            'amount': abs(amount),
            'currency_id': invoices[0].currency_id.id,
            'partner_id': invoices[0].commercial_partner_id.id,
            'partner_type': MAP_INVOICE_TYPE_PARTNER_TYPE[invoices[0].type],
            'partner_bank_account_id': invoices[0].invoice_partner_bank_id.id,
        }
        return values
