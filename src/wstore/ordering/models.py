# -*- coding: utf-8 -*-

# Copyright (c) 2013 - 2016 CoNWeT Lab., Universidad Politécnica de Madrid
# Copyright (c) 2021 Future Internet Consulting and Development Solutions S. L.

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


from djongo import models
from django.contrib.auth.models import User

from wstore.models import Organization, Resource
from wstore.ordering.errors import OrderingError


class Offering(models.Model):
    off_id = models.CharField(max_length=50, blank=True, null=True)
    href = models.URLField()
    owner_organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=100)
    description = models.CharField(max_length=1500)
    is_digital = models.BooleanField(default=True)
    asset = models.ForeignKey(Resource, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_open = models.BooleanField(default=False)
    bundled_offerings = models.JSONField() # List


class Charge(models.Model):
    date = models.DateTimeField()
    cost = models.CharField(max_length=100)
    duty_free = models.CharField(max_length=100)
    currency = models.CharField(max_length=3)
    concept = models.CharField(max_length=100)
    invoice = models.CharField(max_length=200)


class Contract(models.Model):
    item_id = models.CharField(max_length=50)
    product_id = models.CharField(max_length=50, blank=True, null=True)
    offering = models.ForeignKey(Offering, on_delete=models.DO_NOTHING)

    # Parsed version of the pricing model used to calculate charges
    pricing_model = models.JSONField() # Dict
    # Date of the last charge to the customer
    last_charge = models.DateTimeField(blank=True, null=True)
    # List with the made charges
    charges = models.ArrayField(model_container=Charge)

    # Usage fields
    correlation_number = models.IntegerField(default=0)
    last_usage = models.DateTimeField(blank=True, null=True)

    # Revenue sharing product class
    revenue_class = models.CharField(max_length=15, blank=True, null=True)

    suspended = models.BooleanField(default=False)
    terminated = models.BooleanField(default=False)


class Payment(models.Model):
    transactions = models.JSONField() # List
    concept = models.CharField(max_length=20)
    free_contracts = models.ArrayField(model_container=(Contract))


class Order(models.Model):
    description = models.CharField(max_length=1500)
    order_id = models.CharField(max_length=50)
    customer = models.ForeignKey(User)
    owner_organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True, blank=True)
    date = models.DateTimeField()
    sales_ids = models.JSONField() # List

    state = models.CharField(max_length=50)
    tax_address = models.JSONField() # Dict

    # List of contracts attached to the current order
    contracts = models.ArrayField(model_container=(Contract))

    # Pending payment info used in asynchronous charges
    pending_payment = models.EmbeddedField(model_container=Payment, null=True)

    def get_item_contract(self, item_id):
        # Search related contract
        for c in self.contracts:
            if c.item_id == item_id:
                contract = c
                break
        else:
            raise OrderingError('Invalid item id')

        return contract

    def get_product_contract(self, product_id):
        # Search related contract
        for c in self.contracts:
            if c.product_id == product_id:
                contract = c
                break
        else:
            raise OrderingError('Invalid product id')

        return contract

    class Meta:
        app_label = 'wstore'