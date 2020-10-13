# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning, ValidationError
import time
from datetime import datetime, timedelta
import xlwt
import base64
# from cStringIO import StringIO
from io import StringIO
from io import BytesIO
import xlsxwriter
import types
import logging
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

_logger = logging.getLogger(__name__)

class ReportProductSupplier(models.AbstractModel):

    _name = "report.purchase_report_etet.products_supplier_report"
    _description = "Product Supplier Report"


    # def _get_report_values(self, docids, data):
    #     wizard_id = data["wizard_id"]
    #     date_start = data["date_start"]
    #     date_end = data["date_end"]
    #     print ('uuuuuuuu')
    #     report_type = 'qweb-pdf'
    #     report_name = "purchase_report_etet.products_supplier_report"
    #     return {
    #         'doc_ids': docids,
    #         'doc_model': 'report.etet.productsupplier.wizard',
    #         'docs': self.env['report.etet.productsupplier.wizard'].browse(docids),
    #         'report_type': report_type if data else '',
    #     }



    @api.model
    def _get_report_values(self, docids, data=None):
        # if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
        #     raise UserError(_("Form content is missing, this report cannot be printed."))
        print ('ddddddd')
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        return {
            'doc_ids': self.ids,
            'doc_model': self.env['report.etet.productsupplier.wizard'],
            'data': data,
            'docs': self.env['report.etet.productsupplier.wizard'].browse(docids),
            'time': time,
        }        