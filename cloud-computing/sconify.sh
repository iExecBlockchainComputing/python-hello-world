#!/bin/bash
cd $(dirname $0)

IMG_FROM=python-hello-world
IMG_TO=tee-python-hello-world:debug

ARGS=$(sed -e "s'\${IMG_FROM}'${IMG_FROM}'" -e "s'\${IMG_TO}'${IMG_TO}'" sconify.args)
echo $ARGS

docker run -it --rm \
            -v /var/run/docker.sock:/var/run/docker.sock \
            registry.scontain.com:5050/scone-production/iexec-sconify-image:5.3.9 \
            sconify_iexec $ARGS
