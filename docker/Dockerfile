FROM debian:11
ARG user=lsst
RUN apt-get update && apt-get install -y \
    python3-pip \
    git
RUN useradd --create-home $user
USER $user
WORKDIR /home/$user
RUN git clone https://github.com/lsst-ts/ts_bokeh_apps -b

CMD "/bin/bash"