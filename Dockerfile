FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    postgresql-client
    
# build-essential

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD [ "uvicorn", "application.asgi:application", "--host", "0.0.0.0", "--port", "8000" ]