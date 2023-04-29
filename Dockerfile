FROM python:3.11-slim-buster

# Define ARGs
ARG ENVIRONMENT=default

# Python logs to STDOUT
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements/*.txt /tmp/requirements/
RUN set -x \
    && buildDeps=" \
    libffi-dev \
    libpq-dev \
    binutils \
    " \
    && runDeps=" \
    postgresql-client \
    gcc \
    " \
    && apt-get update \
    && apt-get install -y $buildDeps $runDeps \
    && pip install -r /tmp/requirements/base.txt \
    && if [ $ENVIRONMENT = local ]; then \
        # Install python dev dependencies
        pip install -r /tmp/requirements/test.txt \
        && pip install -r /tmp/requirements/dev.txt; \
    fi \
    && apt-get remove -y $buildDeps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Work dir and copy code.
WORKDIR /app
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]