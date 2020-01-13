# -*- coding: utf-8 -*-

# Copyright (c) 2013 - 2017 CoNWeT Lab., Universidad Politécnica de Madrid
# Copyright (c) 2019 Future Internet Consulting and Development Solutions S.L.

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

from django.conf.urls import patterns, url

from wstore.admin import views as admin_views
from wstore.asset_manager import views as offering_views
from wstore.asset_manager.resource_plugins import views as plugins_views
from wstore.ordering import views as ordering_views
from wstore.charging_engine import views as charging_views
from wstore.charging_engine.accounting import views as accounting_views
from wstore.reports import views as reports_views

from wstore.views import ServeMedia


urlpatterns = patterns('',
    # API
    url(r'^charging/api/assetManagement/assets/?$', offering_views.AssetCollection(permitted_methods=('GET',))),
    url(r'^charging/api/assetManagement/assets/uploadJob/?$', offering_views.UploadCollection(permitted_methods=('POST',))),
    url(r'^charging/api/assetManagement/assets/validateJob/?$', offering_views.ValidateCollection(permitted_methods=('POST',))),
    url(r'^charging/api/assetManagement/assets/offeringJob/?$', offering_views.ValidateOfferingCollection(permitted_methods=('POST',))),
    url(r'^charging/api/assetManagement/assets/(?P<asset_id>\w+)/?$', offering_views.AssetEntry(permitted_methods=('GET',))),
    url(r'^charging/api/assetManagement/assets/(?P<asset_id>\w+)/upgradeJob/?$', offering_views.UpgradeCollection(permitted_methods=('POST',))),
    url(r'^charging/api/assetManagement/assets/product/(?P<product_id>\w+)/?$', offering_views.AssetEntryFromProduct(permitted_methods=('GET',))),
    url(r'^charging/api/assetManagement/assetTypes/?$', plugins_views.PluginCollection(permitted_methods=('GET', ))),
    url(r'^charging/api/assetManagement/assetTypes/(?P<plugin_id>[\w -]+)/?$', plugins_views.PluginEntry(permitted_methods=('GET',))),
    url(r'^charging/api/assetManagement/chargePeriods/?$', admin_views.ChargePeriodCollection(permitted_methods=('GET',))),
    url(r'^charging/api/assetManagement/currencyCodes/?$', admin_views.CurrencyCodeCollection(permitted_methods=('GET',))),

    url(r'^charging/api/orderManagement/orders/?$', ordering_views.OrderingCollection(permitted_methods=('POST',))),
    url(r'^charging/api/orderManagement/orders/accept/?$', charging_views.PayPalConfirmation(permitted_methods=('POST',))),
    url(r'^charging/api/orderManagement/orders/cancel/?$', charging_views.PayPalCancellation(permitted_methods=('POST',))),
    url(r'^charging/api/orderManagement/orders/refund/?$', charging_views.PayPalRefund(permitted_methods=('POST',))),
    url(r'^charging/api/orderManagement/products/?$', ordering_views.InventoryCollection(permitted_methods=('POST',))),
    url(r'^charging/api/orderManagement/products/renewJob/?$', ordering_views.RenovationCollection(permitted_methods=('POST',))),
    url(r'^charging/api/orderManagement/accounting/?$', accounting_views.ServiceRecordCollection(permitted_methods=('POST',))),
    url(r'^charging/api/orderManagement/accounting/refresh/?$', accounting_views.SDRRefreshCollection(permitted_methods=('POST',))),
    url(r'^charging/api/reportManagement/created/?$', reports_views.ReportReceiver(permitted_methods=('POST',))),
    url(r'^charging/media/(?P<path>.+)/(?P<name>[\w -.]+)/?$', ServeMedia(permitted_methods=('GET',)))
)
