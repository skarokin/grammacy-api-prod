# build stage: use full python image to build wheels
FROM python:3.12 AS builder
WORKDIR /app

COPY requirements.txt .
# update package lists, install build-essential for compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# final stage: slim python image with only the built wheels
# no alpine because often causes issues with compiled C extensions
FROM python:3.12-slim
WORKDIR /app

# copy wheels from build stage to /wheels directory
COPY --from=builder /app/wheels /wheels

# install the wheels, which includes all dependencies
RUN pip install --no-cache-dir /wheels/*

# copy app code into container
COPY . .

EXPOSE 8000
ENV PYTHONPATH=app
# limit compute resources
CMD ["gunicorn", "--workers=1", "--threads=2", "--worker-class=gthread", "--timeout=120", "-b", "0.0.0.0:8000", "server:app"]