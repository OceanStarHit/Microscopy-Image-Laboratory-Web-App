from celery_tasks.tasks import StitchingCeleryTask
from celery_tasks.utils import create_worker_from

class StitchingCeleryTaskImpl(StitchingCeleryTask):

    def run(self, payload):
        print(payload)

        """ actual implementation """
        num_1 = float(payload['num_1'])
        num_2 = float(payload['num_2'])
        ans = num_1 + num_2
        return ans

# create celery app
app, _ = create_worker_from(StitchingCeleryTaskImpl)

# start worker
if __name__ == '__main__':
    app.worker_main()