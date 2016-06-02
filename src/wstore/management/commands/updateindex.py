# -*- coding: utf-8 -*-

# Copyright (c) 2013 - 2016 CoNWeT Lab., Universidad Polit?cnica de Madrid

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

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from wstore.admin.searchers import ResourceBrowser


class Command(BaseCommand):

    help = 'Updates the index of the specified resource'

    def add_arguments(self, parser):

        parser.add_argument('resource_namespace', nargs='+')

    def handle(self, *args, **options):

        # Loop over the namespaces
        for namespace in args:

            # Clear the index of this type of resource
            ix = ResourceBrowser.clear_index(namespace)

            if ix is None:
                raise CommandError('Resource "%s" does not exist' % namespace)

            # Get the model of this type of resource
            model = ResourceBrowser.get_resource_model(namespace)

            # Add model fields for each resource
            for resource in model.objects.all():
                ResourceBrowser.add_resource(namespace, resource=resource)

            self.stdout.write('The index of "%s" resource was updated successfully.\n' % namespace)
