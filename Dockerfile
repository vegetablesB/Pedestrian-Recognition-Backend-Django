FROM python:3.10
LABEL maintainer="cabeza"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt update && \
    apt install postgresql postgresql-contrib -y && \
    apt install ffmpeg libsm6 libxext6  -y && \
    # apt install --update --no-cache postgresql-client && \
    # apt install \
    #     build-base postgresql-dev musl-dev zlib zlib-dev -y && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    /py/bin/pip install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cpu && \
    if [ "$DEV" = "true" ] ; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    # apt del .tmp-build-deps && \
    # useradd -rm -d /home/django-user -s /bin/bash -g root -G sudo -u 1001 django-user && \
    adduser \
        --disabled-password \
        # --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol/web

ENV PATH="/py/bin:$PATH"

USER django-user
