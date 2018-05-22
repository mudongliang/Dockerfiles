#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
from ConfigParser import SafeConfigParser
import os

config_file = "config.ini"

dockerfile = "Dockerfile"

def add_maintainer(fd):
    fd.write("MAINTAINER \"Dongliang Mu\" <mudongliangabcd@gmail.com>")
    fd.write("\n")
    
def add_system(fd, os, os_tag):
    if not os_tag:
        fd.write("FROM " + os)
    else:
        fd.write("FROM " + os + ":" + os_tag)
    fd.write("\n")

def add_update_by_sys(fd, linux):
    if (linux.lower() == "debian" or linux.lower() == "ubuntu" or 
        linux.lower() == "kali"):
        fd.write("RUN apt-get -y update && apt-get -y upgrade")
        fd.write("\n")
    else:
        print(linux + "is not supported for now")
        # yum -y update

def install_dep_by_sys(fd, linux, package):
    if (linux.lower() == "debian" or linux.lower() == "ubuntu" or 
        linux.lower() == "kali"):
        fd.write("RUN apt-get -y install build-essential " + package)
        fd.write("\n")
    else:
        print(linux + "is not supported for now")
        # yum install package

def switch_workspace(fd, workspace):
    fd.write("WORKDIR " + workspace)
    fd.write("\n")

def install_program(fd, prog_link, prog_dir, compile_method, prog_install):
    fd.write("RUN wget " + prog_link + "; \\")
    fd.write("\n")

    prog_name = os.path.basename(prog_link)

    if prog_name.endswith("tar.gz"):
        fd.write("tar -xvf " + prog_name + "; \\")
        fd.write("\n")
    elif prog_name.endswith("zip"):
        fd.write("unzip " + prog_name + "; \\")
        fd.write("\n")
    else :
        print(prog_name, "has unsupported compression format")

    fd.write("cd " + prog_dir + "; \\")
    fd.write("\n")

    if compile_method == "make":
        fd.write("make; \\")
        fd.write("\n")
    else :
        print(compile_method, "is not supported")

    if prog_install:
        fd.write("make install;")
    else :
        fd.write("clear;")

    fd.write("\n")

def deploy_poc(fd, poc_link, deploy):
    fd.write("RUN wget " + poc_link + "; \\")
    fd.write("\n")
    fd.write(deploy)
    fd.write("\n")

def add_trigger_method(fd, trigger):
    fd.write("CMD " + trigger)
    fd.write("\n")

def clean_cache_by_sys(fd, linux):
    if (linux.lower() == "debian" or linux.lower() == "ubuntu" or 
        linux.lower() == "kali"):
        fd.write("RUN rm -rf /var/lib/apt/lists")
        fd.write("\n")
    else:
        print(linux + "is not supported for now")
        # yum clean all


def main():
    print("Read config file and generate one Dockerfile")

    clean_cache = False

    with open(dockerfile, "w") as fd:
        if not os.path.exists(config_file):
            print("No configuration file")
                 
        config = SafeConfigParser()
        config.read(config_file)

        sys_linux = config.get("Environment", "sys") 
        sys_tag = config.get("Environment", "sys_tag") 
        update = config.getboolean("Environment", "update") 
        dep = config.get("Environment", "dependencies") 
        workspace = config.get("Environment", "workspace")

        add_system(fd, sys_linux, sys_tag)
        add_maintainer(fd)

        if update:
            add_update_by_sys(fd, sys_linux)
            clean_cache = True

        if dep:
            install_dep_by_sys(fd, sys_linux, dep)

        switch_workspace(fd, workspace)

        prog_link = config.get("Source Code", "link")
        prog_dir = config.get("Source Code", "directory")
        compile_method = config.get("Source Code", "compilation")
        prog_install = config.getboolean("Source Code", "install")
        binary_pos = config.get("Source Code", "vul_binary_pos")

        install_program(fd, prog_link, prog_dir, compile_method, prog_install)

        poc_link = config.get("PoC", "link")
        deploy = config.get("PoC", "deploy")
        trigger = config.get("PoC", "trigger")
         
        deploy_poc(fd, poc_link, deploy)

        if clean_cache:
            clean_cache_by_sys(fd, sys_linux)
    
        add_trigger_method(fd, trigger)

    print("Finish Dockerfile generation")

if __name__ == '__main__':
    main()
