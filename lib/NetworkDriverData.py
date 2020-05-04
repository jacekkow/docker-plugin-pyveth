import shelve
from typing import Dict

from docker_plugin_api.NetworkDriverEntities import NetworkCreateEntity, EndpointCreateEntity


networks_store = shelve.open('networks', writeback=True)
networks: Dict[str, NetworkCreateEntity] = networks_store


def networks_sync():
    networks_store.sync()


endpoints: Dict[str, EndpointCreateEntity] = {}
