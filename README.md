chaski-services-email
---------------------

Requirements
------------
* Docker
* Cmake

Help
----
* make
* make help

Commands
--------
```console
Target           Help                                                        Usage
------           ----                                                        -----
build.image       Build image for development                                make build.image
delete            Eliminating project deployment                             make delete
deploy            Deploying project                                          make deploy
run.local         Locally executing the project                              make run.local
ssh               Connect to the container by ssh                            make ssh
```

How to use
----------
```console
Endpoint: /messages
Method: POST
Payload:
        {
            "from": {
                "name": "Team Chaski Services Email",
                "email": "team@chaski.com"
            },
            "to": [
                {
                    "name": "John Montero Chunga",
                    "email": "jmonteroc@chaski.com"
                }
            ],
            "subject": "Welcome to Team Chaski Services Email",
            "metadata": {
                "Message": "Hello John, Now you are part of Team Chaski Services Email."
            }
        }
```