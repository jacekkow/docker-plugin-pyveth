from typing import Dict

from docker_plugin_api.NetworkDriverEntities import NetworkCreateEntity, EndpointCreateEntity

networks : Dict[str, NetworkCreateEntity] = {}
endpoints : Dict[str, EndpointCreateEntity] = {}
