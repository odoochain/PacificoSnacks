from odoo import fields, models, api
import time
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

class Partner_documentation(models.Model):
    _name = 'partner_documentation'
    _description = 'Documentacion de compañias'

    partner_id = fields.Many2one('res.partner', string='Compañia')
    document_name = fields.Char('Documento')
    date_checked = fields.Date('Fecha de aprobación')
    approved = fields.Boolean('Aprobado')
    validity_unit = fields.Integer(default=1, string="Vigencia (unidad)")
    validity_period = fields.Selection([('months', 'Meses'), ('years', 'Años')], string='Vigencia (periodo)', default='years')
    date_expiration = fields.Date(compute ='get_date_expiration', string='Fecha de vencimiento', store=True)
    state = fields.Char(compute ='get_state', string='Estado de aprobación', store=True)
    category_id = fields.Many2one('res.partner.category', string='Categoria')

    @api.onchange('approved')
    def _date_checked(self):
        if self.approved == True :
            self.date_checked = datetime.now()
        else:
            self.date_checked = False

    @api.depends('date_checked','validity_period','validity_unit' )
    def get_date_expiration(self):
        for recod in self:
            if recod.date_checked != False:
                if recod.validity_period == 'months':
                    month = relativedelta(months=recod.validity_unit)
                    recod.date_expiration = recod.date_checked + month
                elif recod.validity_period == 'years':
                    years = relativedelta(years=recod.validity_unit)
                    recod.date_expiration = recod.date_checked + years
            else:
                    recod.date_expiration = False

    @api.depends('date_checked')
    def get_state(self):
        today =  date.today()
        for recod in self:
            if   recod.date_checked != False and recod.date_expiration != False and recod.date_checked > recod.date_expiration:
                 recod.state = 'Vencido'
            elif recod.date_expiration != False and today > recod.date_expiration:
                 recod.state = 'Vencido'
            elif recod.date_checked != False and recod.date_expiration != False and recod.date_checked < recod.date_expiration and today < recod.date_expiration:
                 recod.state = 'Vigente'
                 recod.approved = True
            elif recod.date_expiration == False and recod.date_checked == False:
                 recod.state = 'Pendiente'
                 recod.approved = False
            elif recod.date_expiration == False:
                 recod.state = 'Pendiente'
                 recod.approved = False
            elif recod.date_checked == False:
                 recod.state = 'Pendiente'
                 recod.approved = False
            elif recod.approved == False:
                 recod.state = 'Pendiente'
            else:
                 recod.state = 'Sin definir'















