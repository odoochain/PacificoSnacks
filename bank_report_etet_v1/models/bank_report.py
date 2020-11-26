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


class BankReport(models.TransientModel):
    _name = 'bank.report'
    _description = 'Reporte para pago banco'

    stock_quant_id = fields.Char("LFC")
    data = fields.Binary("Archivo")
    data_name = fields.Char("nombre del archivo")
    secuencia = fields.Char("Aplicacion", default='A1')
    aplicacion = fields.Selection(string="tipo de pago", selection=[('I', 'Inmediata'), ('M', 'Medio dia'),('N', 'Noche')])
    descripcion = fields.Char("Descripcion")
    journal = fields.Many2one('account.journal', string='Diario')
    tipo_pago = fields.Selection(string="tipo de pago", selection=[('104', 'Pago a Proveedores'),('98', 'Pago de Nomina')])
    fecha_aplicacion = fields.Date('Fecha de Aplicacion')
    asientos = fields.Many2many('account.move', string='Asientos', required=True)
    exist_asientos = fields.Boolean(string='Asientos existentes', compute='get_data_asientos')

    @api.onchange('asientos')
    def get_data_asientos(self):
        if self.asientos:
            self.exist_asientos = True
        else:
            self.exist_asientos = False

    @api.onchange('journal','tipo_pago')
    def onchange_journal(self):
        for rec in self:
            return {'domain': {'asientos': [ ('name', 'like', 'CE'),('journal_id', '=', rec.journal.id),
                                             '|', ('partner_id.category_id.id', '=', int(rec.tipo_pago)),('partner_id.category_id.parent_id', '=', int(rec.tipo_pago)) ]}}

    def do_report(self):

        _logger.error("INICIA LA FUNCIÓN GENERAR EL REPORTE ")
        self.make_file()
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?model=bank.report&field=data&id=%s&filename=%s' % (
            self.id, self.data_name),
            'target': 'new',
            'nodestroy': False,
        }

    def make_file(self):
        _logger.error("INICIA LA FUNCIÓN CONSTRUIR EL ARCHIVO ")

        account = self.asientos

        if not account:
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

        company = self.env['res.company'].search([])

        ws.write(0, 0, 'NIT PAGADOR', title_head)
        ws.write(0, 1, 'TIPO DE PAGO', title_head)
        ws.write(0, 2, 'APLICACIÓN', title_head)
        ws.write(0, 3, 'SECUENCIA DE ENVIO', title_head)
        ws.write(0, 4, 'NRO CUENTA A DEBITAR', title_head)
        ws.write(0, 5, 'TIPO DE CUENTA A DEBITAR', title_head)
        ws.write(0, 6, 'DESCRIPCIÓN DEL PAGO', title_head)

        ws.write(1, 0, '' if not company[0].vat else company[0].vat)
        ws.write(1, 1, self.tipo_pago)
        if self.tipo_pago:
            if self.tipo_pago == '104':
                ws.write(1, 1, '220')
            elif self.tipo_pago == '98':
                ws.write(1, 1, '225')
            else:
                ws.write(1, 1, '')
        else:
            ws.write(1, 1, '')
        ws.write(1, 2, self.aplicacion)
        ws.write(1, 3, self.secuencia)
        ws.write(1, 4, self.journal.bank_account_id.acc_number)
        if self.journal.bank_account_id.account_type:
            if self.journal.bank_account_id.account_type == '1':
                ws.write(1, 5, 'S')
            elif self.journal.bank_account_id.account_type == '2':
                ws.write(1, 5, 'D')
            else:
                ws.write(1, 5, '')
        else:
            ws.write(1, 5, '')
        ws.write(1, 6, self.descripcion)


        ws.write(2, 0, 'Tipo Documento Beneficiario', title_head)
        ws.write(2, 1, 'Nit Beneficiario', title_head)
        ws.write(2, 2, 'Nombre Beneficiario ', title_head)
        ws.write(2, 3, 'Tipo Transaccion', title_head)
        ws.write(2, 4, 'Código Banco', title_head)
        ws.write(2, 5, 'No Cuenta Beneficiario', title_head)
        ws.write(2, 6, 'Email', title_head)
        ws.write(2, 7, 'Documento Autorizado', title_head)
        ws.write(2, 8, 'Referencia', title_head)
        ws.write(2, 9, 'OficinaEntrega', title_head)
        ws.write(2, 10, 'ValorTransaccion', title_head)
        ws.write(2, 11, 'Fecha de aplicación', title_head)

        fila = 3
        for ac in account:
            vat = ac.partner_id.vat
            if ac.partner_id.l10n_co_document_type:
               if ac.partner_id.l10n_co_document_type == 'id_document':
                   ws.write(fila, 0, '1')
               elif ac.partner_id.l10n_co_document_type == 'foreign_id_card':
                   ws.write(fila, 0, '2')
               elif ac.partner_id.l10n_co_document_type == 'rut':
                   ws.write(fila, 0, '3')
                   pos = (ac.partner_id.vat).find("-")
                   if pos != -1:
                       vat = ac.partner_id.vat[0:pos]
                   else:
                       vat = ac.partner_id.vat    
               elif ac.partner_id.l10n_co_document_type == 'id_card':
                   ws.write(fila, 0, '4')
               elif ac.partner_id.l10n_co_document_type == 'passport':
                   ws.write(fila, 0, '5')
               else:
                   ws.write(fila, 0, '')
            else:
                ws.write(fila, 0, '')

            ws.write(fila, 1, '' if not vat else vat.replace(".", ""))
            ws.write(fila, 2, ac.partner_id.name)
            if ac.partner_id.bank_ids:
                if ac.partner_id.bank_ids[0].account_type == '1':
                    ws.write(fila, 3, '27')
                elif ac.partner_id.bank_ids[0].account_type == '2':
                    ws.write(fila, 3, '37')
                else:
                    ws.write(fila, 3, '')
            else:
                    ws.write(fila, 3, '')
            ws.write(fila, 4, '') if not ac.partner_id.bank_ids else ws.write(fila, 4, ac.partner_id.bank_ids[0].bank_id.code_bank)
            ws.write(fila, 5, '') if not ac.partner_id.bank_ids else ws.write(fila, 5, ac.partner_id.bank_ids[0].acc_number)
            ws.write(fila, 6, '')
            ws.write(fila, 7, '')
            ws.write(fila, 8, '')
            ws.write(fila, 9, '')
            ws.write(fila, 10, "{:.2f}".format(ac.amount_total))
            ws.write(fila, 11, str(self.fecha_aplicacion.isoformat()).replace("-", ""))
            fila += 1

        try:
            wb.close()
            out = base64.encodestring(buf.getvalue())
            buf.close()
            self.data = out
            self.data_name = 'Reporte pago bancos' + ".xls"
        except ValueError:
            raise Warning('No se pudo generar el archivo')

#
