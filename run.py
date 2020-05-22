#!/usr/bin/env python3

import logging
import os

import docker_plugin_api.Plugin
import flask
import waitress

app = flask.Flask('pyveth')
app.logger.setLevel(logging.DEBUG)

app.register_blueprint(docker_plugin_api.Plugin.app)

import lib.NetworkDriver
docker_plugin_api.Plugin.functions.append('NetworkDriver')
app.register_blueprint(lib.NetworkDriver.app)

if __name__ == '__main__':
	if os.environ.get('ENVIRONMENT', 'dev') == 'dev':
		app.run(debug=True)
	else:
		waitress.serve(app, unix_socket='/run/docker/plugins/pyveth.sock', threads=1)
