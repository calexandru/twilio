# Twilio integration app

This project aims to go over a few simple phone call flows using Twilio.

This is not intended to be a fully featured application, and it has still a long way to go 
to be production ready. (where are the unit tests I hear you ask!!!)

After you cloned the source code on your local machine please edit **.env** file and add 
appropriate settings.
> since Twilio uses webhooks the web service that starts on port 5000 by default needs to be 
> forwarded to the outside and be reachable from the internet (ensure correct APP_BASE_URL is set in env)
> [How To](https://www.twilio.com/docs/voice/quickstart/python#allow-twilio-to-talk-to-your-flask-application)

Start required services (web, worker and beanstalkd)

```console
docker-compose up
```

Quick check (using test endpoint)

```console
foo@bar: curl "http://0.0.0.0:5000/test?phone_number=+40741234567&name=Dummy"

{"job_id":1}
```

Start a call flow (will trigger a call with 1-minute delay)

```console
foo@bar: curl -X POST -H "Content-Type: application/json" -d '{"phone_number": "+40741234567",
"name":"Dummy"}' http://0.0.0.0:5000/call

{"job_id":1}
```


**That's it! Explore, contribute, enjoy!**
