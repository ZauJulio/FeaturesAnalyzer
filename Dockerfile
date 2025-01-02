FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake \
    gobject-introspection \
    libcairo2-dev \
    libcanberra-gtk3-module \
    libgdk-pixbuf2.0-dev \
    libgirepository1.0-dev \
    libgtk-3-dev \
    meson \
    ninja-build \
    python3-cairo-dev \
    wayland-protocols \
    xorg

# Clean up APT when done
RUN rm -rf /var/lib/apt/lists/* && apt-get clean

# Install/update base dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools meson-python

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
