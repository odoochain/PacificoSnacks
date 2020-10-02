# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportProductSupplierView(models.TransientModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.etet.productsupplier.wizard'  

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today) 


    def get_report_purchase(self):
        self.ensure_one()
        report_type = 'qweb-pdf'
        data = self._prepare_report_data()
        report_name = "purchase_report_etet.products_supplier_report"
        return (
            self.env["ir.actions.report"]
            .search(
                [("report_name", "=", report_name), ("report_type", "=", report_type)],
                limit=1,
            )
            .report_action(self, data=data)
        )


    def _prepare_report_data(self):
        self.ensure_one()
        active_ids = self.env.context.get("active_ids", [])
        return {
            "wizard_id": self.id,
            "ids": active_ids,
            "model": "hr.contribution.register",
            "form": self.read(),
            "date_start": self.date_start,
            "date_end": self.date_end,            
        }


    # @api.model
    # def _get_report(self, docids, data=None):
    #     date_start = data['form']['date_start']
    #     date_end = data['form']['date_end']

    #     SO = self.env['purchase.order.line']
    #     start_date = datetime.strptime(date_start, DATE_FORMAT)
    #     end_date = datetime.strptime(date_end, DATE_FORMAT)
    #     delta = timedelta(days=1)

    #     docs = []
    #     while start_date <= end_date:
    #         date = start_date
    #         start_date += delta

    #         print(date, start_date)
    #         orders = SO.search([
    #             ('date_order', '>=', date.strftime(DATETIME_FORMAT)),
    #             ('date_order', '<', start_date.strftime(DATETIME_FORMAT)),
    #             ('state', 'in', ['sale', 'done'])
    #         ])

    #         total_orders = len(orders)
    #         amount_total = sum(order.amount_total for order in orders)

    #     #    self._cr.execute(
    #     #        ''' SELECT p.date_order, p.order_id, p.product_id, p.partner_id, p.product.qty, p.price_unit, p.price_subtotal, p.price_total FROM purchase_order_line p order by date_order''')

    #     #    lines = self._cr.fetchall()

    #     #    return lines


    #         docs.append({
    #             'date': self.env.order.line.date_order,
    #             'order': self.env.order.line.order_id,
    #             'product': self.env.order.line.product_id,
    #             'partner': self.env.order.line.partner_id,
    #             'qty': self.env.order.line.product.qty,
    #             'pricesunit': self.env.order.line.price_unit,
    #             'pricesubtotal': self.env.order.line.price_subtotal,
    #             'pricestotal': self.env.order.line.price_total

    #         })

    #     return {
    #         'doc_ids': data['ids'],
    #         'doc_model': data['model'],
    #         'date_start': date_start,
    #         'date_end': date_end,
    #         'docs': docs,
    #     }