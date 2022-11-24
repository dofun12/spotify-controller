FROM python:3.9-alpine
WORKDIR /app

COPY . .
RUN pip3 install poetry
RUN poetry --no-root install
CMD [ "python3", "-m" , "uvicorn", "main:app", "--host=0.0.0.0", "--port", "8080"]