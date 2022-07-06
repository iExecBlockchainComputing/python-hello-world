FROM docker.io/iexechub/iexec-graphene-base:f810d8c-dev

RUN  apt-get install -y python3

### install needed python3 dependencies
RUN pip3 install pyfiglet

ARG SOURCE_DIR=src
ARG GRAMINE_DIR=gramine

# get the code of pythonexample to /workplace/app
COPY $SOURCE_DIR/app.py /workplace/app

# set the main function for python and node app, no need for binnary app
RUN sed -i "s#MAIN_FUNC=#MAIN_FUNC=/workplace/app/app.py#" /apploader.sh

WORKDIR /workplace/app

# finalize manifest
COPY $GRAMINE_DIR/entrypoint.manifest /
RUN python3 -B /var/tmp/finalize_manifest.py

# Dummy key

# sign image
COPY $GRAMINE_DIR/signer-key.pem /signer-key.pem
RUN /graphene/python/graphene-sgx-sign \
        -libpal /graphene/Runtime/libpal-Linux-SGX.so \
        -key /signer-key.pem \
        -manifest /entrypoint.manifest \
        -output /entrypoint.manifest.sgx

RUN rm -rf /var/tmp/* \
    && rm -rf /graphene/python/graphene-sgx-sign /graphene/python/graphenelibos/sgx_sign.py \
    && rm -rf /signer-key.pem
