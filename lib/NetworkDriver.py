import ipaddress
import random

import flask
import pyroute2
from docker_plugin_api.NetworkDriverEntities import *
from docker_plugin_api.Plugin import Blueprint, InputValidationException

from .NetworkDriverData import *

app = Blueprint('NetworkDriver', __name__)


def genid(size=8, chars='0123456789abcdef'):
    return ''.join([random.choice(chars) for _ in range(size)])


def create_interface(endpoint, network) -> str:
    ifname0 = 'veth{}'.format(genid())
    ifname1 = 'veth{}'.format(genid())

    with pyroute2.IPRoute() as ip:
        ip.link('add', ifname=ifname0, peer=ifname1, kind='veth')
        idx = ip.link_lookup(ifname=ifname0)[0]
        if endpoint.Interface.MacAddress:
            ip.link('set', index=idx, address=endpoint.Interface.MacAddress)
        ip.link('set', index=idx, state='up')
        if endpoint.Interface.Address:
            addr = ipaddress.ip_interface(endpoint.Interface.Address)
            ip.addr('add', index=idx, address=addr.ip.compressed, mask=addr.network.prefixlen)
        if endpoint.Interface.AddressIPv6:
            addr = ipaddress.ip_interface(endpoint.Interface.AddressIPv6)
            ip.addr('add', index=idx, address=addr.ip.compressed, mask=addr.network.prefixlen)
        endpoint.Interface.Name = ifname0

        idx = ip.link_lookup(ifname=ifname1)[0]
        ip.link('set', index=idx, state='up')
        if 'parent' in network.Options:
            id_parent = ip.link_lookup(ifname=network.Options['parent'])[0]
            print(ip.link("set", index=idx, master=id_parent))
        endpoint.Interface.Peer = ifname1

    return ifname0


@app.route('/NetworkDriver.GetCapabilities', methods=['POST'])
def GetCapabilities():
    return {
        'Scope': 'local',
        'ConnectivityScope': 'global',
    }


@app.route('/NetworkDriver.CreateNetwork', methods=['POST'])
def CreateNetwork():
    network = NetworkCreateEntity(**flask.request.get_json(force=True))
    try:
        for option, value in network.Options['com.docker.network.generic'].items():
            if option not in network.Options:
                network.Options[option] = value
    except KeyError:
        pass
    networks[network.NetworkID] = network
    networks_sync()
    return {}


@app.route('/NetworkDriver.DeleteNetwork', methods=['POST'])
def DeleteNetwork():
    network = NetworkDeleteEntity(**flask.request.get_json(force=True))
    if network.NetworkID in networks:
        del networks[network.NetworkID]
        networks_sync()
    return {}


@app.route('/NetworkDriver.CreateEndpoint', methods=['POST'])
def CreateEndpoint():
    endpoint = EndpointCreateEntity(**flask.request.get_json(force=True))
    endpoints['{}-{}'.format(endpoint.NetworkID, endpoint.EndpointID)] = endpoint
    return {
        'Interface': {
        }
    }


@app.route('/NetworkDriver.EndpointOperInfo', methods=['POST'])
def EndpointOperInfo():
    endpoint = EndpointOperInfoEntity(**flask.request.get_json(force=True))
    return {
        'Value': {
        }
    }


@app.route('/NetworkDriver.DeleteEndpoint', methods=['POST'])
def DeleteEndpoint():
    entity = EndpointDeleteEntity(**flask.request.get_json(force=True))
    endpoint_id = '{}-{}'.format(entity.NetworkID, entity.EndpointID)
    if endpoint_id in endpoints:
        del endpoints['{}-{}'.format(entity.NetworkID, entity.EndpointID)]
    return {}


@app.route('/NetworkDriver.Join', methods=['POST'])
def Join():
    join = JoinEntity(**flask.request.get_json(force=True))
    network = networks[join.NetworkID]
    endpoint = endpoints['{}-{}'.format(join.NetworkID, join.EndpointID)]

    interface = create_interface(endpoint, network)

    gw4 = None
    for net4 in network.IPv4:
        try:
            gw4 = ipaddress.ip_interface(net4.Gateway)
            break
        except:
            pass
    gw6 = None
    for net6 in network.IPv6:
        try:
            gw6 = ipaddress.ip_interface(net6.Gateway)
            break
        except:
            pass

    result = {
        'InterfaceName': {
            'SrcName': interface,
            'DstPrefix': 'eth',
        },
    }
    if gw4 is not None:
        result['Gateway'] = gw4.ip.compressed
    if gw6 is not None:
        result['GatewayIPv6'] = gw6.ip.compressed
    return result


@app.route('/NetworkDriver.Leave', methods=['POST'])
def Leave():
    leave = LeaveEntity(**flask.request.get_json(force=True))
    return {}


@app.route('/NetworkDriver.DiscoverNew', methods=['POST'])
def DiscoverNew():
    entity = DiscoverNewEntity(**flask.request.get_json(force=True))
    return {}


@app.route('/NetworkDriver.DiscoverDelete', methods=['POST'])
def DiscoverDelete():
    entity = DiscoverDeleteEntity(**flask.request.get_json(force=True))
    return {}


@app.route('/NetworkDriver.ProgramExternalConnectivity', methods=['POST'])
def ProgramExternalConnectivity():
    entity = ProgramExternalConnectivityEntity(**flask.request.get_json(force=True))
    return {}


@app.route('/NetworkDriver.RevokeExternalConnectivity', methods=['POST'])
def RevokeExternalConnectivity():
    entity = RevokeExternalConnectivityEntity(**flask.request.get_json(force=True))
    return {}
