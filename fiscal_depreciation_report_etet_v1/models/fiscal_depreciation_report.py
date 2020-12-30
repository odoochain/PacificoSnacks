# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning, ValidationError
import time
from datetime import datetime, timedelta, date
import xlwt
import base64
from dateutil import relativedelta as rdelta
# from cStringIO import StringIO
from io import StringIO
from io import BytesIO
import xlsxwriter
import types
import logging


_logger = logging.getLogger(__name__)


class depreciationreport(models.TransientModel):
    _name = 'depreciation.report'
    _description = 'Fiscal Depreciation Report'

    data = fields.Binary("Archivo")
    data_name = fields.Char("nombre del archivo")
    activos = fields.Many2many('account.asset')
    date_creation = fields.Date(string='Fecha Reporte', default=fields.Date.today())
    line_mov_dep = fields.Many2many('account.move_fiscal')


    def do_report(self):

        _logger.error("INICIA LA FUNCIÓN GENERAR EL REPORTE ")
        self.make_file()
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?model=depreciation.report&field=data&id=%s&filename=%s' % (
            self.id, self.data_name),
            'target': 'new',
            'nodestroy': False,
        }

    def make_file(self):
        _logger.error("INICIA LA FUNCIÓN CONSTRUIR EL ARCHIVO ")

        activos_fijos = self.env['account.asset'].search([])
        activos_mov = self.env['account.move_fiscal'].search([])


        if not activos_fijos:
            raise Warning(_('!No hay resultados para los datos seleccionados¡'))

        buf = BytesIO()
        wb = xlsxwriter.Workbook(buf)
        ws = wb.add_worksheet('Report')

        # formatos
        title_head = wb.add_format({
            'bold': 1,
            'border': 1,
            'align': 'rigth',
            'fg_color': '#33CCCC',

            })
        title_head.set_font_name('Arial')
        title_head.set_font_size(10)
        title_head.set_font_color('#ffffff')
        format_date = wb.add_format({'num_format': 'mm/dd/yyyy'})


        ws.write(0, 1, 'PACIFICO SNACKS', title_head)
        ws.write(1, 9,  self.date_creation, format_date)
        ws.write(1, 0, 'REPORTE DEPRECIACION FISCAL ACTIVOS FIJOS', title_head)
        ws.write(1, 8, 'Fecha:')

        ws.write(2, 0, 'REFERENCIA', title_head)
        ws.write(2, 1, 'TIEMPO DEPRECIACION EN MESES DIAN', title_head)
        ws.write(2, 2, 'VALOR RESIDUAL FISCAL', title_head)
        ws.write(2, 3, 'VALOR DEPRECIACION MENSUAL', title_head)
        ws.write(2, 4, 'INICIO DEPRECIACION', title_head)
        ws.write(2, 5,  self.date_creation, format_date)
        ws.write(2, 6, 'DEPRECIACION ACUMULADA 2020', title_head)
        ws.write(2, 7, 'SALDO', title_head)
        ws.write(2, 8, 'DETERIORO', title_head)
        ws.write(2, 9, 'FECHA DE DETERIORO', title_head)


        fila = 3
        for ac in activos_fijos:
#         convierte la resta de fecha a meses de diferencia "a"
          d1 = ac.first_depreciation_date
          d2 = self.date_creation
          rd = rdelta.relativedelta(d2,d1)
          a = "{0.months}".format(rd)
          b = "{0.years}".format(rd)
          c = (int(b) * 12) + int(a) + 1
          pass
          ws.write(fila, 0, '') if not ac.name else ws.write(fila, 0, ac.name)
          ws.write(fila, 1, '') if not ac.duracion_f else ws.write(fila, 1, ac.duracion_f)
          ws.write(fila, 2, '') if not ac.non_depreciable_value else ws.write(fila, 2, "{:,.2f}".format(ac.non_depreciable_value))
          ws.write(fila, 4, '') if not ac.first_depreciation_date else ws.write(fila, 4, ac.first_depreciation_date, format_date)
          ws.write(fila, 5, '') if not ac.first_depreciation_date else ws.write(fila, 5, int(c))

          if ac.fiscal_depreciation_move_ids:
              for af in ac.fiscal_depreciation_move_ids:

                  if self.date_creation.year == af.date_fiscal.year:
                      if self.date_creation.month == af.date_fiscal.month:
                          ws.write(fila, 3, '') if not af.amount_total else ws.write(fila, 3, "{:,.2f}".format(af.amount_total))
                          ws.write(fila, 6, '') if not af.asset_depreciated_value_fiscal else ws.write(fila, 6, "{:,.2f}".format(af.asset_depreciated_value_fiscal))
                          ws.write(fila, 7, '') if not af.asset_remaining_value_fiscal else ws.write(fila, 7, "{:,.2f}".format(af.asset_remaining_value_fiscal))

              fila += 1

        try:
            wb.close()
            out = base64.encodestring(buf.getvalue())
            buf.close()
            self.data = out
            self.data_name = 'Reporte Activos Depreciacion Fiscal' + ".xls"
        except ValueError:
            raise Warning('No se pudo generar el archivo')

#
