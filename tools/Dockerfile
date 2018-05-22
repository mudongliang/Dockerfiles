FROM debian:latest
MAINTAINER "Dongliang Mu" <mudongliangabcd@gmail.com>
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install build-essential wget
WORKDIR /root
RUN wget https://raw.githubusercontent.com/mudongliang/source-packages/master/CVE-2004-2167/latex2rtf-1.9.15.tar.gz; \
tar -xvf latex2rtf-1.9.15.tar.gz; \
cd latex2rtf-1.9.15; \
make; \
make install;
RUN wget https://raw.githubusercontent.com/mudongliang/LinuxFlaw/master/CVE-2004-2167/latex2rtf.c; \
gcc -o exploit latex2rtf.c; ./exploit > poc.tex
RUN rm -rf /var/lib/apt/lists
CMD latex2rtf-1.9.15/latex2rtf poc.tex
