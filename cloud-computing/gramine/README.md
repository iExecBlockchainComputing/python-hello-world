## How to run demo with Gramine on localhost

1. Start a SPS container:
```shell
SPS_VERSION=<set SPS version here>
docker run -d \
  -v /opt/multiple/sessions:/graphene/workplace/sessions \
  -v /opt/secret-prov/certs/:/graphene/workplace/certs \
  -p 8080:8080 -p 4433:4433 \
  -e SPS_USERNAME=admin -e SPS_PASSWORD=admin \
  --name iexec-sps \
  iexechub/iexec-sps:${SPS_VERSION}
```


2. Build your app (from `cloud-computing` directory) :
```shell
docker build -t tee-gramine-python-hello-world:latest -f gramine/Dockerfile  .
```
Please note the `measurement` value.


3. To add a session to the SPS, run the following after having filled both env var:
```shell
SESSION_ID=<define your custom session id>
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
        "IEXEC_IN": "/iexec_in",
        "IEXEC_OUT": "/iexec_out",
        "IEXEC_DATASET_FILENAME": "file.txt",
        "IEXEC_INPUT_FILES_NUMBER": "1",
        "IEXEC_INPUT_FILE_NAME_1": "file.txt",
        "IEXEC_TASK_ID": "TASK_ID",
        "IEXEC_APP_DEVELOPER_SECRET": "App developer secret",
        "IEXEC_REQUESTER_SECRET_1": "Requester secret 1",
        "IEXEC_REQUESTER_SECRET_2": "Requester secret 2",
        "IEXEC_REQUESTER_SECRET_3": "Requester secret 3"
      },
      "volumes": [
      ]
    }
  ]
}'
```


4. Run the app:
```shell
docker run \
  --device=/dev/sgx/enclave \
  -v /iexec_in:/iexec_in -v /tmp/iexec_out:/iexec_out \
  -v /var/run/aesmd/aesm.socket:/var/run/aesmd/aesm.socket \
  -v $PWD/encryptedData:/workplace/encryptedData \
  -v /opt/secret-prov/certs/:/graphene/attestation/certs/ \
  --net=host \
  -e session=${SESSION_ID} -e sps=localhost:4433 \
  tee-gramine-python-hello-world:latest
```


### Troubleshooting:

#### "Get keys failed"
When the app can't communicate with the SPS, you can encounter some numeric error codes, in the following format:
```
[error] connect to kms failed, kms_endpoint is iexec-sps:4433, cert_path is /graphene/attestation/certs/test-ca-sha256.crt
[error] get keys failed, return -[ERROR_CODE] 
```

Depending on the error code, the issue is the following:

| Error code |       Error       |                                                         Solution                                                          |
|:----------:|:-----------------:|:-------------------------------------------------------------------------------------------------------------------------:|
|    111     |  Can't reach SPS  |                                       Check SPS IP is correct in app configuration.                                       |
|    9984    | Certificate error | Check both app & SPS share a valid certificate. Regenerate it if needed, providing SPS IP as `Common Name` when prompted. |


#### Dataset and input files are not correctly read
Check they are correctly added as `sgx.allowed_files` in `entrypoint.manifest`.
