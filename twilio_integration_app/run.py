import argparse

from twilio_integration_app import settings
from twilio_integration_app.app import flask_app
from twilio_integration_app.worker import Worker


class RunType:
    WEB_SERVER = "web"
    WORKER = "worker"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=(RunType.WEB_SERVER, RunType.WORKER),
        default=RunType.WEB_SERVER,
        help="What service should we start?",
    )
    args = parser.parse_args()
    if args.type == RunType.WEB_SERVER:
        flask_app.run(host=settings.APP_HOST, port=settings.APP_PORT)
    else:
        w = Worker()
        w.listen_for_jobs()


if __name__ == "__main__":
    main()
