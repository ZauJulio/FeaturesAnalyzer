# Stage 1: Configure the base image
###################################
FROM ubuntu:22.04

# Define environment variables
ENV TZ=Brazil/East
ENV XDG_RUNTIME_DIR=/tmp

# Set timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Stage 2: Install the base packages
###################################
RUN apt-get update -y

RUN apt install -y xauth
RUN touch /root/.Xauthority

RUN apt install   \
  libgl1-mesa-dev \
  libgl1-mesa-dri \
  mesa-common-dev \
  libgtk2.0-dev   \
  libpq-dev       \
  qtbase5-dev     \
  -y --no-install-recommends

RUN apt install      \
  python3.10         \
  python3-pip        \
  python3-setuptools \
  -y --no-install-recommends

RUN python3 -m pip install --upgrade pip

# Stage 3: Install the application dependencies
###################################

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# Stage 4: Run the application
###################################
WORKDIR /app/src

CMD ["python3", "main.py"]
