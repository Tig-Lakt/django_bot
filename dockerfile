FROM python:3.10-slim-buster

WORKDIR /django_bot

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "src/main.py"]