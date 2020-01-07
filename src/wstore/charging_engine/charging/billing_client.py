# -*- coding: utf-8 -*-

# Copyright (c) 2016 - 2017 CoNWeT Lab., Universidad Politécnica de Madrid

# This file belongs to the business-charging-backend
# of the Business API Ecosystem.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
from __future__ import division

from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import object
from past.utils import old_div
from decimal import Decimal
from requests import Session, Request
from urllib.parse import urlparse, urljoin

from django.conf import settings


class BillingClient(object):

    def __init__(self):
        self._billing_api = settings.BILLING
        if not self._billing_api.endswith('/'):
            self._billing_api += '/'

    def create_charge(self, charge_model, product_id, start_date=None, end_date=None):

        str_time = charge_model.date.isoformat() + 'Z'
        tax_rate = (old_div((Decimal(charge_model.cost) - Decimal(charge_model.duty_free)) * Decimal('100'), Decimal(charge_model.cost)))

        domain = settings.SITE
        invoice_url = urljoin(domain, charge_model.invoice)
        description = charge_model.concept + ' charge of ' + charge_model.cost + ' ' + charge_model.currency + ' ' + invoice_url

        charge = {
            'date': str_time,
            'description': description,
            'type': charge_model.concept,
            'currencyCode': charge_model.currency,
            'taxIncludedAmount': charge_model.cost,
            'taxExcludedAmount': charge_model.duty_free,
            'appliedCustomerBillingTaxRate': [{
                'amount': str(tax_rate),
                'taxCategory': 'VAT'
            }],
            'serviceId': [{
                'id': product_id,
                'type': 'Inventory product'
            }]
        }

        if end_date is not None or start_date is not None:
            start_period = start_date.isoformat() + 'Z' if start_date is not None else str_time
            end_period = end_date.isoformat() + 'Z' if end_date is not None else str_time

            charge['period'] = [{
                'startPeriod': start_period,
                'endPeriod': end_period
            }]

        url = self._billing_api + 'api/billingManagement/v2/appliedCustomerBillingCharge'
        req = Request('POST', url, json=charge)

        session = Session()
        prepped = session.prepare_request(req)

        # Override host header to avoid inconsistent hrefs in the API
        prepped.headers['Host'] = urlparse(domain).netloc

        resp = session.send(prepped)
        resp.raise_for_status()
