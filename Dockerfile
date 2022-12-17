FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY Pipfile Pipfile.lock .

RUN pip3 install pipenv
RUN pipenv install --system --deploy

COPY . .
RUN rm -f /app/done.txt

EXPOSE 8000

ENTRYPOINT ["bash", "/app/startup.sh"]