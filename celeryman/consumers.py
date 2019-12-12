import logging

from celeryman import tasks
from django.conf import settings

from chassis.core.consumers_registry import registry
from feather.consumers import CUDBaseConsumerStep


logger = logging.getLogger(__name__)


@registry.register
class CelerymanMagpieWorkConsumerStep(CUDBaseConsumerStep):
    important_data = ['work_identifier']
    queue_name = settings.CELERYMAN_MAGPIE_WORK_CUD_QUEUE
    routing_key = settings.CELERYMAN_WORK_CUD_ROUTING_KEY
    verbose_message = 'work'

    def create_method(self, body):
        logger.info(">>> create_method body")
        logger.info(body)

    def update_method(self, body):
        logger.info(">>> update_method body")
        logger.info(body)

    def delete_method(self, body):
        tasks.do_something_in_celery.delay('woof')
