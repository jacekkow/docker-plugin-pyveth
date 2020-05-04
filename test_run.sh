#!/bin/sh

set -e

for file in integration/*.json; do
	method=${file#*-}
	method=${method%%-*}
	echo ${method}

	curl -X POST --data "@${file}" "http://127.0.0.1:5000/NetworkDriver.${method}"
done
