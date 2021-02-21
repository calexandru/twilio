import json
from dataclasses import asdict
from dataclasses import dataclass
from enum import Enum


class JobType(str, Enum):
    CALL = "call"
    SMS = "sms"


@dataclass
class TwilioJob:
    phone_number: str
    name: str
    id: int = 0
    type: JobType = JobType.CALL

    def serialize(self):
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_data):
        return cls(**json.loads(json_data))
