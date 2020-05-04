#!/bin/sh

set -e

NAME=${NAME:-jacekkow/pyveth}
VERSION=${VERSION:-latest}

PLUGIN="${NAME}:${VERSION}"

docker plugin install jacekkow/pyipam:latest || true

docker network create \
  --internal \
  --driver "${PLUGIN}" \
  --ipam-driver jacekkow/pyipam:latest \
  --ipv6 \
  --subnet 192.168.255.0/24 \
  --ip-range 192.168.255.128/26 \
  --gateway 192.168.255.254 \
  --subnet 2001:db8::/32 \
  --ip-range 2001:db8:aaaa:bbbb::/64 \
  --gateway 2001:db8:ffff:ffff:ffff:ffff:ffff:ffff \
  test1

ADDRESSES=$(docker run --rm --network test1 \
  debian \
  /bin/ip addr show
)
echo "${ADDRESSES}" | grep 192.168.255.129/24
echo "${ADDRESSES}" | grep 2001:db8:aaaa:bbbb::1/32


ADDRESSES=$(docker run --rm --network test1 \
  --ip 192.168.255.25 --ip6 2001:db8:dddd:eeee:ffff:1:2:3 \
  debian \
  /bin/ip addr show
)
echo "${ADDRESSES}" | grep 192.168.255.25/24
echo "${ADDRESSES}" | grep 2001:db8:dddd:eeee:ffff:1:2:3/32

docker network rm test1


docker network create \
  --internal \
  --driver "${PLUGIN}" \
  --ipam-driver jacekkow/pyipam:latest \
  --ipv6 \
  --subnet 192.168.255.0/24 \
  --gateway 192.168.255.254 \
  --subnet 2001:db8::/32 \
  --gateway 2001:db8:ffff:ffff:ffff:ffff:ffff:ffff \
  test2

ROUTES=$(docker run --rm --network test2 \
  debian \
  /bin/ip route show
)
echo "${ROUTES}" | grep 192.168.255.254

ROUTES=$(docker run --rm --network test2 \
  debian \
  /bin/ip -6 route show
)
echo "${ROUTES}" | grep 2001:db8:ffff:ffff:ffff:ffff:ffff:ffff

docker network rm test2
