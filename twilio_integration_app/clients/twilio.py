import urllib
from urllib.parse import urljoin

from twilio.rest import Client
from twilio.twiml.voice_response import Gather
from twilio.twiml.voice_response import VoiceResponse

from twilio_integration_app import settings


class TwilioClient:
    def __init__(
        self, account_sid=settings.TWILIO_ACCOUNT_SID, auth_token=settings.TWILIO_AUTH_TOKEN
    ):
        self.client = Client(account_sid, auth_token)

    def call(self, phone_number: str, name: str):
        qs_data = urllib.parse.urlencode({"phone_number": phone_number, "name": name})
        return self.client.calls.create(
            twiml=TwilioTemplates.voice_call(name),
            to=phone_number,
            from_=settings.TWILIO_PHONE_NUMBER,
            machine_detection="DetectMessageEnd",
            status_callback=urljoin(settings.API_BASE_URL, f"/call_status?{qs_data}"),
            status_callback_event=["completed"],
            async_amd_status_callback=urljoin(settings.API_BASE_URL, "voicemail"),
        )

    def sms(self, phone_number: str, name: str):
        return self.client.messages.create(
            body=f"Hi {name}, this is Alex, let me know when is a better time to chat.",
            to=phone_number,
            from_=settings.TWILIO_PHONE_NUMBER,
        )


class TwilioTemplates:
    @staticmethod
    def voice_call(name: str) -> str:
        response = VoiceResponse()
        action_url = urljoin(settings.API_BASE_URL, "action_callback")
        gather = Gather(
            action=action_url,
            method="POST",
            input="speech",
            hints="yes, no",
            timeout=5,
            actionOnEmptyResult="true",
            speechTimeout="auto",
        )
        gather.say(
            f"Hi {name} - Would like to subscribe to updates from Alex? (Say Yes or No)",
        )
        response.append(gather)
        response.say("We didn't receive any input. Goodbye!")
        response.hangup()
        return str(response)

    @staticmethod
    def yes_answer() -> str:
        response = VoiceResponse()
        response.say("This is great! Welcome onboard.")
        response.hangup()
        return str(response)

    @staticmethod
    def no_answer() -> str:
        response = VoiceResponse()
        response.say("How unfortunate, maybe some other time.")
        response.hangup()
        return str(response)

    @staticmethod
    def unrecognized_answer() -> str:
        response = VoiceResponse()
        response.say("Could not understand your answer. Goodbye!")
        response.hangup()
        return str(response)

    @staticmethod
    def voicemail() -> str:
        response = VoiceResponse()
        response.say("Hey, this is Alex trying to reach you!")
        response.hangup()
        return str(response)

    @staticmethod
    def hangup() -> str:
        return str(VoiceResponse().hangup())
