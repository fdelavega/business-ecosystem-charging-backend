# -*- coding: utf-8 -*-

# Copyright (c) 2013 - 2016 CoNWeT Lab., Universidad Politécnica de Madrid
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

from builtins import str
from builtins import object
from django.utils.importlib import import_module
from django.utils.functional import SimpleLazyObject
from django.utils.http import http_date, parse_http_date_safe


def get_api_user(request):
    from django.contrib.auth.models import AnonymousUser
    from django.conf import settings
    from wstore.models import Organization, User

    # Get User information from the request
    try:
        token_info = request.META['HTTP_AUTHORIZATION'].split(' ')
        nick_name = request.META['HTTP_X_NICK_NAME']
        display_name = request.META['HTTP_X_DISPLAY_NAME']
        email = request.META['HTTP_X_EMAIL']
        roles = request.META['HTTP_X_ROLES'].split(',')
        user_name = request.META['HTTP_X_ACTOR']
        external_username = request.META['HTTP_X_EXT_NAME']
    except:
        return AnonymousUser()

    if len(token_info) != 2 and token_info[0].lower() != 'bearer':
        return AnonymousUser()

    # Check if the user already exist
    try:
        user = User.objects.get(username=user_name)
    except:
        user = User.objects.create(username=user_name)

    if nick_name == user_name:
        # Update user info
        user.email = email
        user.userprofile.complete_name = display_name
        user.userprofile.actor_id = external_username
        user.is_staff = settings.ADMIN_ROLE.lower() in roles
        user.save()

    user.userprofile.access_token = token_info[1]
    
    user_roles = []

    if settings.PROVIDER_ROLE in roles:
        user_roles.append('provider')

    if settings.CUSTOMER_ROLE in roles:
        user_roles.append('customer')

    # Get or create current organization
    try:
        org = Organization.objects.get(name=nick_name)
    except:
        org = Organization.objects.create(name=nick_name)

    org.private = nick_name == user_name
    org.save()

    user.userprofile.current_roles = user_roles
    user.userprofile.current_organization = org

    # change user.userprofile.current_organization
    user.userprofile.save()

    return user


class AuthenticationMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: get_api_user(request))

        response = self.get_response(request)
        return response


class ConditionalGetMiddleware(object):
    """
    Handles conditional GET operations. If the response has a ETag or
    Last-Modified header, and the request has If-None-Match or
    If-Modified-Since, the response is replaced by an HttpNotModified.

    Also sets the Date and Content-Length response-headers.
    """
    def process_response(self, request, response):
        response['Date'] = http_date()
        if not response.has_header('Content-Length'):
            response['Content-Length'] = str(len(response.content))

        if response.has_header('ETag'):
            if_none_match = request.META.get('HTTP_IF_NONE_MATCH')
            if if_none_match == response['ETag']:
                # Setting the status is enough here. The response handling path
                # automatically removes content for this status code (in
                # http.conditional_content_removal()).
                response.status_code = 304

        if response.has_header('Last-Modified'):
            if_modified_since = request.META.get('HTTP_IF_MODIFIED_SINCE')
            if if_modified_since is not None:
                try:
                    # IE adds a length attribute to the If-Modified-Since header
                    separator = if_modified_since.index(';')
                    if_modified_since = if_modified_since[0:separator]
                except:
                    pass
                if_modified_since = parse_http_date_safe(if_modified_since)
            if if_modified_since is not None:
                last_modified = parse_http_date_safe(response['Last-Modified'])
                if last_modified is not None and last_modified <= if_modified_since:
                    # Setting the status code is enough here (same reasons as
                    # above).
                    response.status_code = 304

        return response
