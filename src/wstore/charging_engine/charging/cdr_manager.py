# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2016 CoNWeT Lab., Universidad Politécnica de Madrid

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

from bson import ObjectId
from decimal import Decimal

from django.conf import settings

from wstore.rss_adaptor.rss_adaptor import RSSAdaptorThread
from wstore.store_commons.database import get_database_connection


class CDRManager(object):

    _order = None

    def __init__(self, order, contract):
        self._order = order
        self._contract = contract

    def _generate_cdr_part(self, part, event, cdr_info):
        # Create connection for raw database access
        db = get_database_connection()

        # Take and increment the correlation number using
        # the mongoDB atomic access in order to avoid race
        # problems
        currency = self._contract.pricing_model['general_currency']

        # Version 2 uses a correlation number per provider
        corr_number = db.wstore_organization.find_and_modify(
            query={'_id': ObjectId(self._contract.offering.owner_organization.pk)},
            update={'$inc': {'correlation_number': 1}}
        )['correlation_number']

        return {
            'provider': cdr_info['provider'],
            'correlation': unicode(corr_number),
            'order': self._order.order_id + ' ' + self._contract.item_id,
            'offering': cdr_info['offering'],
            'product_class': cdr_info['product_class'],
            'description': cdr_info['description'],
            'cost_currency': currency,
            'cost_value': unicode(part['value']),
            'tax_value': unicode(Decimal(part['value']) - Decimal(part['duty_free'])),
            'time_stamp': cdr_info['time_stamp'],
            'customer': cdr_info['customer'],
            'event': event
        }

    def generate_cdr(self, applied_parts, time_stamp, price=None, duty_free=None):

        cdrs = []

        # Set offering ID
        off_model = self._contract.offering
        offering = off_model.off_id + ' ' + off_model.name + ' ' + off_model.version
        currency = self._contract.pricing_model['general_currency']

        # Get the provider (Organization)
        provider = off_model.owner_organization.name

        # Get the customer
        customer = self._order.owner_organization.name

        cdr_info = {
            'provider': provider,
            'offering': offering,
            'time_stamp': time_stamp,
            'customer': customer,
            'product_class': self._contract.revenue_class
        }

        # If any deduction has been applied the whole payment is
        # included in a single CDR instead of including parts in
        # order to avoid a mismatch between the revenues being shared
        # and the real payment

        if price is not None:
            # Create a payment part representing the whole payment
            aggregated_part = {
                'value': price,
                'duty_free': duty_free,
                'currency': self._contract.pricing_model['general_currency']
            }
            cdr_info['description'] = 'Complete Charging event: ' + unicode(price) + ' ' + currency
            cdrs.append(self._generate_cdr_part(aggregated_part, 'Charging event', cdr_info))

        else:
            # Check the type of the applied parts
            if 'single_payment' in applied_parts:

                # A cdr is generated for every price part
                for part in applied_parts['single_payment']:
                    cdr_info['description'] = 'One time payment: ' + unicode(part['value']) + ' ' + currency
                    cdrs.append(self._generate_cdr_part(part, 'One time payment event', cdr_info))

            if 'subscription' in applied_parts:

                # A cdr is generated by price part
                for part in applied_parts['subscription']:
                    cdr_info['description'] = 'Recurring payment: ' + unicode(part['value']) + ' ' + currency + ' ' + part['unit']
                    cdrs.append(self._generate_cdr_part(part, 'Recurring payment event', cdr_info))

            if 'accounting' in applied_parts:

                # A cdr is generated by price part
                for part in applied_parts['accounting']:
                    use_part = {
                        'value': part['price'],
                        'duty_free': part['duty_free'],
                        'currency': currency
                    }

                    # Calculate the total consumption
                    use = 0
                    for sdr in part['accounting']:
                        use += int(sdr['value'])
                        cdr_info['description'] = 'Fee per ' + part['model']['unit'] + ', Consumption: ' + unicode(use)

                    cdrs.append(self._generate_cdr_part(use_part, 'Pay per use event', cdr_info))

        # Send the created CDRs to the Revenue Sharing System
        r = RSSAdaptorThread(cdrs)
        r.start()
