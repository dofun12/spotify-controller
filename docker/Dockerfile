FROM python:3.9
WORKDIR /app


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
# CMD [ "python3", "main.py", "--host=0.0.0.0", "--port", "8080"]
CMD [ "python3", "main.py", "--host=0.0.0.0", "--port=8082", "--cron-hour", "3", "--cron-minute", "0"]