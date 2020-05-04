#!/usr/bin/env python3

import logging

import docker_plugin_api.Plugin
import flask

app = flask.Flask('pyveth')
app.logger.setLevel(logging.DEBUG)

app.register_blueprint(docker_plugin_api.Plugin.app)

import lib.NetworkDriver
docker_plugin_api.Plugin.functions.append('NetworkDriver')
app.register_blueprint(lib.NetworkDriver.app)

if __name__ == '__main__':
    app.run(debug=True)
