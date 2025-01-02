FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libcairo2-dev python3-cairo-dev libgirepository1.0-dev gobject-introspection \
    at-spi2-core libcanberra-gtk3-module libgdk-pixbuf2.0-dev libgdk-pixbuf2.0-0 adwaita-icon-theme-full \
    python3-pip meson ninja-build \
    libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7-dev \
    libtiff-dev tk-dev tcl-dev libblas-dev liblapack-dev \
    libgtk-3-dev \
    libx11-dev wayland-protocols libffi-dev xorg \
    && rm -rf /var/lib/apt/lists/*

# Install pip, setuptools, and upgrade them
RUN pip install --no-cache-dir --upgrade pip setuptools

# Install meson-python
RUN pip install --no-cache-dir meson-python

# Install pygobject
RUN pip install --no-cache-dir --no-build-isolation pygobject==3.50.0

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app
COPY .env /app/.env

WORKDIR /app/src

# Set the entry point
CMD ["python", "main.py"]
