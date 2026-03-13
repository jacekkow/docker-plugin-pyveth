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

## Options

To use options, add `--opt option=value` as an argument of `docker network create`:

```bash
docker network create --driver jacekkow/pyveth:latest --opt parent=br0 new-network
```

Available options:

`parent=brname`

Automatically attach host interface to the bridge interface `brname`.

`nogw=1`

Disable assignment of gateway IP.

`nogw4=1`

Disable assignment of IPv4 gateway IP.

`nogw6=1`

Disable assignment of IPv6 gateway IP.

`gw4=IP`

`gw6=IP`

Forces assignment of a specified gateway (only if one is not provided by the IPAM module)
when creating the interface. Useful for [pyipam](https://github.com/jacekkow/docker-plugin-pyipam)
with `ptp=1` option and `nogw=1`/`nogw4=1`/`nogw6=1` here.

Using these would add routes like:
```
default via IP dev eth0
IP dev eth0 scope link
```

## Container creation options

To use these options add `--network name=network_name,driver-opt=option=value,driver-opt=option=value`
to the `docker run` invocation:

```bash
docker run -i -t --rm --network name=test,ip=192.168.1.1,driver-opt=gw4=192.168.0.1,driver-opt=gw6=fe80:: alpine
```

Available options:

`gw4=IP`

`gw6=IP`

Overrides network-level gw4/gw6 options.

## Manual packaging

In order to test this module in development environment, you can build it
by following [Docker Engine documentation](https://docs.docker.com/engine/extend/#developing-a-plugin).

You can also use `package.sh` helper script which will perform
all the steps (including installation) automatically.
