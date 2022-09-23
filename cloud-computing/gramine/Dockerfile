# FIXME: use tagged version when released
FROM docker-regis.iex.ec/iexec-graphene-base:27d9321a

RUN  apt-get install -y python3

### install needed python3 dependencies
RUN pip3 install pyfiglet

ARG SOURCE_DIR=src
ARG GRAMINE_DIR=gramine

# get the code of app to /workplace/app
COPY $SOURCE_DIR/app.py /workplace/app

# set the main function for python and node app, no need for binnary app
RUN sed -i "s#MAIN_FUNC=#MAIN_FUNC=/workplace/app/app.py#" /apploader.sh

WORKDIR /workplace/app

# Copy the manifest to use from within the base image
# or create your own
RUN mv /common-manifests/python.entrypoint.manifest /entrypoint.manifest \
    && rm -r /common-manifests

# Finalize app (finalize manifest and sign app)
RUN /finalize-app.sh
