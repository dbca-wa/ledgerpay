import logging
from ledgerpay.main_models import GlobalSettings

logger = logging.getLogger(__name__)


def construct_name_values(mul):
    ret = []
    for i in range(1, 21):
        ret.append({'name': str(i), 'value': i})
    return ret


class DefaultDataManager(object):

    def __init__(self):
        # Store
        for item in GlobalSettings.default_values:
            try:
                obj, created = GlobalSettings.objects.get_or_create(key=item[0])
                if created:
                    obj.value = item[1]
                    obj.save()
                    logger.info("Created {}: {}".format(item[0], item[1]))
            except Exception as e:
                logger.error('{}, Key: {}'.format(e, item[0]))