# Initial stage
FROM python:3.8.6 AS python-base-image
ENV PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false

# -- Build stage --
FROM python-base-image as builder
WORKDIR /app
# install poetry in the base python image
RUN pip install --no-cache-dir "poetry==1.1.4"
# create a virtual environment where we will install the project and his dependencies
RUN python -m venv /app/venv
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --without-hashes | /app/venv/bin/pip install -r /dev/stdin
COPY . .
# install the project main package
RUN poetry build && /app/venv/bin/pip install dist/*.whl

# -- Final stage -- we use the slim python image
FROM python:3.8.6-slim as twilio_web
# move the created virtual env from the build stage
COPY --from=builder /app /app
# add virtual env bin to path - this will allow the call of "app" cli
ENV PATH=/app/venv/bin:$PATH
# image entry command
CMD ["run", "-t", "web"]

# -- Final stage -- we use the slim python image
FROM python:3.8.6-slim as twilio_worker
# move the created virtual env from the build stage
COPY --from=builder /app /app
# add virtual env bin to path - this will allow the call of "app" cli
ENV PATH=/app/venv/bin:$PATH
# image entry command
CMD ["run", "-t", "worker"]
