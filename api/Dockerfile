# build stage: use full python image to build wheels
FROM python:3.12 AS builder

WORKDIR /app

# update package lists, install build-essential (C++ compiler, make, etc)
# then, remove package lists to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# copy requirements, then install wheels, then build all wheels
COPY requirements.txt .
RUN pip install --no-cache-dir wheel
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# final stage: slim python image with only the built wheels
FROM python:3.12-slim

WORKDIR /app

# copy wheels from build stage to /wheels directory
COPY --from=builder /app/wheels /wheels

# install the wheels, which includes all dependencies
RUN pip install --no-cache /wheels/*

# copy app code into container
COPY . .

EXPOSE 8000
ENV PYTHONPATH=app
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "server:app"]