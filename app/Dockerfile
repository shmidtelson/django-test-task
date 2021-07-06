FROM python:3.9
RUN printenv > env.txt
RUN cat env.txt
ENV PYTHONUNBUFFERED=1
ARG APP_PATH=/code
RUN mkdir -p ${APP_PATH}
COPY . ${APP_PATH}
WORKDIR ${APP_PATH}

RUN pip install pipenv
RUN pipenv install --deploy --system --ignore-pipfile
