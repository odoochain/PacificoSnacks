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

_logger = logging.getLogger(__name__)


class StockUomReport(models.TransientModel):
    _name = 'stock.uom.report'
    _description = 'Stock Uom Report'

    stock_quant_id = fields.Char("LFC")
    data = fields.Binary("Archivo")
    data_name = fields.Char("nombre del archivo")

#    @api.multi
    def do_report(self):

        _logger.error("INICIA LA FUNCIÓN GENERAR EL REPORTE ")
        value = self.get_values()
        if not value:
            raise Warning(_('!No hay resultados para los datos seleccionados¡'))
        self.make_file(value)
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?model=stock.uom.report&field=data&id=%s&filename=%s' % (
            self.id, self.data_name),
            'target': 'new',
            'nodestroy': False,
        }

    def get_values(self):
        value = []

        self._cr.execute(''' SELECT sl.name, pt.name, sq.quantity, m.name, um.name FROM stock_quant sq inner join product_product pp on pp.id = sq.product_id inner join product_template pt on pt.id = pp.product_tmpl_id inner join uom_uom m ON m.id=pt.uom_id inner join uom_uom um ON um.id=pt.uom_po_id inner join stock_location sl on sl.id = sq.location_id order by sq.location_id''')

        lines = self._cr.fetchall()

        return lines

    def make_file(self, value):
        _logger.error("INICIA LA FUNCIÓN CONSTRUIR EL ARCHIVO ")
#        buf = StringIO()
        buf = BytesIO()
        wb = xlsxwriter.Workbook(buf)
        ws = wb.add_worksheet('Report')

        # formatos
        title_head = wb.add_format({
            'bold': 1,
            'border': 0,
            'align': 'rigth',
            'valign': 'vcenter'})
        title_head.set_font_name('Arial')
        title_head.set_font_size(10)

        subtitle_head = wb.add_format({
            'bold': 1,
            'border': 1,
            'align': 'rigth',
            'fg_color': 'orange',
            'valign': 'vcenter'})
        title_head.set_font_name('Arial')
        title_head.set_font_size(10)

        user = self.env['res.users'].browse(self._uid)
        ws.write(0, 2, 'PACIFICO SNACKS', title_head)
        ws.write(1, 0, 'REPORTE INVENTARIO PRODUCTOS UNIDADES DE COMPRA Y VENTA', title_head)

        ws.write(3, 0, 'Bodega', title_head)
        ws.write(3, 1, 'Producto', title_head)
        ws.write(3, 2, 'Cantidad', title_head)
        ws.write(3, 3, 'Unidad Medida Compra', title_head)
        ws.write(3, 4, 'Unidad Medida Venta', title_head)
        

        fila = 4
        for x in value:
            ws.write_row(fila, 0, x)
            fila += 1

        try:
            wb.close()
            out = base64.encodestring(buf.getvalue())
            buf.close()
            self.data = out
            self.data_name = 'Reporte inventario' + ".xlsx"
        except ValueError:
            raise Warning('No se pudo generar el archivo')

#
