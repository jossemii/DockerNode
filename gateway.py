from posix import environ
from typing import Generator
import celaut_pb2 as celaut
import build, utils
from compile import REGISTRY, HYCACHE
import logger as l
from verify import SHA3_256_ID, check_service, get_service_hex_main_hash
import subprocess, os, threading
import grpc, gateway_pb2, gateway_pb2_grpc
from concurrent import futures
from grpc_reflection.v1alpha import reflection
import pymongo, json
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse
import docker as docker_lib
import netifaces as ni

GET_ENV = lambda env, default: int(os.environ.get(env)) if env in os.environ.keys() else default
DOCKER_CLIENT = lambda: docker_lib.from_env()
DOCKER_NETWORK = 'docker0'
LOCAL_NETWORK = 'lo'
GATEWAY_PORT = GET_ENV(env = 'GATEWAY_PORT', default = 8080)
SELF_RATE = GET_ENV(env = 'COMPUTE_POWER_RATE', default = 1)
COST_OF_BUILD = GET_ENV(env = 'COST_OF_BUILD', default = 0)

def generate_gateway_instance(network: str) -> gateway_pb2.Instance:
    instance = celaut.Instance()

    uri = celaut.Instance.Uri()
    try:
        uri.ip = ni.ifaddresses(network)[ni.AF_INET][0]['addr']
    except ValueError as e:
        l.LOGGER('You must specify a valid interface name ' + network)
        raise Exception('Error generating gateway instance --> ' + str(e))
    uri.port = GATEWAY_PORT
    uri_slot = celaut.Instance.Uri_Slot()
    uri_slot.internal_port = GATEWAY_PORT
    uri_slot.uri.append(uri)
    instance.uri_slot.append(uri_slot)
    
    slot = celaut.Service.Api.Slot()
    slot.port = GATEWAY_PORT
    instance.api.slot.append(slot)
    return gateway_pb2.Instance(
        instance = instance,
        instance_meta = celaut.Any.Metadata(
            hashtag = celaut.Any.Metadata.HashTag(
                attr_hashtag = [
                    celaut.Any.Metadata.HashTag.AttrHashTag(
                        key = 1, # Api attr.
                        value = [
                            celaut.Any.Metadata.HashTag(
                                attr_hashtag = [
                                    celaut.Any.Metadata.HashTag.AttrHashTag(
                                        key = 2, # Slot attr.
                                        value = [
                                            celaut.Any.Metadata.HashTag(
                                                attr_hashtag = [
                                                    celaut.Any.Metadata.HashTag.AttrHashTag(
                                                        key = 2, # Transport Protocol attr.
                                                        value = [
                                                            celaut.Any.Metadata.HashTag(
                                                                tag = ['http2', 'grpc']
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        )
    )

# Insert the instance if it does not exists.
def insert_instance_on_mongo(instance: celaut.Instance):
    parsed_instance = json.loads(MessageToJson(instance))
    pymongo.MongoClient(
        "mongodb://localhost:27017/"
    )["mongo"]["peerInstances"].update_one(
        filter = parsed_instance,
        update={'$setOnInsert': parsed_instance},
        upsert = True
    )

cache_lock = threading.Lock()
cache = {}  # ip:[dependencies]

# internal token -> str( peer_ip##container_ip##container_id )   peer_ip se refiere a la direccion del servicio padre (que puede ser interno o no).
# external token -> str( peer_ip##node_ip:node_port##his_token )

# En caso de mandarle la tarea a otro nodo:
#   En cache se añadirá el servicio como dependencia del nodo elegido,
#   en vez de usar la ip del servicio se pone el token que nos dió ese servicio,
#   nosotros a nuestro servicio solicitante le daremos un token con el formato node_ip##his_token.


def set_on_cache( father_ip : str, id_or_token: str, ip_or_uri: str):
    

    # En caso de ser un nodo externo:
    if not father_ip in cache:
        cache_lock.acquire()
        cache.update({father_ip: []})
        cache_lock.release()
        # Si peer_ip es un servicio del nodo ya
        # debería estar en el registro.


    # Añade el nuevo servicio como dependencia.
    cache[father_ip].append(ip_or_uri + '##' + id_or_token)
    l.LOGGER('Set on cache ' + ip_or_uri + '##' + id_or_token + ' as dependency of ' + father_ip )


def purgue_internal(father_ip, container_id, container_ip):
    try:
        DOCKER_CLIENT().containers.get(container_id).remove(force=True)
    except docker_lib.errors.APIError as e:
        l.LOGGER(str(e) + 'ERROR WITH DOCKER WHEN TRYING TO REMOVE THE CONTAINER ' + container_id)

    cache_lock.acquire()

    try:
        cache[father_ip].remove(container_ip + '##' + container_id)
    except ValueError as e:
        l.LOGGER(str(e) + str(cache[father_ip]) + ' trying to remove ' + container_ip + '##' + container_id)
    except KeyError as e:
        l.LOGGER(str(e) + father_ip + ' not in ' + str(cache.keys()))

    if container_ip in cache:
        for dependency in cache[container_ip]:
            # Si la dependencia esta en local.
            if utils.get_network_name(ip_or_uri = dependency.split('##')[0]) == DOCKER_NETWORK:
                purgue_internal(
                    father_ip = container_ip,
                    container_id = dependency.split('##')[1],
                    container_ip = dependency.split('##')[0]
                )
            # Si la dependencia se encuentra en otro nodo.
            else:
                purgue_external(
                    father_ip = father_ip,
                    node_uri = dependency.split('##')[0],
                    token = dependency[len(dependency.split('##')[0]) + 1:] # Por si el token comienza en # ...
                )

        try:
            l.LOGGER('Deleting the instance ' + container_id + ' from cache with ' + str(cache[container_ip]) + ' dependencies.')
            del cache[container_ip]
        except KeyError as e:
            l.LOGGER(str(e) + container_ip + ' not in ' + str(cache.keys()))

    cache_lock.release()


def purgue_external(father_ip, node_uri, token):
    # EN NODE_URI LLEGA UNA IP ¿?
    if len(node_uri.split(':')) < 2:
        l.LOGGER('Should be an uri not an ip. Something was wrong. The node uri is ' + node_uri)
        return None
    
    cache_lock.acquire()
    
    try:
        cache[father_ip].remove(node_uri + '##' + token)
    except ValueError as e:
        l.LOGGER(str(e) + str(cache[father_ip]) + ' trying to remove ' + node_uri + '##' + token)
    except KeyError as e:
        l.LOGGER(str(e) + father_ip + ' not in ' + str(cache.keys()))

    # Le manda al otro nodo que elimine esa instancia.
    try:
        gateway_pb2_grpc.Gateway(
            grpc.insecure_channel(node_uri)
        ).StopService(
             gateway_pb2.TokenMessage(
                token = token
            )
        )
    except grpc.RpcError as e:
        l.LOGGER('Error during remove a container on ' + node_uri + ' ' + str(e))

    cache_lock.release()


def set_config(container_id: str, config: celaut.Configuration):
    __config__ = celaut.ConfigurationFile()
    __config__.gateway.CopyFrom(generate_gateway_instance(network=DOCKER_NETWORK))
    __config__.config.CopyFrom(config)
    os.mkdir(HYCACHE + container_id)
    with open(HYCACHE + container_id + '/__config__', 'wb') as file:
        file.write(__config__.SerializeToString())
    while 1:
        try:
            subprocess.run(
                '/usr/bin/docker cp ' + HYCACHE + container_id + '/__config__ ' + container_id + ':/__config__',
                shell=True
            )
            break
        except subprocess.CalledProcessError as e:
            l.LOGGER(e.output)
    os.remove(HYCACHE + container_id + '/__config__')
    os.rmdir(HYCACHE + container_id)


def create_container(id: str, entrypoint: str, use_other_ports=None) -> docker_lib.models.containers.Container:
    try:
        return DOCKER_CLIENT().containers.create(
            image = id + '.docker', # https://github.com/moby/moby/issues/20972#issuecomment-193381422
            entrypoint = entrypoint,
            ports = use_other_ports
        )
    except docker_lib.errors.ImageNotFound:
        l.LOGGER('IMAGE WOULD BE IN DOCKER REGISTRY. BUT NOT FOUND.')     # LOS ERRORES DEBERIAN LANZAR ALGUN TIPO DE EXCEPCION QUE LLEGUE HASTA EL GRPC.
    except docker_lib.errors.APIError:
        l.LOGGER('DOCKER API ERROR ')

def build_cost(service: celaut.Service, metadata: celaut.Any.Metadata) -> int:
    try:
        # Coste de construcción si no se posee el contenedor del servicio.
        # Debe de tener en cuenta el coste de buscar el conedor por la red.
        return sum([
            COST_OF_BUILD * get_service_hex_main_hash(service = service, metadata = metadata) \
                in [img.tags[0].split('.')[0] for img in DOCKER_CLIENT().images.list()] is False,
            # Coste de obtener el contenedor ... #TODO
            ])
    except:
        pass
    return 0

def execution_cost(service: celaut.Service, metadata: celaut.Any.Metadata) -> int:
    return sum([
        len( DOCKER_CLIENT().containers.list() ),
        build_cost(service = service, metadata = metadata),
    ]) * SELF_RATE

def service_balancer(service: celaut.Service, metadata: celaut.Any.Metadata) -> dict: # sorted by cost, dict of celaut.Instances or None (meaning local execution) and cost.
    class PeerCostList:
        # Sorts the list from the element with the smallest weight to the element with the largest weight.
        
        def __init__(self) -> None:
            self.dict = {} # elem : weight
        
        def add_elem(self, weight: int, elem: celaut.Instance = None ) -> None:
            self.dict.update({elem: weight})
        
        def get(self) -> dict:
            return {k : v for k, v in sorted(self.dict.items(), key=lambda item: item[1])}

    try:
        peers = PeerCostList()
        peers.add_elem(
            weight = execution_cost(service = service, metadata = metadata)
        )

        for peer in list(pymongo.MongoClient(
                        "mongodb://localhost:27017/"
                    )["mongo"]["peerInstances"].find()):
            del peer['_id']
            peer_instance = Parse(
                text = json.dumps(peer),
                message = celaut.Instance(),
                ignore_unknown_fields = True
            )
            peer_uri = utils.get_grpc_uri(instance = peer_instance)
            try:
                peers.add_elem(
                    elem = peer_instance,
                    weight = gateway_pb2_grpc.GatewayStub(
                                grpc.insecure_channel(
                                    peer_uri.ip + ':' +  str(peer_uri.port)
                                )
                            ).GetServiceCost(
                                utils.service_extended(service = service, metadata = metadata)
                            ).cost
                )
            except: l.LOGGER('Error taking the cost.')

        return peers.get()

    except Exception as e:
        l.LOGGER('Error during balancer, ' + str(e))
        return None


def launch_service(
        service: celaut.Service, 
        metadata: celaut.Any.Metadata, 
        father_ip: str, 
        config: celaut.Configuration = None
        ) -> gateway_pb2.Instance:
    l.LOGGER('Go to launch a service. ' + str(service) + ' with metadata ' + str(metadata) + ' and config ' + str(config))
    if service == None: raise Exception("Service object can't be None")
    getting_container = False
    # Here it asks the balancer if it should assign the job to a peer.
    while True:
        for node_instance, cost in service_balancer(
            service = service,
            metadata = metadata
        ).items():
            l.LOGGER('Balancer select peer ' + str(node_instance) + ' with cost ' + str(cost))
            
            if node_instance:
                try:
                    node_uri = utils.get_grpc_uri(node_instance)
                    l.LOGGER('El servicio se lanza en el nodo con uri ' + str(node_uri))
                    service_instance =  gateway_pb2_grpc.GatewayStub(
                        grpc.insecure_channel(
                            node_uri.ip + ':' +  str(node_uri.port)
                        )
                    ).StartService(
                        utils.service_extended(
                            service = service, 
                            metadata = metadata,
                            config = config
                        )
                    )
                    set_on_cache(
                        father_ip = father_ip,
                        ip_or_uri =  node_uri.ip + ':' +  str(node_uri.port), # Add node_uri.
                        id_or_token = service_instance.token  # Add token.
                    )
                    service_instance.token = father_ip + '##' + node_uri.ip + '##' + service_instance.token
                    return service_instance
                except Exception as e:
                    l.LOGGER('Failed starting a service on peer, occurs the eror: ' + str(e))

            #  The node launches the service locally.
            l.LOGGER('El nodo lanza el servicio localmente.')
            try:
                build.build(
                        service = service, 
                        metadata = metadata,
                        get_it_outside = not getting_container
                    )  #  If the container is not built, build it.
            except:
                # If it does not have the container, it takes it from another node in the background and requests
                #  the instance from another node as well.
                getting_container = True
                continue

            instance = gateway_pb2.Instance()

            # If the request is made by a local service.
            if utils.get_network_name(father_ip) == DOCKER_NETWORK:
                container = create_container(
                    id = get_service_hex_main_hash(service = service, metadata = metadata),
                    entrypoint = service.container.entrypoint
                )

                set_config(container_id = container.id, config = config)

                # The container must be started after adding the configuration file and
                #  before requiring its IP address, since docker assigns it at startup.

                try:
                    container.start()
                except docker_lib.errors.APIError as e:
                    l.LOGGER('ERROR ON CONTAINER ' + str(container.id) + ' '+str(e)) # TODO LOS ERRORES DEBERIAN LANZAR ALGUN TIPO DE EXCEPCION QUE LLEGUE HASTA EL GRPC.

                # Reload this object from the server again and update attrs with the new data.
                container.reload()
                container_ip = container.attrs['NetworkSettings']['IPAddress']

                set_on_cache(
                    father_ip = father_ip,
                    id_or_token = container.id,
                    ip_or_uri = container_ip
                )

                for slot in service.api.slot:
                    uri_slot = celaut.Instance.Uri_Slot()
                    uri_slot.internal_port = slot.port

                    # Since it is internal, we know that it will only have one possible address per slot.
                    uri = celaut.Instance.Uri()
                    uri.ip = container_ip
                    uri.port = slot.port
                    uri_slot.uri.append(uri)

                    instance.instance.uri_slot.append(uri_slot)

            # Si hace la peticion un servicio de otro nodo.
            else:
                assigment_ports = {slot.port: utils.get_free_port() for slot in service.api.slot}

                container = create_container(
                    use_other_ports = assigment_ports,
                    id = get_service_hex_main_hash( service = service, metadata = metadata),
                    entrypoint = service.container.entrypoint
                )
                set_config(container_id = container.id, config = config)

                try:
                    container.start()
                except docker_lib.errors.APIError as e:
                    # TODO LOS ERRORES DEBERÍAN LANZAR UNA EXCEPCION QUE LLEGUE HASTA EL GRPC.
                    l.LOGGER('ERROR ON CONTAINER '+ str(container.id) + ' '+str(e)) 

                # Reload this object from the server again and update attrs with the new data.
                container.reload()

                set_on_cache(
                    father_ip = father_ip,
                    id_or_token = container.id,
                    ip_or_uri = container.attrs['NetworkSettings']['IPAddress']
                )

                for port in assigment_ports:
                    uri_slot = celaut.Instance.Uri_Slot()
                    uri_slot.internal_port = port

                    # for host_ip in host_ip_list:
                    uri = celaut.Instance.Uri()
                    uri.ip = utils.get_local_ip_from_network(
                        network = utils.get_network_name(ip_or_uri=father_ip)
                    )
                    uri.port = assigment_ports[port]
                    uri_slot.uri.append(uri)

                    instance.instance.uri_slot.append(uri_slot)

            instance.instance.api.CopyFrom(service.api)
            instance.token = father_ip + '##' + container.attrs['NetworkSettings']['IPAddress'] + '##' + container.id
            l.LOGGER('Thrown out a new instance by ' + father_ip + ' of the container_id ' + container.id)
            return instance


def save_service(service: celaut.Service, metadata = celaut.Any.Metadata):
    # If the service is not on the registry, save it.
    hash = get_service_hex_main_hash(service = service, metadata = metadata)
    if not os.path.isfile(REGISTRY+hash):
        with open(REGISTRY + hash, 'wb') as file:
            file.write(
                celaut.Any(
                    metadata = metadata,
                    value = service.SerializeToString()
                ).SerializeToString()
            )

def peers_iterator(ignore_network: str = None) -> Generator[celaut.Instance.Uri, None, None]:
    peers = list(pymongo.MongoClient(
                "mongodb://localhost:27017/"
            )["mongo"]["peerInstances"].find())

    for peer in peers:
        peer_uri = peer['uriSlot'][0]['uri'][0]
        if ignore_network and not utils.address_in_network(
            ip_or_uri = peer_uri['ip'],
            net = ignore_network
        ): 
            l.LOGGER('  Looking for a service on peer ' + str(peer))
            yield peer_uri

def search_container(
        service: celaut.Service, 
        metadata: celaut.Any.Metadata, 
        ignore_network: str = None
    ) -> Generator[gateway_pb2.Chunk, None, None]:
    # Search a service tar container.
    for peer in peers_iterator(ignore_network = ignore_network):
        try:
            yield gateway_pb2_grpc.Gateway(
                    grpc.insecure_channel(peer['ip'] + ':' + str(peer['port']))
                ).GetServiceTar(
                    utils.service_extended(
                        service = service,
                        metadata = metadata
                    )
                )
            break
        except: pass

def search_file(hashes: list, ignore_network: str = None) -> Generator[celaut.Any, None, None]:
    # TODO: It can search for other 'Service ledger' or 'ANY ledger' instances that could've this type of files.
    for peer in  peers_iterator(ignore_network = ignore_network):
        try:
            yield gateway_pb2_grpc.GatewayStub(
                    grpc.insecure_channel(peer['ip'] + ':' + str(peer['port']))
                ).GetFile(
                    utils.service_hashes(
                        hashes = hashes
                    )
                )
        except: pass

def search_definition(hashes: list, ignore_network: str = None) -> celaut.Service:
    #  Search a service description.
    service = celaut.Service()
    for any in  search_file(
        hashes = hashes,
        ignore_network = ignore_network
    ):
        service.parseFromString(any.value)
        if any.metadata.complete:
            if check_service(
                    service = service,
                    hashes = hashes
                ):
                    break
            else:
                service = celaut.Service()
    
    if service:
        #  Save the service on the registry.
        save_service(
            service = service,
            metadata = any.metadata
        )
        return service 

    else:
        l.LOGGER('The service '+ hashes[0].value.hex() + ' was not found.')
        raise Exception('The service ' + hashes[0].value.hex() + ' was not found.')

def get_service_from_registry(hash: str) -> celaut.Service:
    service = celaut.Service()
    service.ParseFromString(
        get_from_registry(hash = hash).value
    )
    return service

def get_from_registry(hash: str) -> celaut.Any:
    l.LOGGER('Getting ' + hash + ' service from the local registry.')
    try:
        with open(REGISTRY + hash, 'rb') as file: # TODO: content all to Any, delete the .service sufix.
            any = celaut.Any()
            any.ParseFromString(file.read())
            return any
    except (IOError, FileNotFoundError):
        l.LOGGER('The service was not on registry.')
        raise FileNotFoundError


class Gateway(gateway_pb2_grpc.Gateway):

    def StartService(self, request_iterator, context):
        l.LOGGER('Starting service ...')
        configuration = None
        hashes = []
        for r in request_iterator:

            # Captura la configuracion si puede.
            if r.HasField('config'):
                configuration = r.config
            
            # Si me da hash, comprueba que sea sha256 y que se encuentre en el registro.
            if r.HasField('hash'):
                hashes.append(r.hash)
                if configuration and SHA3_256_ID == r.hash.type and \
                    r.hash.value.hex() in [s for s in os.listdir(REGISTRY)]:
                    try:
                        return launch_service(
                            service = get_service_from_registry(
                                hash = r.hash.value.hex()
                            ),
                            metadata = celaut.Any.Metadata(
                                hashtag = celaut.Any.Metadata.HashTag(
                                    hash = hashes
                                )
                            ), 
                            config = configuration,
                            father_ip = utils.get_only_the_ip_from_context(context_peer = context.peer())
                        )
                    except Exception as e:
                        l.LOGGER('Exception launching a service ' + str(e))
                        continue
            
            # Si me da servicio.
            if r.HasField('service') and configuration:
                save_service(
                    service = r.service,
                    metadata = celaut.Any.Metadata(
                        hashtag = celaut.Any.Metadata.HashTag(
                            hash = hashes
                        )
                    )
                )
                return launch_service(
                    service = r.service,
                    metadata = celaut.Any.Metadata(
                        hashtag = celaut.Any.Metadata.HashTag(
                            hash = hashes
                        )
                    ), 
                    config = configuration,
                    father_ip = utils.get_only_the_ip_from_context(context_peer = context.peer())
                )
        
        l.LOGGER('The service is not in the registry and the request does not have the definition.')
        
        try:
            return launch_service(
                service = search_definition(hashes = hashes),
                metadata = celaut.Any.Metadata(
                    hashtag = celaut.Any.Metadata.HashTag(
                        hash = hashes
                    )
                ), 
                config = configuration,
                father_ip = utils.get_only_the_ip_from_context(context_peer = context.peer())
            ) 
        except Exception as e:
            raise Exception('Was imposible start the service. ' + str(e))


    def StopService(self, request, context):

        l.LOGGER('Stopping the service with token ' + request.token)
        
        if utils.get_network_name(ip_or_uri = request.token.split('##')[1]) == DOCKER_NETWORK: # Suponemos que no tenemos un token externo que empieza por una direccion de nuestra subnet.
            purgue_internal(
                father_ip = request.token.split('##')[0],
                container_id = request.token.split('##')[2],
                container_ip = request.token.split('##')[1]
            )
        
        else:
            purgue_external(
                father_ip = request.token.split('##')[0],
                node_uri = request.token.split('##')[1],
                token = request.token[len( request.token.split('##')[1] ) + 1:] # Por si el token comienza en # ...
            )
        
        l.LOGGER('Stopped the instance with token -> ' + request.token)
        return gateway_pb2.Empty()
    
    def Hynode(self, request: gateway_pb2.Instance, context):
        l.LOGGER('\nAdding peer ' + str(request))
        insert_instance_on_mongo(instance = request.instance)
        return generate_gateway_instance(
            network = utils.get_network_name(
                ip_or_uri = utils.get_only_the_ip_from_context(
                    context_peer = context.peer()
                )
            )
        )

    def GetFile(self, request_iterator, context) -> celaut.Any:
        l.LOGGER('Request for give a service definition')
        hashes = []
        for hash in request_iterator:
            try:
                # Comprueba que sea sha256 y que se encuentre en el registro.
                hashes.append(hash)
                if SHA3_256_ID == hash.type and \
                    hash.value.hex() in [s for s in os.listdir(REGISTRY)]:
                    return get_from_registry(
                                hash = hash.value.hex()
                           )
            except: pass
        
        try:
            return search_file(
                ignore_network = utils.get_network_name(
                        ip_or_uri = utils.get_only_the_ip_from_context(context_peer = context.peer())
                    ),
                hashes = hashes
            )[0] # It's not verifying the content, because we couldn't 've the format for prune metadata in it. The final client will've to check it.
        except:
            raise Exception('Was imposible get the service definition.')

    def GetServiceTar(self, request_iterator, context) -> Generator[gateway_pb2.Chunk, None, None]:
        l.LOGGER('Request for give a service container.')
        for r in request_iterator:

            # Si me da hash, comprueba que sea sha256 y que se encuentre en el registro.
            if r.HasField('hash') and SHA3_256_ID== r.hash.type:
                hash = r.hash.value.hex()
                break
            
            # Si me da servicio.
            if r.HasField('service'):
                hash = get_service_hex_main_hash(service = r.service)
                save_service(
                    service = r.service,
                    metadata = celaut.Any.Metadata(
                        hashtag = [celaut.Any.Metadata.HashTag(
                            hash = [
                                celaut.Any.Metadata.HashTag.Hash(
                                    type = SHA3_256_ID,
                                    value = bytes.fromhex(hash)
                                )
                            ]                            
                        )]
                    )
                )
                service = r.service
                break

        l.LOGGER('Getting the container of service ' + hash)
        if hash and hash in [s for s in os.listdir(REGISTRY)]:
            try:
                os.system('docker save ' + hash + '.service > ' + HYCACHE + hash + '.tar')
                l.LOGGER('Returned the tar container buffer.')
                return utils.get_file_chunks(filename = HYCACHE + hash + '.tar')
            except:
                l.LOGGER('Error saving the container ' + hash)
        else:
            # Puede buscar el contenedor en otra red distinta a la del solicitante.
            try:
                return search_container(
                    ignore_network = utils.get_network_name(
                        ip_or_uri = utils.get_only_the_ip_from_context(context_peer = context.peer())
                        ),
                    service = service
                )
            except:
                l.LOGGER('The service ' + hash + ' was not found.')

        raise Exception('Was imposible get the service container.')


    def GetServiceCost(self, request_iterator, context):
        for r in request_iterator:

            if r.HasField('hash') and SHA3_256_ID == r.hash.type and \
                r.hash.value.hex() in [s for s in os.listdir(REGISTRY)]:
                cost = execution_cost(
                        service = get_service_from_registry(
                                hash = r.hash.value.hex()
                            ),
                        metadata = celaut.Any.Metadata(
                            hashtag = [celaut.Any.Metadata.HashTag(
                                hash = r.hash
                            )]
                        )
                    )
                break

            if r.HasField('service'):
                cost = execution_cost(
                    service = r.service,
                    metadata = celaut.Any.Metadata(
                        hashtag = [celaut.Any.Metadata.HashTag(
                            hash = r.hash
                        )]
                    )
                )
                break

        l.LOGGER('Execution cost for a service is requested, cost -> ' + str(cost))
        return gateway_pb2.CostMessage(
            cost = cost
        )



if __name__ == "__main__":
    from zeroconf import Zeroconf

    # Create __hycache__ if it does not exists.
    try:
        os.system('mkdir ' + HYCACHE)
    except:
        pass

    # Zeroconf for connect to the network (one per network).
    for network in ni.interfaces():
        if network != DOCKER_NETWORK and network != LOCAL_NETWORK:
            Zeroconf(network=network)

    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=30))
    gateway_pb2_grpc.add_GatewayServicer_to_server(
        Gateway(), server=server
    )

    SERVICE_NAMES = (
        gateway_pb2.DESCRIPTOR.services_by_name['Gateway'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:' + str(GATEWAY_PORT))
    l.LOGGER('Starting gateway at port'+ str(GATEWAY_PORT))
    server.start()
    server.wait_for_termination()
