FROM debian:11
ARG user=lsst
ENV VIRTUAL_ENV=/home/$user/venv

EXPOSE 5056
EXPOSE 5057

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    git

RUN useradd --create-home $user
USER $user
WORKDIR /home/$user
SHELL ["/bin/bash", "-c"]
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN git clone https://github.com/lsst-ts/ts_bokeh_apps -b application_creation_improvement
WORKDIR /home/$user/ts_bokeh_apps/
RUN pip install -r requirements.txt
RUN python3 setup.py install

WORKDIR /home/$user
COPY "entrypoint.sh" "entrypoint.sh"
COPY "configuration.yml" "configuration.yml"
ENTRYPOINT ["/bin/bash", "entrypoint.sh", "/home/$user/configuration1.yml"]