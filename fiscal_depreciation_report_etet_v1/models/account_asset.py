from odoo import fields, models, api


class AccountAsset(models.Model):
    _inherit = 'account.asset'
    _description = 'Description'

    duracion_f = fields.Integer(string='Number of Depreciations', readonly=True, states={'draft': [('readonly', False)], 'model': [('readonly', False)]}, default=5, help="Numero de depreciaciones para el activo informe fiscal ")
    tax_residual_value = fields.Monetary(string="Valor Residual Fiscal", help="Valor digitable a partir de 2018" )
    method_period_fiscal = fields.Selection([('1', 'Months'), ('12', 'Years')], string='Number of Months in a Period',
                                     readonly=True, default='12',
                                     states={'draft': [('readonly', False)], 'model': [('readonly', False)]},
                                     help="The amount of time between two depreciations")
    data = fields.Binary("Archivo")
    data_name = fields.Char("nombre del archivo")
    equipos = fields.Many2many('maintenance.equipment')
    date_creation = fields.Date('Created Date', required=True, default=fields.Date.today())

    def compute_depreciation_fiscal_board(self):
        self.ensure_one()
        amount_change_ids = self.depreciation_move_ids.filtered(lambda x: x.asset_value_change and not x.reversal_move_id).sorted(key=lambda l: l.date)
        posted_depreciation_move_ids = self.depreciation_move_ids.filtered(lambda x: x.state == 'posted' and not x.asset_value_change and not x.reversal_move_id).sorted(key=lambda l: l.date)
        already_depreciated_amount = sum([m.amount_total for m in posted_depreciation_move_ids])
        depreciation_number = self.duracion_f
        if self.prorata:
            depreciation_number += 1
        starting_sequence = 0
        amount_to_depreciate = self.tax_residual_value + sum([m.amount_total for m in amount_change_ids])
        depreciation_date = self.first_depreciation_date
        # if we already have some previous validated entries, starting date is last entry + method period
        if posted_depreciation_move_ids and posted_depreciation_move_ids[-1].date:
            last_depreciation_date = fields.Date.from_string(posted_depreciation_move_ids[-1].date)
            if last_depreciation_date > depreciation_date:  # in case we unpause the asset
                depreciation_date = last_depreciation_date + relativedelta(months=+int(self.method_period))
        commands = [(2, line_id.id, False) for line_id in self.depreciation_move_ids.filtered(lambda x: x.state == 'draft')]
        newlines = self._recompute_board(depreciation_number, starting_sequence, amount_to_depreciate, depreciation_date, already_depreciated_amount, amount_change_ids)
        newline_vals_list = []
        for newline_vals in newlines:
            # no need of amount field, as it is computed and we don't want to trigger its inverse function
            del(newline_vals['amount_total'])
            newline_vals_list.append(newline_vals)
        new_moves = self.env['account.move'].create(newline_vals_list)
        for move in new_moves:
            commands.append((4, move.id))
        return self.write({'depreciation_move_ids': commands})

    def do_report(self):

#        _logger.error("INICIA LA FUNCIÓN GENERAR EL REPORTE ")
        self.make_file()
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?model=depreciation.report&field=data&id=%s&filename=%s' % (
            self.id, self.data_name),
            'target': 'new',
            'nodestroy': False,
        }

    def make_file(self):
#        _logger.error("INICIA LA FUNCIÓN CONSTRUIR EL ARCHIVO ")

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
        ws.write(1, 0, 'REPORTE ACTIVOS Y USUARIOS', title_head)
        ws.write(1, 2, 'Fecha:')

        ws.write(2, 0, 'TIEMPO DEPRECIACION EN MESES DIAN', title_head)
        ws.write(2, 1, 'VALOR RESIDUAL', title_head)
        ws.write(2, 2, 'VALOR DEPRECIACION MENSUAL', title_head)
        ws.write(2, 3, 'INICIO DEPRECIACION', title_head)
        ws.write(2, 4, 'AÑO', title_head)
        ws.write(2, 5, 'DEPRECIACION ACUMULADA 2020', title_head)
        ws.write(2, 6, 'SALDO', title_head)
        ws.write(2, 7, 'DETERIORO', title_head)
        ws.write(2, 8, 'FECHA DE DETERIORO', title_head)


        fila = 3
        for eq in equipamiento:

          ws.write(fila, 0, '') if not eq.name else ws.write(fila, 0, eq.partner_ref)
          ws.write(fila, 1, '') if not eq.name else ws.write(fila, 1, eq.name)
          ws.write(fila, 2, '') if not eq.employee_id.name else ws.write(fila, 2, eq.employee_id.name)
          ws.write(fila, 3, '') if not eq.location else ws.write(fila, 3, eq.location)
          ws.write(fila, 5, '') if not eq.name else ws.write(fila, 5, eq.partner_ref)
          fila += 1

        try:
            wb.close()
            out = base64.encodestring(buf.getvalue())
            buf.close()
            self.data = out
            self.data_name = 'Reporte Activos' + ".xls"
        except ValueError:
            raise Warning('No se pudo generar el archivo')