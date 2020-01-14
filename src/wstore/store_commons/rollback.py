# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2017 CoNWeT Lab., Universidad Politécnica de Madrid

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

import os

from django.conf import settings

from wstore.models import ResourceVersion


def downgrade_asset(asset):
    prev_version_id = asset.old_versions.pop()
    prev_version = ResourceVersion.objects.get(id=prev_version_id)

    # Check if a file has to be removed
    if asset.resource_path != '':
        file_path = settings.BASEDIR + '/' + asset.resource_path

        if os.path.exists(file_path):
            os.remove(file_path)

    asset.resource_path = prev_version.resource_path
    asset.version = prev_version.version
    asset.download_link = prev_version.download_link
    asset.meta_info = prev_version.meta_info
    asset.content_type = prev_version.content_type
    asset.state = 'attached'
    asset.save()


def downgrade_asset_pa(self):
    if hasattr(self, '_to_downgrade') and self._to_downgrade is not None and len(self._to_downgrade.old_versions):
        downgrade_asset(self._to_downgrade)


def rollback(post_action=None):
    """
    Make a rollback in case a failure occurs during the execution of a given method
    :param post_action: Callable to be executed as the last step of a rollback
    :return:
    """

    def wrap(method):
        def _remove_file(file_):
            os.remove(file_)

        def _remove_model(model):
            model.delete()

        def wrapper(self, *args, **kwargs):
            # Inject rollback logger
            self.rollback_logger = {
                'files': [],
                'models': []
            }

            try:
                result = method(self, *args, **kwargs)
            except Exception as e:

                # Remove created files
                for file_ in self.rollback_logger['files']:
                    _remove_file(file_)

                # Remove created models
                for model in self.rollback_logger['models']:
                    _remove_model(model)

                if post_action is not None:
                    post_action(self)

                raise e

            return result

        return wrapper
    return wrap
