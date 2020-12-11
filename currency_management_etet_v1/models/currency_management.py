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


class divisas(models.TransientModel):
    _name = 'divisas'
    _description = 'Divisas'

    fecha = fields.Date('fecha')
    trm = fields.Float('TRM', compute='compute_trm')


    def do_report(self):

        _logger.error("INICIA LA FUNCIÓN GENERAR EL REPORTE ")
        self.make_file()
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?model=divisas.report&field=data&id=%s&filename=%s' % (
            self.id, self.data_name),
            'target': 'new',
            'nodestroy': False,
        }

    def make_file(self):
        _logger.error("INICIA LA FUNCIÓN CONSTRUIR EL ARCHIVO ")

        equipamiento = self.env['maintenance.equipment'].search([])
        date_creation = fields.Date.today()
        pass
        if not equipamiento:
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
            'valign': 'vcenter',
            })
        title_head.set_font_name('Arial')
        title_head.set_font_size(10)
        title_head.set_font_color('#ffffff')
        format_date = wb.add_format({'num_format': 'mm/dd/yyyy'})


        ws.write(0, 1, 'PACIFICO SNACKS', title_head)
        ws.write(1, 3,  date_creation, format_date)
        ws.write(1, 0, 'REPORTE DIVISAS', title_head)
        ws.write(1, 2, 'Fecha:')

        ws.write(2, 0, 'TERCERO', title_head)
        ws.write(2, 1, 'USD', title_head)
        ws.write(2, 2, 'TRM INICIAL', title_head)
        ws.write(2, 3, 'VALOR RECONOCIMIENTO INICIAL', title_head)
        ws.write(2, 4, 'TRM DIA PAGO', title_head)
        ws.write(2, 5, 'VALOR EN PESOS DIA PAGO', title_head)
        ws.write(2, 6, 'DIFERENCIA EN CAMBIO', title_head)

        fila = 3
        for eq in equipamiento:

          ws.write(fila, 0, '') if not eq.name else ws.write(fila, 0, eq.partner_ref)
          ws.write(fila, 1, '') if not eq.name else ws.write(fila, 1, eq.name)
          ws.write(fila, 2, '') if not eq.employee_id.name else ws.write(fila, 2, eq.employee_id.name)
          ws.write(fila, 3, '') if not eq.location else ws.write(fila, 3, eq.location)
          fila += 1

        try:
            wb.close()
            out = base64.encodestring(buf.getvalue())
            buf.close()
            self.data = out
            self.data_name = 'Reporte Activos' + ".xls"
        except ValueError:
            raise Warning('No se pudo generar el archivo')

    #