FROM debian:jessie

RUN apt-get update
RUN apt-get install -y --force-yes wget gnupg

# Unfortunately, this key isn't available over HTTPS.
RUN wget -O /tmp/llvm-snapshot.gpg.key http://apt.llvm.org/llvm-snapshot.gpg.key
RUN apt-key add /tmp/llvm-snapshot.gpg.key
RUN bash -c 'echo "deb http://apt.llvm.org/jessie/ llvm-toolchain-jessie-4.0 main" >> /etc/apt/sources.list'
RUN bash -c 'echo "deb-src http://apt.llvm.org/jessie/ llvm-toolchain-jessie-4.0 main" >> /etc/apt/sources.list'
RUN apt-get update
RUN apt-get install -y --force-yes clang-4.0 clang-4.0-doc libclang-common-4.0-dev libclang-4.0-dev libclang1-4.0 libclang1-4.0-dbg libllvm-4.0-ocaml-dev libllvm4.0 libllvm4.0-dbg lldb-4.0 llvm-4.0 llvm-4.0-dev llvm-4.0-doc llvm-4.0-examples llvm-4.0-runtime clang-format-4.0 python-clang-4.0 libfuzzer-4.0-dev


ENV CFLAGS="-O1 -g -fsanitize=address,bool,float-cast-overflow,integer-divide-by-zero,return,returns-nonnull-attribute,shift-exponent,unreachable,vla-bound -fno-sanitize-recover=all -fno-omit-frame-pointer -DFUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION=1"
ENV CXXFLAGS="-O1 -g -fsanitize=address,bool,float-cast-overflow,integer-divide-by-zero,return,returns-nonnull-attribute,shift-exponent,unreachable,vla-bound -fno-sanitize-recover=all -fno-omit-frame-pointer -DFUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION=1"
ENV LDFLAGS="-g -fsanitize=address,bool,float-cast-overflow,integer-divide-by-zero,return,returns-nonnull-attribute,shift-exponent,unreachable,vla-bound"
ENV CC="/usr/bin/clang-4.0"
ENV CXX="/usr/bin/clang++-4.0"
ENV ASAN_OPTIONS="exitcode=1,handle_segv=1,detect_leaks=1,leak_check_at_exit=1,allocator_may_return_null=1,detect_odr_violation=0"
ENV ASAN_SYMBOLIZER_PATH="/usr/lib/llvm-4.0/bin/llvm-symbolizer"

RUN bash -c 'echo "export CFLAGS=\"${CFLAGS}\"" >> /root/.bashrc'
RUN bash -c 'echo "export CXXFLAGS=\"${CXXFLAGS}\"" >> /root/.bashrc'
RUN bash -c 'echo "export LDFLAGS=\"${LDFLAGS}\"" >> /root/.bashrc'
RUN bash -c 'echo "export CC=\"${CC}\"" >> /root/.bashrc'
RUN bash -c 'echo "export CXX=\"${CXX}\"" >> /root/.bashrc'
RUN bash -c 'echo "export CXXFLAGS=\"${CXXFLAGS}\"" >> /root/.bashrc'
RUN bash -c 'echo "export ASAN_OPTIONS=\"${ASAN_OPTIONS}\"" >> /root/.bashrc'
RUN bash -c 'echo "export ASAN_SYMBOLIZER_PATH=\"${ASAN_SYMBOLIZER_PATH}\"" >> /root/.bashrc'
RUN bash -c 'echo "echo Use `docker cp /path/to/input <container>:/path/inside/container` to stage files for testing" >> /root/.bashrc'

# Only the last ENTRYPOINT or CMD is honored, so this can be overridden.
ENTRYPOINT /bin/bash
RUN apt-get install -y --force-yes git make

WORKDIR /root
RUN git clone git://sourceware.org/git/binutils-gdb.git
WORKDIR /root/binutils-gdb
RUN git reset --hard 1b19ec971047a074486e6b775dc1969aa13f30fb
WORKDIR /root/binutils-gdb/build
RUN sh /root/binutils-gdb/libiberty/configure
RUN make

RUN echo '#include <stdint.h>\n#include <stdlib.h>\n#include <string.h>\n\n#include "demangle.h"\n\n\
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {\n\
\tchar *name = new char[size + 1];\n\
\tmemcpy(name, data, size);\n\
\tname[size] = 0;  // NUL-terminate\n\
\tchar *demangled = cplus_demangle(name, DMGL_AUTO);\n\
\tif (demangled) free(demangled);\n\
\tdelete[] name;\n\
\treturn 0;\n\
}' > ../libiberty/demangle_fuzzer.cc
RUN bash -c 'source /root/.bashrc && $CXX $CXXFLAGS $LDFLAGS -DHAVE_DECL_BASENAME -I../include ../libiberty/demangle_fuzzer.cc libiberty.a -lFuzzer -o demangle_fuzzer'

RUN bash -c 'echo "#!/bin/bash" > /root/repro.sh'
RUN bash -c 'echo "/root/binutils-gdb/build/demangle_fuzzer \$1" >> /root/repro.sh'
RUN bash -c 'chmod 755 /root/repro.sh'

RUN bash -c 'echo "echo \"Repro: /root/repro.sh <poc>\"" >> /root/.bashrc'
