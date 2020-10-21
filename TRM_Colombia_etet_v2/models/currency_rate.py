import logging
from odoo import fields, models, api
import time
from suds.client import Client
_logger = logging.getLogger(__name__)

class currency_rate(models.Model):
    _inherit = "res.currency.rate"

    @api.model
    def get_col_trm(self):

        WSDL_URL = 'https://www.superfinanciera.gov.co/SuperfinancieraWebServiceTRM/TCRMServicesWebService/TCRMServicesWebService?WSDL'
        date = time.strftime('%Y-%m-%d')
        try:
            client = Client(WSDL_URL, location=WSDL_URL, faults=True)
            trm = client.service.queryTCRM(date)
        except Exception as e:
            return _logger.critical("Error while working with BancoRep API: " + str(e))

        last_rates = self.env["res.currency.rate"].search([("name", "=", date), ("currency_id", "=", 2)])

        if last_rates.name == False :
            vals = {
            "rate": float(trm.value),
            "name": date,
            "currency_id": 2
            }
            super(currency_rate, self).create(vals)
            _logger.info(
                "New exchange rate created to date: " +
                date +
                ", with value: " +
                str(float(trm.value))
            )
        else:
            _logger.critical("Already exist TRM for the date "+date)
















