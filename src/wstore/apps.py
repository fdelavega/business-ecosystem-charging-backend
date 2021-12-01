
from django.apps import AppConfig


class WstoreConfig(AppConfig):
    name = 'wstore'
    verbose_name = 'WStore'

    def ready(self):
        import sys

        from django.conf import settings
        from django.core.exceptions import ImproperlyConfigured

        from wstore.models import Context
        from wstore.store_commons.utils.url import is_valid_url
        from wstore.ordering.inventory_client import InventoryClient
        from wstore.rss_adaptor.rss_manager import ProviderManager

        testing = sys.argv[1:2] == ['test'] or sys.argv[1:2] == ['migrate']
        if not testing:
            # Validate that a correct site and local_site has been provided
            if not is_valid_url(settings.SITE) or not is_valid_url(settings.LOCAL_SITE):
                raise ImproperlyConfigured('SITE and LOCAL_SITE settings must be a valid URL')

            # Create context object if it does not exists
            if not len(Context.objects.all()):
                Context.objects.create(
                    failed_cdrs=[],
                    failed_upgrades=[]
                )

            inventory = InventoryClient()
            inventory.create_inventory_subscription()

            # Create RSS default aggregator and provider
            credentials = {
                'user': settings.STORE_NAME,
                'roles': [settings.ADMIN_ROLE],
                'email': settings.WSTOREMAIL
            }
            prov_manager = ProviderManager(credentials)

            try:
                prov_manager.register_aggregator({
                    'aggregatorId': settings.WSTOREMAIL,
                    'aggregatorName': settings.STORE_NAME,
                    'defaultAggregator': True
                })
            except Exception as e:  # If the error is a conflict means that the aggregator is already registered
                if e.response.status_code != 409:
                    raise e
