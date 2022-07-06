FROM ubuntu:18.04
WORKDIR /app

# Set envs
ENV TZ=Brazil/East
ENV XDG_RUNTIME_DIR=/tmp

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . .

RUN apt-get update -y

RUN apt install -y xauth
RUN touch /root/.Xauthority

RUN apt install -y libgl1-mesa-dev libgl1-mesa-dri mesa-common-dev libgtk2.0-dev libpq-dev qt5-default --no-install-recommends
RUN apt install -y python3.8 python3-pip python3-setuptools --no-install-recommends

RUN python3 -m pip install --upgrade pip

RUN pip install -r requirements.txt

WORKDIR /app/src

CMD ["python3", "main.py"]