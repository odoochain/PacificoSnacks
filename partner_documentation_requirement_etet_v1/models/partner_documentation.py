from odoo import fields, models, api
import time
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class Partner_documentation(models.Model):
    _name = 'partner_documentation'
    _description = 'Documentacion de compañias'

    partner_id = fields.Many2one('res.partner', string='Compañia')
    document_name = fields.Char('Documento')
    date_expedition = fields.Date('Fecha de expedición')
    date_checked = fields.Date(compute ='get_date_checked', string='Fecha de aprobación', store=True)
    approved = fields.Boolean('Aprobado')
    validity_unit = fields.Integer(default=1, string="Vigencia (unidad)")
    validity_period = fields.Selection([('months', 'Meses'), ('years', 'Años')], string='Vigencia (periodo)', default='years')
    date_expiration = fields.Date(compute ='get_date_expiration', string='Fecha de vencimiento', store=True)
    state = fields.Char(compute ='get_state', string='Estado', store=True)
    category_id = fields.Many2one('res.partner.category', string='Categoria')

    @api.constrains('validity_unit')
    def _validity_unit(self):
        if self.validity_unit > 500:
            raise ValidationError('La unidad de vigencia no puede ser mayor a 500!')
        if self.validity_unit == 0:
            raise ValidationError('La unidad de vigencia no puede ser igual a 0!')

    @api.depends('approved')
    def get_date_checked(self):
        for recod in self:
            if recod.approved == True :
                recod.date_checked = datetime.now()
            else:
                recod.date_checked = False

    @api.depends('date_expedition','validity_period','validity_unit' )
    def get_date_expiration(self):
        for recod in self:
            if recod.date_expedition != False:
                if recod.validity_period == 'months':
                    month = relativedelta(months=recod.validity_unit)
                    recod.date_expiration = recod.date_expedition + month
                elif recod.validity_period == 'years':
                    years = relativedelta(years=recod.validity_unit)
                    recod.date_expiration = recod.date_expedition + years
            else:
                    recod.date_expiration = False

    @api.depends('date_expedition', 'approved', 'validity_period','validity_unit')
    def get_state(self):
        today =  date.today()
        for recod in self:
            if   recod.date_expedition != False and recod.date_expiration != False and recod.date_expedition > recod.date_expiration:
                 recod.state = 'Vencido'
                 recod.approved = False
            elif recod.date_expiration != False and today >= recod.date_expiration:
                 recod.state = 'Vencido'
                 recod.approved = False
            elif recod.date_expedition != False and recod.date_expiration != False and recod.date_expedition < recod.date_expiration and today < recod.date_expiration:
                 recod.state = 'Vigente'
                 recod.approved = True
            elif recod.date_expiration == False and recod.date_expedition == False:
                 recod.state = 'Pendiente'
                 recod.approved = False
            elif recod.date_expiration == False:
                 recod.state = 'Pendiente'
                 recod.approved = False
            elif recod.date_expedition == False:
                 recod.state = 'Pendiente'
                 recod.approved = False
            elif recod.approved == False:
                 recod.state = 'Pendiente'
            else:
                 recod.state = 'Sin definir'















