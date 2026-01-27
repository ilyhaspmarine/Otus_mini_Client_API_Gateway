FROM python:3-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN groupadd -r -g 1000 basicgroup && \
    useradd -r -u 1000 -g basicgroup basicuser

WORKDIR /client-api

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /client-api

USER basicuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]