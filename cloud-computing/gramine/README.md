## How to run demo with Gramine

1. Start a SPS container:
```shell
docker run -d -v /opt/multiple/sessions:/graphene/workplace/sessions -p 8080:8080 -p 4433:4433 -e SPS_USERNAME=admin -e SPS_PASSWORD=admin --name iexec-sps iexechub/iexec-sps:bf3bb00-dev
```


2. Build your app (from `cloud-computing` directory) :
```shell
docker build -t tee-gramine-python-hello-world:latest -f gramine/Dockerfile  .
```
Please note the `measurement` value.


3. To add a session to the SPS, run the following after having filled both env var:
```shell
SESSION_ID=<defined your custom session id>
MEASUREMENT=<set previous retrieved measurement>

curl --location --request POST 'localhost:8080/api/session/' \
--header 'Authorization: Basic YWRtaW46YWRtaW4=' \
--header 'Content-Type: application/json' \
--data-raw '{
  "session": "'${SESSION_ID}'",
  "enclaves": [
    {
      "name": "app",
      "mrenclave": "'${MEASUREMENT}'",
      "command": "/apploader.sh",
      "environment": {
        "IEXEC_IN": "/workplace/iexec_in",
        "IEXEC_OUT": "/workplace/iexec_out",
        "IEXEC_DATASET_FILENAME": "file.txt",
        "IEXEC_INPUT_FILES_NUMBER": "1",
        "IEXEC_INPUT_FILE_NAME_1": "file.txt",
        "IEXEC_TASK_ID": "TASK_ID",
        "IEXEC_APP_DEVELOPER_SECRET": "App developer secret",
        "IEXEC_REQUESTER_SECRET_1": "Requester secret 1",
        "IEXEC_REQUESTER_SECRET_2": "Requester secret 2",
        "IEXEC_REQUESTER_SECRET_3": "Requester secret 3"
      }
    }
  ]
}'
```

4. Run the app:
```shell
docker run --device=/dev/sgx/enclave -v /iexec_in:/workplace/iexec_in -v /iexec_out:/workplace/iexec_out -v /var/run/aesmd/aesm.socket:/var/run/aesmd/aesm.socket -v $PWD/encryptedData:/workplace/encryptedData --net=host -e session=${SESSION_ID} -e sps=localhost:4433  tee-gramine-python-hello-world:latest
```


### Troubleshooting:


#### Dataset and input files are not correctly read
Check they are correctly added as `sgx.allowed_files` in `entrypoint.manifest`.