import os
from logging.config import dictConfig

API_BASE_URL = os.getenv("BASE_URL", "http://cpersic.go.ro/")

# FLASK
APP_HOST = os.getenv("APP_HOST", "localhost")
APP_PORT = int(os.getenv("APP_PORT", "5000"))

# BEANSTALK
BEANSTALK_HOST = os.getenv("BEANSTALK_HOST", "localhost")
BEANSTALK_PORT = int(os.getenv("REDIS_PORT", "11300"))
BEANSTALK_TUBE = os.getenv("BEANSTALK_TUBE", "twilio_tube")

# TWILIO
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+447723328061")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "GENERICSID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "generictoken")

# LOGGING
LOG_LEVEL = os.getenv("LOG_LEVEL") or "DEBUG"
LOGGING = {
    "version": 1,
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s: %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "worker": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        }
    },
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
}
dictConfig(LOGGING)
