from src.gateway.server import get_from_registry

GATEWAY_HOST = '127.0.0.1:8080'

def docker_container_id_from_name(docker_name):
    return 'token'

def check_gateway():
    import requests
    try:
        return requests.get('http://'+GATEWAY_HOST+'/') == 200
    except ConnectionError:
        return False

def launch_instance(image):
    import requests
    import json
    with open('__registry__/'+image+'.json') as file:
        file = json.load(file)
        envs = {}
        for env in file['Container']['Envs']:
            print('Valor para: '+env)
            envs.update({
                env:input()
            })
    response = requests.post('http://'+GATEWAY_HOST+'/'+image, json=envs)
    print(response)

def clean_cache():
    import os
    os.system('rm -rf __cache__')
    os.system('mkdir __cache__')
    print('Cleaned.')

def delete_instance(docker_name):
    import requests
    token = docker_container_id_from_name(docker_name)
    print('Confirm to delete '+docker_name+' [Yes/No] ')
    inpt = input()
    if inpt == 'Y' or inpt == 'y' or inpt == 'yes' or inpt == 'Yes':
        if requests.get('http://'+GATEWAY_HOST+'/'+token) == 200: print('DO IT.')
    else: print('Canceled.')

def delete_image(image):
    print('Confirm to delete '+image+' [Yes/No] ')
    inpt = input()
    if inpt == 'Y' or inpt == 'y' or inpt == 'yes' or inpt == 'Yes':
        pass
    else: print('Canceled.')

def images_list():
    import os
    for l in os.listdir('../__registry__'):
        if len(l.split('.'))==2:
            print(l.split('.')[0])

def instances_list():
    import os
    os.system('sudo docker ps')

if __name__ == "__main__":
    """
    import os
    os.chdir( os.getcwd() )
    os.system('python3')    
    """

    import sys
    id = sys.argv[1]

    if id == 'seeder':
        from contracts.eth_main.seeder import seed
        seed() if len(sys.argv) == 2 else seed(private_key=sys.argv[2])
        
    if id == 'connect':
        from src.utils.zeroconf import connect
        connect(sys.argv[2])

    """
        else:
            from src.builder.build import build
            print('Go to build ', id)
            service_with_meta = get_from_registry(id)
            print(
                build(
                    service_buffer = service_with_meta.value,
                    metadata = service_with_meta.metadata,
                    service_id = id
                )
            )    
    """