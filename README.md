# pyveth - Docker Plugin for veth networks

Simple network plugin for Docker Engine that can replace macvlan
in container-as-VM scenarios, allowing host-to-container communication
(see https://github.com/docker/for-linux/issues/931 for bug details).

It should be a drop-in replacement for macvlan module.

![Build status](https://github.com/jacekkow/docker-plugin-pyveth/workflows/Release/badge.svg)

## Installation

Plugin is packaged as [Docker Engine-managed plugin](https://docs.docker.com/engine/extend/).
Check out [plugin page on Docker Hub](https://hub.docker.com/p/jacekkow/pyveth).

To install it simply run:

```bash
docker plugin install jacekkow/pyveth
```

## Usage

After installation you can use driver in newly-created networks:

```bash
docker network create --driver jacekkow/pyveth:latest new-network
```

By default it will simply create a pair of veth interfaces for each container.
One will be pushed inside the container and another will remain on host
(without any IP assigned).

Plugin accepts optional `parent` parameter, which is a name of bridge
interface that the second interface should be added to:

```bash
docker network create --driver jacekkow/pyveth:latest --opt parent=br0 new-network
```

This way host interface will be automatically attached to the specified bridge.

## Manual packaging

In order to test this module in development environment, you can build it
by following [Docker Engine documentation](https://docs.docker.com/engine/extend/#developing-a-plugin).

You can also use `package.sh` helper script which will perform
all the steps (including installation) automatically.
