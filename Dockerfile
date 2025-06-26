FROM python:3.12-bullseye

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		postgresql-client \
        git \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

# COPY PROJECT
COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
