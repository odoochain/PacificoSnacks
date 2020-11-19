from odoo import fields, models, api
from odoo.exceptions import except_orm, Warning, RedirectWarning, ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Validaciones de plantilla factura electronica'

    def action_post(self):
        if self.partner_id.category_id:
            if self.partner_id.category_id[0].id == 100:
                res_company = self.env['res.company'].browse(1)
                res_company.update({'l10n_co_edi_template_code': '03'})
            elif self.partner_id.category_id[0].id == 4:
                res_company = self.env['res.company'].browse(1)
                res_company.update({'l10n_co_edi_template_code': '01'})
            else:
                raise Warning('El cliente debe pertener a la categoría Cliente/Nacional o la categoría Cliente/Exportación')
        else:
            raise Warning('El cliente no tiene asignado una categoría (Cliente/Nacional o Cliente/Exportación)')

        super(AccountMove, self).action_post()









