# An NSO Nano service as a CI/CD pipeline

Nano services are a great feature to help you build a solid CI/CD pipeline with
no or low code on top of Cisco NSO orchestration platform. Defined in YANG
format, Nano services can be easily extended with small Python modules for
specific tasks. This example service, named `nano`, demonstrates a pipeline with
manual work approval, pre and post-testing, SLA tracking, Webex notifications,
XML and Python template-based device configurations.

For a description of a use case and a typical workflow, please check
[USECASE.md](USECASE.md).

**Provided code and configurations are intended for educational purposes only.**

## How to run this example

This repo represents a folder where you should instantiate a local NSO CDB with
the `ncs-setup` command. Combining with NSO Local Install, it will create an
environment to run and develop the example.

You need to complete a few steps:

1. Install NSO in Local Install mode
1. Clone the repo
1. Create a Python virtual environment and install all dependencies
1. Configure environment variables
1. Compile packages and start NSO

The service is tested against NSO 5.5.2.6 for macOS (Intel), NEDs:
cisco-ios-cli-3.8, Python 3.9.5.

### Install NSO

You need to have an NSO installed in Local Install mode to run this example with
mostly no modifications. For detailed instructions on how to get a copy of NSO
and do a local install, please check
[DevNet documentation](https://developer.cisco.com/docs/nso/#!getting-and-installing-nso)
and
[NSO Installation Guide](https://developer.cisco.com/docs/nso/guides/#!nso-local-install).

After a successful installation, please make sure you source the `ncsrc` file
from a local install folder, for example:

```sh
$ source /Users/username/nso/5.5.2.6/ncsrc

$ ncs --version
5.5.2.6

$ echo $PYTHONPATH
/Users/username/nso/5.5.2.6/src/ncs/pyapi

$ echo $NCS_DIR
/Users/username/nso/5.5.2.6
```

`/Users/username/nso/5.5.2.6/` is a NSO local install folder.

### Clone the repo

```sh
git clone https://githib.com/andreygrechin/nano
cd nano
```

### Create a Python virtual environment and install all dependencies

Check a version of Python; we need at least 3.9.

```sh
$ python3 --version
Python 3.9.5
```

To install dependencies, run:

```sh
$ python3 -m venv .venv

$ source .venv/bin/activate

$ which python3
/Users/username/repos/nso/nano/.venv/bin/python3

$ pip3 install -r requirements.txt

```

For linting and other development activities, you may add additional
requirements from `requirements-dev.txt`.

To check if NSO Python API is available, try this:

```sh
python3 -c "import ncs"
```

### Configure environment variables

The example uses Webex API to send notifications to an approver and report
Service Progress Monitoring (aka SLA of service instances) status. You can find
instructions on creating a Webex bot and getting all the required credentials
[here](https://developer.webex.com/docs/bots).

You need to add obtained credentials via environment variables. Alternatively,
you may specify them as a part of a configuration of the service.

```sh
export WEBEX_BOT_TOKEN="YOUR-WEBEX-BOT-TOKEN-HERE"
export WEBEX_ROOM_ID="YOUR-WEBEX-ROOM-ID-HERE"
```

To check credentials, run:

```sh
curl --location --request POST 'https://api.ciscospark.com/v1/messages' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer ${WEBEX_BOT_TOKEN}" \
--data-raw '{
  "roomId" : "'"${WEBEX_ROOM_ID}"'",
  "text" : "my test msg"
}'
```

### Compile packages and start NSO

`make` or `make all` will clean up underlying folders, compile YANG models, set
up required simulated devices, create an empty local NSO CDB, create local NSO
files in the repo folder, load configuration files, and start NSO.

To run CLI or WebUI, use `make cli` or `make webui`. A default password for the
user `admin` is `admin`.

After entering CLI, check if all packages are successfully loaded.

```text
admin@ncs# show packages package oper-status
                                                                                                      PACKAGE
                        PROGRAM                                                                       META     FILE
                        CODE     JAVA           PYTHON         BAD NCS  PACKAGE  PACKAGE  CIRCULAR    DATA     LOAD   ERROR
NAME                UP  ERROR    UNINITIALIZED  UNINITIALIZED  VERSION  NAME     VERSION  DEPENDENCY  ERROR    ERROR  INFO
-----------------------------------------------------------------------------------------------------------------------------
cisco-ios-cli-3.8   X   -        -              -              -        -        -        -           -        -      -
example-nano-0.1.0  X   -        -              -              -        -        -        -           -        -      -

admin@ncs#
```

For a description of a use case and a typical workflow, please check
[USECASE.md](USECASE.md).

## Clean up

After finishing your session, you may stop the NSO process and clean up folders
with `make clean` or just `make stop` to stop NSO.

## Testing the NSO service

To optionally run `lux` tests, you need to install it with all dependencies.
Check [the documentation](https://github.com/hawk/lux/blob/master/INSTALL.md)
for details.

An example of a [lux](https://github.com/hawk/lux) script is included in the
repo. It's pretty simple, but it does the job. Check it
[here](tests/internal/lux/service/run.lux). You may run it from scratch with the
`make all nsotest` command.

## Getting help

If you have questions, concerns, bug reports, etc., please create an issue
against this repository.

## Getting involved

For contribution guidelines, please check
[CONTRIBUTING.md](.github/CONTRIBUTING.md).

## References

1. [NetDevOps intro from Julio Gomez](https://github.com/juliogomez/netdevops),
   based on NSO, Ansible and GitLab CI/CD pipelines.
1. [Nano Services – Another approach for Reactive Fastmap (RFM) services](https://www.youtube.com/watch?v=NJhOBf8J-J8), [demo](https://www.youtube.com/watch?v=DMHOlInbfe0).
1. [Building a Service, from Template to Reactive Fast Map to Nano services](https://www.youtube.com/watch?v=OIzBhzdAC9M).
