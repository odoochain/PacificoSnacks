from datetime import date, timedelta, datetime

from odoo import fields, models, api

class Sales(models.Model):
    _inherit = 'sale.order'
    _description = 'calculo de fechas'

    requested_delivery_date = fields.Date('Fecha solicitada de entrega')
    #days_in_transit = fields.Integer('Days in Transit')
    possible_upload_date = fields.Char('Posible fecha de cargue', compute='_possible_upload_date')
    #day_upload_customer = fields.Integer('dato cliente')
    num_day = fields.Integer('dia')
    to_days = fields.Integer(string='Dias en transito', related='partner_id.to_days')
    day_upload_week = fields.Selection(string='Dia de cargue cliente', related='partner_id.day_upload_week')

    @api.onchange('requested_delivery_date')
    def _possible_upload_date(self):

        if self.requested_delivery_date != False:
            day_upload = self.requested_delivery_date - timedelta(days=self.to_days)
            self.num_day = day_upload.strftime("%w")

            if int(self.day_upload_week) > self.num_day:
               resta = self.num_day - int(self.day_upload_week)
               self.possible_upload_date = (day_upload - timedelta(days=resta)).strftime("%d-%m-%y-%A")
            elif int(self.day_upload_week) < self.num_day:
               resta = int(self.day_upload_week) - self.num_day
               self.possible_upload_date = (day_upload + timedelta(days=resta)).strftime("%d-%m-%y-%A")
            else:
               self.possible_upload_date = day_upload.strftime("%d-%m-%y-%A")
        else:
               self.possible_upload_date = False