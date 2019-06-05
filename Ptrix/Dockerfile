FROM ubuntu:14.04
MAINTAINER "Dongliang Mu" <mudongliangabcd@gmail.com>
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y build-essential autoconf unzip gawk texinfo bison flex

WORKDIR /root/

# Github repo is too big, so it's better to test it with local file
COPY afl-pt.zip /root
RUN unzip afl-pt.zip

WORKDIR /root/afl-pt-master

#RUN cd pt; make -j$(nproc); ./reinstall_ptmod.sh

# Build the customized AFL
RUN cd afl-2.42b; make -j$(nproc)

## Build elfpatcher
RUN cd afl-2.42b/pt_mode/elfpatcher; ./bootstrap.sh; ./configure; make -j$(nproc)

# Build pt_proxy
RUN cd afl-2.42b/pt_mode/pt_proxy; make -j$(nproc)

# Build customized ld
RUN cd afl-2.42b/pt_mode/glibc-2.19; mkdir build; cd build; ../configure --disable-sanity-checks; make -j$(nproc)

# Build testcase cxxfilt
RUN cd afl-2.42b/test_progs/binutils-2.29; mkdir build; cd build; ../configure --enable-shared=no --enable-static=yes; make -j$(nproc)

# Patch testcase cxxfilt
RUN cd afl-2.42b/pt_mode; ./patch-bin.sh ../test_progs/binutils-2.29/build/binutils/cxxfilt

# Fuzzing testcase cxxfilt 
#RUN cd afl-2.42b/
#./pt-fuzz-fast -P -i ./testcases/others/elf -o ./test_progs/binutils-2.29/build/binutils/cxxfilt_out -- ./test_progs/binutils-2.29/build/binutils/cxxfilt

RUN rm -rf /var/lib/apt/lists/*
CMD lsb_release -a
