from typing import List, Dict

import celery

# contains all celery tasks
# implementations are found in each respective task main.py file


class StitchingCeleryTask(celery.Task):
    name = 'stitching_celery_task'

    def run(self, tiles, pattern):
        """
        place holder method
        """
        pass

class DDCeleryTask(celery.Task):
    name = 'dd_celery_task'

    def run(self, tiles, pattern):
        """
        place holder method
        """
        pass

class DDDCeleryTask(celery.Task):
    name = 'ddd_celery_task'

    def run(self, tiles, pattern):
        """
        place holder method
        """
        pass

class FocusCeleryTask(celery.Task):
    name = 'focus_celery_task'

    def run(self, tiles, pattern):
        """
        place holder method
        """
        pass

class SRRFCeleryTask(celery.Task):
    name = 'srrf_celery_task'

    def run(self, tiles, pattern):
        """
        place holder method
        """
        pass

