from datetime import date, timedelta, datetime

from odoo import fields, models, api

class Sales(models.Model):
    _inherit = 'sale.order'
    _description = 'calculo de fechas'

    requested_delivery_date = fields.Date('Fecha solicitada de entrega')
    possible_upload_date = fields.Char('Posible fecha de cargue')
    num_day = fields.Integer('dia')
    to_days = fields.Integer(string='Dias en transito', related='partner_id.to_days')
    day_upload_week = fields.Selection(string='Dia de cargue cliente', related='partner_id.day_upload_week')
    possible_arrival_date_destination = fields.Char('Posible fecha llegada a destino')

    @api.onchange('requested_delivery_date')
    def _possible_upload_date(self):

        if self.requested_delivery_date != False:

            day_upload = self.requested_delivery_date - timedelta(days=self.to_days)
            self.num_day = day_upload.strftime("%w")

            while self.num_day != int(self.day_upload_week):
                day_upload = day_upload - timedelta(days=1)
                self.num_day = day_upload.strftime("%w")

            self.possible_upload_date = day_upload.strftime("%m-%d-%Y")
            self.possible_arrival_date_destination = (day_upload + timedelta(days=self.to_days)).strftime("%m-%d-%Y")
        else:
               self.possible_upload_date = False





