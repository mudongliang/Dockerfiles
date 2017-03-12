FROM debian:latest
MAINTAINER "Dongliang Mu" <mudongliangabcd@gmail.com>
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y build-essential screenfetch
RUN rm -rf /var/lib/apt/lists/*
CMD /usr/bin/screenfetch
