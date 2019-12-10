# This file is automatically created by the `regen` command.
# To make changes please edit the `SERVICE_DOCKERFILES` setting.
# See https://devdocs.platform-dev.gcp.oreilly.com/chassis/dockerfile.html#dockerfiles
FROM gcr.io/common-build/chassis:latest
ENV DJANGO_SETTINGS_MODULE celeryman.settings
COPY /requirements.txt /orm/service/requirements.txt
RUN pip install --no-cache-dir --no-compile -r /orm/service/requirements.txt
COPY . /orm/service/
WORKDIR /orm/service/
RUN /orm/manage.py collectstatic --noinput
