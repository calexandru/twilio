import greenstalk

from twilio_integration_app import settings
from twilio_integration_app.job import TwilioJob

TEN_MINUTES = 600  # in seconds


class BeanStalkClient:
    def __init__(
        self,
        host=settings.BEANSTALK_HOST,
        port=settings.BEANSTALK_PORT,
        tube=settings.BEANSTALK_TUBE,
        **kwargs
    ):
        self.client = greenstalk.Client(address=(host, port), use=tube, watch=tube, **kwargs)

    def publish_job(self, twilio_job: TwilioJob, delay: int = 0) -> int:
        return self.client.put(twilio_job.serialize(), delay=delay)

    def fetch_job(self) -> TwilioJob:
        job = self.client.reserve()
        twilio_job = TwilioJob.from_json(job.body)
        twilio_job.id = job.id
        return twilio_job

    def acknowledge_job(self, twilio_job: TwilioJob) -> None:
        self.client.delete(greenstalk.Job(id=twilio_job.id, body=""))

    def retry_job(self, twilio_job: TwilioJob) -> None:
        self.client.release(greenstalk.Job(id=twilio_job.id, body=""), delay=TEN_MINUTES)

    def fail_job(self, twilio_job: TwilioJob) -> None:
        self.client.bury(greenstalk.Job(id=twilio_job.id, body=""))
