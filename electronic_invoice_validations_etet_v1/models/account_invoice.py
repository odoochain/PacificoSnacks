from odoo import fields, models, api
from odoo.exceptions import except_orm, Warning, RedirectWarning, ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Validaciones de plantilla factura electronica'

    def action_post(self):
        if self.journal_id.type == 'sale':
            if self.partner_id.category_id:
                get_category = False
                for category in self.partner_id.category_id:
                    if category.id == 100:
                        res_company = self.env['res.company'].browse(1)
                        res_company.update({'l10n_co_edi_template_code': '03'})
                        get_category = True
                        break
                    elif category.id == 4:
                        res_company = self.env['res.company'].browse(1)
                        res_company.update({'l10n_co_edi_template_code': '01'})
                        get_category = True
                        break
                if not get_category:
                    raise Warning(
                        'El cliente debe pertener a la categoría Cliente/Nacional o a la categoría Cliente/Exportación')
            else:
                raise Warning('El cliente no tiene asignado una categoría (Cliente/Nacional o Cliente/Exportación)')

        super(AccountMove, self).action_post()









