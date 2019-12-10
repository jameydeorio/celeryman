# celeryman

The celeryman service [tell us what this service will do, don't be shy]

## Quickstart

celeryman is based on the [microservice chassis](https://github.com/oreillymedia/chassis).
For more information about the chassis and its available commands, please
consult the [chassis documentation](http://devdocs.platform-dev.gcp.oreilly.com/chassis/).

If you've never logged into our Docker registry, you can configure your Docker
daemon to use your Google credentials:

```
$ gcloud auth configure-docker
```

(For more information on setting up `gcloud`, consult [our guide](http://devdocs.platform-dev.gcp.oreilly.com/cloud/gke/)).

If you've never set up a `~/.chassis/credentials.json` file, you should run the following commands:
```
$ docker-compose build --pull
$ docker-compose run --rm manage credentials
```

When you first clone the repository, start it up with:

```
$ docker-compose build --pull
$ docker-compose up -d database
$ docker-compose run --rm tests
$ docker-compose up
```

Your service will be running on port  at the IP your Docker is
running.  This will be http://localhost: on Linux or Docker for
Mac, or at the address returned by `docker-machine ip default` if you're using
docker-machine.
