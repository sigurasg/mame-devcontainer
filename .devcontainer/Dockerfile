FROM ubuntu:22.04

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV OVERRIDE_CC=clang
ENV OVERRIDE_CXX=clang++
ENV ARCHOPTS=
ENV SUBTARGET=mame
ENV TOOLS=1

RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash && \
    apt-get update && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y install \
        sudo \
        git \
        gcc \
        g++ \
        clang \
        lldb \
        libfontconfig-dev \
        libsdl2-dev \
        libsdl2-ttf-dev \
        libasound2-dev \
        libxinerama-dev \
        libxi-dev \
        qtcreator \
        qtbase5-dev \
        qtbase5-dev-tools && \
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME
