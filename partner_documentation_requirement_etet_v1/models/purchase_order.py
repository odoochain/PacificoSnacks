from odoo import fields, models, api
from odoo.exceptions import except_orm, Warning, RedirectWarning, ValidationError

class purchase_order(models.Model):
    _inherit = 'purchase.order'
    _description = 'Ordenes de compra'

    partner_doc_id = fields.Many2many('partner_documentation', string='Documentos', store=True)
    exist_doc = fields.Boolean(string='Documentos Existentes', default= False)

    @api.onchange('partner_id')
    def get_documents(self):
        if self.partner_id:
            self.partner_doc_id = self.env['partner_documentation'].search([('partner_id', '=', self.partner_id.id)])
            if self.partner_doc_id:
                self.exist_doc = True
            else:
                self.exist_doc = False

    def button_confirm(self):
        if self.partner_id.category_id:
            req_documents = self.env['required_documentation'].search([('category_id', '=', self.partner_id.category_id[0].id)])
            if req_documents.id:
                num_document = self.env['partner_documentation'].search_count([('partner_id', '=', self.partner_id.id)])
                num_doc_approved = self.env['partner_documentation'].search_count([('partner_id', '=', self.partner_id.id), ('state', '=', 'Vigente')])
                if num_doc_approved != num_document:
                    raise Warning('!No es posible confirmar la orden! Se requiere la revisión de los documentos del proveedor.')

        super(purchase_order, self).button_confirm()









