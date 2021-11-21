import celery

# contains all celery tasks
# implementations are found in each respective task main.py file

class StitchingCeleryTask(celery.Task):
    name = 'stitching_celery_task'

    def run(self, payload):
        """
        place holder method
        """
        pass

