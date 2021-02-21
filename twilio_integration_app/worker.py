import logging

from twilio_integration_app.clients.beanstalk import BeanStalkClient
from twilio_integration_app.clients.twilio import TwilioClient
from twilio_integration_app.job import JobType
from twilio_integration_app.job import TwilioJob

logger = logging.getLogger("worker")


class Worker:
    def __init__(self):
        self.beanstalk_client = BeanStalkClient()
        self.twilio_client = TwilioClient()

    def listen_for_jobs(self):
        """Subscribe to channel and listen for new messages"""
        logger.info("Waiting for something to do ..")
        while True:
            twilio_job = self.beanstalk_client.fetch_job()
            try:
                logger.debug(f"Just got a job - lucky me - {twilio_job}")
                if self.process_job(twilio_job):
                    self.beanstalk_client.acknowledge_job(twilio_job)
                    logger.debug("Job done!")
                else:
                    self.beanstalk_client.retry_job(twilio_job)
                    logger.debug("Could not complete this job - sent it back")
            except Exception as ex:
                logger.error(f"Failed to process job: {twilio_job.id}. Reason: {ex}")
                self.beanstalk_client.fail_job(twilio_job)

    def process_job(self, twilio_job: TwilioJob) -> bool:
        """Handle a call message and trigger Twilio voice call"""
        logger.debug(f"Preparing to call - {twilio_job}")
        if twilio_job.type == JobType.CALL:
            result = self.twilio_client.call(twilio_job.phone_number, twilio_job.name)
            logger.debug(f"Initiated call with ID - {result.sid}")
        elif twilio_job.type == JobType.SMS:
            result = self.twilio_client.sms(twilio_job.phone_number, twilio_job.name)
            logger.debug(f"Initiated SMS sending - {result.sid}")
        return result
