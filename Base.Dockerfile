FROM mcr.microsoft.com/devcontainers/python:3.11
WORKDIR /app
ADD . /app/
EXPOSE 8000

RUN apt upgrade -y
RUN apt update -y

RUN python -m venv .venv
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# CMD ["uvicorn", "main.entrypoint.main:app", "--host", "0.0.0.0", "--port", "8000"]
