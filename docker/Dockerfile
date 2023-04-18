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
USER $USER
WORKDIR /home/$USER
SHELL ["/bin/bash", "-c"]
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

#RUN git clone https://github.com/lsst-ts/ts_bokeh_apps -b application_creation_improvement

WORKDIR /home/$USER/ts_bokeh_apps/
RUN mkdir ts_bokeh_apps
COPY  ts_bokeh_apps/ .
RUN pip install -r requirements.txt
RUN python3 setup.py install

WORKDIR /home/$USER

COPY "ts_bokeh_apps/docker/entrypoint.sh" "entrypoint.sh"
COPY "ts_bokeh_apps/docker/configuration.yml" "configuration.yml"

ENV CUSTOM_USER=$USER

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]