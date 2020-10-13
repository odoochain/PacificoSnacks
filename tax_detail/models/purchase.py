# -*- coding: utf-8 -*-
# Keware.co / See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.misc import formatLang, format_date, get_lang


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    amount_by_group = fields.Binary(string="Tax amount by group",
                                    compute='_compute_taxes_by_group')  # compute='_compute_taxes_by_group')

    @api.depends('order_line', 'partner_id', 'currency_id')
    def _compute_taxes_by_group(self):
        '''
        Metodo que responde al computado del campo, este metodo llama dos metodos mas, se encarga de llevar el 
        flujo y llena el campo
        @author: Jvaldesb - Varuna
        '''

        for order in self:
            lang_env = order.with_context(lang=order.partner_id.lang).env
            taxes = self.prepare_taxes(order)
            unified_taxes = self.filter_taxes(taxes[0], list(set(taxes[1])))
            order.amount_by_group = [(tax['tax_group_id'].name, tax['amount'], order.amount_untaxed,
                                      formatLang(lang_env, tax['amount'], currency_obj=order.currency_id),
                                      formatLang(lang_env, order.amount_untaxed, currency_obj=order.currency_id),
                                      len(unified_taxes), tax['tax_group_id'].id) for tax in unified_taxes]

    def prepare_taxes(self, order):
        '''
        Metodo que prepara los impuestos para la clasificacion de los mismos en el detalle
        @author: Jvaldesb - Varuna
        @return: object list con dos eleementos  object list
        '''
        taxes_totals = []
        tax_list = []
        for line in order.order_line:
            if line.taxes_id:
                for tax in line.taxes_id:
                    taxes = tax.compute_all(line.price_unit, line.currency_id, line.product_qty,
                                            line.product_id, line.partner_id)

                    tax_detail = {"tax_group_id": tax.tax_group_id,
                                  "amount": sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))}
                    taxes_totals.append(tax_detail)
                    tax_list.append(tax.tax_group_id)

        return [taxes_totals, tax_list]

    def filter_taxes(self, taxes, taxes_list):
        '''
        Metodo que clasifica y retorna los impuestos totales y para renderizar
        @author: Jvaldesb - Varuna
        @return: object list con una lista de diccionarios con el impuesto segun el grupo y el total
        '''
        unified_taxes = []
        for tax in taxes_list:
            amount = 0
            for t in taxes:
                if tax == t['tax_group_id']:
                    amount += t['amount']

            unified_taxes.append({"tax_group_id": tax, "amount": amount})
        return unified_taxes
