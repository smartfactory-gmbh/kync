ARG extra_pipenv_args
ARG extra_os_packages
ARG mode
ARG release

FROM tiangolo/uwsgi-nginx:python3.11

COPY .docker/nginx.conf /etc/nginx/conf.d/extra.conf

WORKDIR /app

# Install Python and Package Libraries
RUN yes | pip install --no-cache-dir pipenv
RUN apt-get update && apt-get install -y gcc libpq-dev musl-dev gettext net-tools netcat

COPY ./Pipfile ./Pipfile.lock /app/

RUN pipenv install --system --deploy --clear $extra_pipenv_args

COPY . /app/

RUN mkdir -p /app/static && mkdir -p /app/media && mkdir -p /app/locale
VOLUME /app/media

RUN python ./manage.py collectstatic --noinput

HEALTHCHECK --interval=1m --timeout=3s \
    CMD curl -H 'X-HealthCheck: check' -f "http://localhost/" || exit 1

ENV RELEASE=$release
