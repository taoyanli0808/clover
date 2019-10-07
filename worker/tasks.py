
from clover import celery


@celery.task()
def run_automation(*args, **kargs):
    """
    :param args:
    :param kargs:
    :return:
    """
    pass


@celery.task()
def run_interface(*args, **kargs):
    """
    :param args:
    :param kargs:
    :return:
    """
    pass


@celery.task()
def run_performance(*args, **kargs):
    """
    :param args:
    :param kargs:
    :return:
    """
    pass
