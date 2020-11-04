from odoo import fields, models, api
import time
from . import required_documentation

class Partner(models.Model):
    _inherit = 'res.partner'
    _description = 'Documentacion requerida para proveedores'

    num_document = fields.Integer(compute='compute_documents')
    num_doc_approved = fields.Integer(compute='compute_documents')
    all_doc_approved = fields.Boolean(compute='compute_documents')

    def compute_documents(self):
            self.num_document = self.env['partner_documentation'].search_count([('partner_id', '=', self.id)])
            self.num_doc_approved = self.env['partner_documentation'].search_count([('partner_id', '=', self.id), ('state', '=', 'Vigente')])
            if self.num_doc_approved == self.num_document:
                self.all_doc_approved = True
            else:
                self.all_doc_approved = False

    def get_documentation(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Documentation',
            'view_mode': 'tree',
            'res_model': 'partner_documentation',
            'domain': [('partner_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def write(self, values):
        res = super(Partner, self).write(values)
        partner_id = self.id
        if self.category_id.id != False:
            category_id = self.category_id[0].id
            self.create_document(category_id, partner_id)
        else:
            partner_doc = self.env['partner_documentation'].search([('partner_id', '=', partner_id)])
            partner_doc.unlink()
        return res

    def create_document(self, category_id, partner_id):

        date = time.strftime('%Y-%m-%d')
        req_documents = self.env['required_documentation'].search([('category_id', '=', category_id)])
        if req_documents.id != False:
            for doc in req_documents.documentation_id:
                partner_doc = self.env['partner_documentation'].search([('partner_id', '=', partner_id),('document_name', '=', doc.document_name),('category_id', '=', category_id)])
                not_category_doc = self.env['partner_documentation'].search([('partner_id', '=', partner_id), ('category_id', '!=', category_id)])
                not_category_doc.unlink()
                if partner_doc.id == False:
                    vals = {
                        "partner_id": partner_id,
                        "document_name": doc.document_name,
                        "date_checked": False,
                        "approved": False,
                        "validity_unit": doc.validity_unit,
                        "validity_period": doc.validity_period,
                        "category_id": req_documents.category_id.id,
                        "state": 'Pendiente',
                        "date_expiration": False,
                    }
                    self.env['partner_documentation'].create(vals)
        if req_documents.id == False:
            partner_doc = self.env['partner_documentation'].search([('partner_id', '=', partner_id), ('category_id', '!=', category_id)])
            partner_doc.unlink()









