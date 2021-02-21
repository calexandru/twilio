import re

from flask import abort
from flask import Flask
from flask import request

from twilio_integration_app.clients.beanstalk import BeanStalkClient
from twilio_integration_app.clients.twilio import TwilioTemplates
from twilio_integration_app.job import JobType
from twilio_integration_app.job import TwilioJob

ONE_MINUTE = 60  # in seconds
FIVE_SECONDS = 5
YES_SPEECH = "yes"
NO_SPEECH = "no"

flask_app = Flask(__name__)
flask_app.queue = BeanStalkClient()


@flask_app.route("/", methods=["GET"])
def home():
    flask_app.logger.debug("Hello")
    return "Twilio integration WEB"


@flask_app.route("/call", methods=["POST"])
def call():
    client_data = request.json
    if not client_data:
        abort(400, "Invalid call - expected json payload")
    if not (phone_number := client_data.get("phone_number")):
        abort(400, "Phone number is mandatory")
    if not (name := client_data.get("name")):
        abort(400, "Name is mandatory")
    job = TwilioJob(phone_number, name)
    job_id = flask_app.queue.publish_job(job, delay=ONE_MINUTE)
    flask_app.logger.debug(f"Published new call job: {job}")
    return {"job_id": job_id}


@flask_app.route("/test", methods=["GET"])
def test():
    name = request.args.get("name", "John Doe")
    phone_number = request.args.get("phone_number", "John Doe")
    delay = int(request.args.get("delay", "5"))
    job_type = JobType(request.args.get("type", "call"))

    job = TwilioJob(phone_number, name, type=job_type)
    job_id = flask_app.queue.publish_job(job, delay=delay)
    flask_app.logger.debug(f"Published new call job: {job}")
    return {"job_id": job_id}


@flask_app.route("/action_callback", methods=["POST"])
def action_callback():
    flask_app.logger.info(f"Action details: {request.values}")
    speech_result = request.values.get("SpeechResult", "")
    flask_app.logger.debug(f"This words were said to us: {speech_result}")
    words = list(map(str.lower, filter(None, re.split(r"\.|,|\s", speech_result))))
    if YES_SPEECH in words:
        return TwilioTemplates.yes_answer()
    elif NO_SPEECH in words:
        return TwilioTemplates.no_answer()
    return TwilioTemplates.unrecognized_answer()


@flask_app.route("/call_status", methods=["POST"])
def call_status():
    flask_app.logger.debug(f"Status details: {request.values}")
    if request.values.get("CallStatus") in ["busy", "no-answer", "cancelled"]:
        phone_number = request.values.get("To")
        name = request.args.get("name", "")
        job = TwilioJob(phone_number, name, type=JobType.SMS)
        flask_app.queue.publish_job(job, delay=FIVE_SECONDS)
        flask_app.logger.debug(f"Published new SMS job: {job}")
    return "OK"


@flask_app.route("/voicemail", methods=["POST"])
def voicemail():
    flask_app.logger.debug(f"Voicemail details: {request.values}")
    return TwilioTemplates.voicemail()
