# -*- coding: utf-8 -*-
from datetime import date, datetime, time, timedelta

import babel
from dateutil.relativedelta import relativedelta
from pytz import timezone

from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError, AccessError, ValidationError


def days_between(start_date, end_date):
    #Add 1 day to end date to solve different last days of month 
    #s1, e1 =  datetime.strptime(start_date,"%Y-%m-%d") , datetime.strptime(end_date,"%Y-%m-%d")  + timedelta(days=1)
    s1, e1 =  start_date , end_date + timedelta(days=1)
    #Convert to 360 days
    s360 = (s1.year * 12 + s1.month) * 30 + s1.day
    e360 = (e1.year * 12 + e1.month) * 30 + e1.day
    #Count days between the two 360 dates and return tuple (months, days)
    res = divmod(e360 - s360, 30)
    return ((res[0] * 30) + res[1]) or 0

           
class HrPayslip(models.Model):
    _inherit = 'hr.payslip'


    type_payslip_id = fields.Many2one('hr.type.payslip', string="Type")


    def actualizar_entradas(self):
        res = self.onchange_employee_id()                                              
        return True


    def get_inputs_hora_extra(self, contract_id, date_from, date_to):
        self._cr.execute(''' SELECT i.name, i.code, h.amount FROM hr_extras h
                                INNER JOIN hr_rule_input i ON i.id=h.input_id
                                WHERE h.contract_id=%s AND h.state='approved'
                                AND h.date BETWEEN %s AND %s
                                ORDER BY i.code''',(contract_id.id, date_from, date_to))
        horas_extras = self._cr.fetchall()
        return horas_extras        

    def get_inputs_loans(self, contract_id, date_from, date_to):
        self._cr.execute(''' SELECT i.name, i.code, l.amount
                                FROM hr_loan_line l
                                INNER JOIN hr_loan h ON h.id=l.loan_id
                                INNER JOIN hr_rule_input i ON i.id=h.input_id
                                WHERE h.contract_id=%s AND h.state='approve'
                                AND l.date BETWEEN %s AND %s
                                AND h.loan_fijo IS False
                                ORDER BY i.code ''',(contract_id.id, date_from, date_to))
        loans_ids = self._cr.fetchall()
        return loans_ids        

    def get_inputs_loans_fijos(self, contract_id):
        self._cr.execute(''' SELECT i.name, i.code, h.loan_amount
                                FROM hr_loan h
                                INNER JOIN hr_rule_input i ON i.id=h.input_id
                                WHERE h.contract_id=%s AND h.state='approve'
                                AND h.loan_fijo IS True
                                ORDER BY i.code ''',(contract_id.id,))
        loans_fijos_ids = self._cr.fetchall()
        return loans_fijos_ids        


    @api.model
    def get_inputs(self, contracts, date_from, date_to):
        res = []

        structure_ids = contracts.get_all_structures()
        rule_ids = (
            self.env["hr.payroll.structure"].browse(structure_ids).get_all_rules()
        )
        sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x: x[1])]
        payslip_inputs = (
            self.env["hr.salary.rule"].browse(sorted_rule_ids).mapped("input_ids")
        )
        for contract in contracts:
            horas_extras = self.get_inputs_hora_extra(contract, date_from, date_to)
            if horas_extras:
                for hora in horas_extras:
                    res.append({
                            "name": hora[0],
                            "code": hora[1],
                            "amount": hora[2],
                            "contract_id": contract.id,
                    })

            loans_ids = self.get_inputs_loans(contract, date_from, date_to)
            if loans_ids:
                for loan in loans_ids:
                    res.append({
                            "name": loan[0],
                            "code": loan[1],
                            "amount": loan[2],
                            "contract_id": contract.id,
                    })

            loans_fijos_ids = self.get_inputs_loans_fijos(contract)
            if loans_fijos_ids:
                for loan_fijo in loans_fijos_ids:
                    res.append({
                            "name": loan_fijo[0],
                            "code": loan_fijo[1],
                            "amount": loan_fijo[2],
                            "contract_id": contract.id,
                    })

            # for payslip_input in payslip_inputs:
            #     res.append(
            #         {
            #             "name": payslip_input.name,
            #             "code": payslip_input.code,
            #             "contract_id": contract.id,
            #         }
            #     )
        return res        


    def onchange_employee_id(self):
        if (not self.employee_id) or (not self.date_from) or (not self.date_to):
            return

        employee = self.employee_id
        date_from = self.date_from
        date_to = self.date_to
        contract_ids = self.contract_id.ids

        ttyme = datetime.combine(date_from, time.min)
        locale = self.env.context.get("lang") or "en_US"
        self.name = _("Salary Slip of %s for %s") % (
            employee.name,
            tools.ustr(
                babel.dates.format_date(date=ttyme, format="MMMM-y", locale=locale)
            ),
        )
        self.company_id = employee.company_id

        if not self.env.context.get("contract") or not self.contract_id:
            contract_ids = self.get_contract(employee, date_from, date_to)
            if not contract_ids:
                return
            self.contract_id = self.env["hr.contract"].browse(contract_ids[0])

        if not self.contract_id.struct_id:
            return
        self.struct_id = self.contract_id.struct_id

        # computation of the salary input
        contracts = self.env["hr.contract"].browse(contract_ids)
        worked_days_line_ids = self.get_worked_day_lines(contracts, date_from, date_to)
        worked_days_lines = self.worked_days_line_ids.browse([])
        for r in worked_days_line_ids:
            worked_days_lines += worked_days_lines.new(r)
        self.worked_days_line_ids = worked_days_lines

        input_line_ids = self.get_inputs(contracts, date_from, date_to)
        input_lines = self.input_line_ids.browse([])
        for r in input_line_ids:
            input_lines += input_lines.new(r)
        self.input_line_ids = input_lines
        return


    @api.model
    def get_worked_day_lines(self, contracts, date_from, date_to):
        """
        @param contract: Browse record of contracts
        @return: returns a list of dict containing the input that should be
        applied for the given contract between date_from and date_to
        """
        res = []
        # fill only if the contract as a working schedule linked
        for contract in contracts.filtered(lambda contract: contract.resource_calendar_id):
            day_from = datetime.combine(date_from, time.min)
            day_to = datetime.combine(date_to, time.max)

            # compute leave days
            leaves = {}
            calendar = contract.resource_calendar_id
            tz = timezone(calendar.tz)
            day_leave_intervals = contract.employee_id.list_leaves(
                day_from, day_to, calendar=contract.resource_calendar_id
            )
            for day, hours, leave in day_leave_intervals:
                holiday = leave[:1].holiday_id
                current_leave_struct = leaves.setdefault(
                    holiday.holiday_status_id,
                    {
                        "name": holiday.holiday_status_id.name or _("Global Leaves"),
                        "sequence": 5,
                        "code": holiday.holiday_status_id.name or "GLOBAL",
                        "number_of_days": 0.0,
                        "number_of_hours": 0.0,
                        "contract_id": contract.id,
                    },
                )
                current_leave_struct["number_of_hours"] += hours
                work_hours = calendar.get_work_hours_count(
                    tz.localize(datetime.combine(day, time.min)),
                    tz.localize(datetime.combine(day, time.max)),
                    compute_leaves=False,
                )
                if work_hours:
                    current_leave_struct["number_of_days"] += hours / work_hours

            # compute worked days
            if contract.date_start >= self.date_from:
                day_from = datetime.combine(contract.date_start, time.min)
                work_data = contract.employee_id._get_work_days_data(
                    day_from, day_to, calendar=contract.resource_calendar_id
                )
            else:
                work_data = contract.employee_id._get_work_days_data(
                    day_from, day_to, calendar=contract.resource_calendar_id
                )
               
            if not contract.resource_calendar_id.hours_per_day:
                raise ValidationError(
                    _("Debe ingresar la cantidad de horas por dia en la Planificación de trabajo del contrato del empleado")
                )                
            total_days = days_between(date_from, date_to)
            total_hours = total_days*contract.resource_calendar_id.hours_per_day
            attendances_total = {
                "name": _("Total del periodo"),
                "sequence": 1,
                "code": "TOTALDAYS",
                "number_of_days": total_days,
                "number_of_hours": total_hours,
                "contract_id": contract.id,
            }            

            attendances = {
                "name": _("Normal Working Days paid at 100%"),
                "sequence": 1,
                "code": "WORK100",
                "number_of_days": work_data["days"],
                "number_of_hours": work_data["hours"],
                "contract_id": contract.id,
            }

            res.append(attendances_total)
            res.append(attendances)
            res.extend(leaves.values())
        return res        