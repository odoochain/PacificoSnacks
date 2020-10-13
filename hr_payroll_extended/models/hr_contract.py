# -*- coding: utf-8 -*-
from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError, ValidationError

import logging

_logger = logging.getLogger(__name__)
           
class HrContract(models.Model):
    """
    Employee contract based on the visa, work permits
    allows to configure different Salary structure
    """

    _inherit = "hr.contract"
    _description = "Employee Contract"


    def get_all_structures(self):
        """
        @return: the structures linked to the given contracts, ordered by
                 hierachy (parent=False first, then first level children and
                 so on) and without duplicata
        """
        structures = self.mapped("struct_id")
        if not structures:
            return []
        # YTI TODO return browse records
        return list(set(structures._get_parent_structure().ids))