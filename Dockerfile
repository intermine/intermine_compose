FROM python:3.6-alpine AS python-build-env
LABEL maintainer="Ank"
RUN apk update && apk add ca-certificates && apk add libpq postgresql-dev && apk add libffi-dev \
    && apk add build-base && rm -rf /var/cache/apk/*
WORKDIR /app
ADD requirements.txt /app
RUN cd /app && pip install -r requirements.txt

FROM python:3.6-alpine
LABEL maintainer="Ank"
RUN apk update && apk add ca-certificates && apk add libpq postgresql-client
WORKDIR /app
ADD . /app
COPY --from=python-build-env /root/.cache /root/.cache
RUN cd /app && pip install -r requirements.txt && rm -rf /root/.cache
RUN chmod +x launch.sh
EXPOSE 9991
CMD ["/bin/sh", "/app/launch.sh"]