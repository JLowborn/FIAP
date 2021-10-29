'''
FIAP
Defesa Cibernética
Development & Coding for Security

Python Docker API Interface

Prof. Ms. Fábio H. Cabrini
Atividade: Check Point 6

Alunos:
Carlos Jesus - RM87187
Filipe Grahl - RM86663
Gustavo Khairalla - RM87101
Victor Dias - RM88582
'''

from colorama import Fore, Style
import docker
import json
from os import getenv
from os import getuid
import pymongo
import requests


''' Database information '''
client = docker.from_env()
API_ADDRESS = ''    # CHANGE TO API ADDRESS
mongo = pymongo.MongoClient(getenv('MONGO_URI'))
database = mongo['docker_interface']


''' Show all available containers '''
def show_containers():
    containers = requests.get(API_ADDRESS + '/containers/json?all=true').json()
    print(f'\n{Fore.GREEN}[+]{Fore.WHITE} Available Containers:\n')
    print(f"{'CONTAINER_ID':<12}  {'IMAGE_NAME':<22}  {'STATUS':<10}  {'CONTAINER_NAME':<22}")
    for container in containers:
        _id = container['Id'][:12]
        name = container['Names'][0].replace('/','')
        image = container['Image']
        status = container['State']
        print(f"{_id:<12}  {image:<22}  {status:<10}  {name:<22}")


''' Create container and automatically starts it '''
def create_container():
    image = input('[-] Image name: ')
    name = input('[-] Container name [leave blank for random name]: ')
    payload = json.dumps({
        "Hostname": "",
        "Domainname": "",
        "User": "",
        "AttachStdin": False,
        "AttachStdout": True,
        "AttachStderr": True,
        "Tty": False,
        "OpenStdin": False,
        "StdinOnce": False,
        "Image": image
    })

    response = requests.post(API_ADDRESS + '/containers/create', data=payload) if not name else requests.post(API_ADDRESS + f'/containers/create?name={name}', data=payload)

    # If the image does not exist
    if response.status_code == 404:
        exit(f'\n{Fore.RED}[!]{Fore.WHITE} No such image')

    _id = response.json()['Id']
    print(f"\n{Fore.GREEN}[+]{Fore.WHITE} Container successfully created: {_id}")


''' Delete selected container '''
def delete_container():
    _id = input('[-] Container ID: ')
    response = requests.post(API_ADDRESS + f'containers/{_id}/stop')  # Stop the container before deleting it

    # If the container does not exist
    if response.status_code == 404:
        exit(f'\n{Fore.RED}[!]{Fore.WHITE} No such container')

    response = requests.delete(API_ADDRESS + f'/containers/{_id}')  # Delete the container
    print(f"\n{Fore.GREEN}[+]{Fore.WHITE} Container successfully removed: {_id}")


''' Stop and delete all existing containers '''
def delete_all_containers():
    confirm = input(f"{Fore.YELLOW}[i]{Fore.WHITE} You're about the delete all containers, are you sure? [y/N] ")
    
    if confirm.lower() in ('y', 'yes'):
        containers = requests.get(API_ADDRESS + '/containers/json').json()
        containers = [container['Id'][:12] for container in containers]
        
        # Stop all containers before deletion
        [requests.post(API_ADDRESS + f'/containers/{_id}/stop') for _id in containers]

        # Delete all containers
        [requests.delete(API_ADDRESS + f'/containers/{_id}') for _id in containers]

        print(f"\n{Fore.GREEN}[+]{Fore.WHITE} All containers successfully deleted")
    else:
        print('[-] Canceled')


''' Show all pulled images '''
def show_images():
    images = requests.get(API_ADDRESS + '/images/json?all=true').json()
    print(f'\n{Fore.GREEN}[+]{Fore.WHITE} Available Images:\n')
    print(f"{'REPOSITORY':<12}  {'TAG':<12}  {'IMAGE ID':<12}")
    for image in images:
        _id = image['Id'].split(':')[1][:12]
        repository, tag = image['RepoTags'][0].split(':')
        print(f"{repository:<12}  {tag:<12}  {_id:<12}")


''' Pull/Update image and return it's ID '''
def pull_image():
    image = input('[-] Image name: ')
    response = requests.post(API_ADDRESS + f'/images/create?fromImage={image}')

    # If the image does not exist
    if response.status_code == 404:
        exit(f'\n{Fore.RED}[!]{Fore.WHITE} No such image')

    print(f"\n{Fore.GREEN}[+]{Fore.WHITE} Image successfully pulled: {image}")


''' Delet selected image '''
def delete_image():
    image = input('[-] Image name/id: ')
    response = requests.delete(API_ADDRESS + f'/images/{image}?force=true')

    if response.status_code == 404:
        exit(f'\n{Fore.RED}[!]{Fore.WHITE} No such image')

    print(f"{Fore.GREEN}[+]{Fore.WHITE} Image successfully deleted: {image}")


''' Delete all pulled images '''
def delete_all_images():
    confirm = input(f"{Fore.YELLOW}[i]{Fore.WHITE} You're about the delete all images, are you sure? [y/N] ")
    
    if confirm.lower() in ('y', 'yes'):
        images = requests.get(API_ADDRESS + '/images/json?all=true').json()
        images = [image['Id'].split(':')[1][:12] for image in images]

        # Force delete all images
        [requests.delete(API_ADDRESS + f'/images/{_id}?force=true') for _id in images]

        print(f"{Fore.GREEN}[+]{Fore.WHITE} All images successfully deleted")
    else:
        print('[-] Canceled')


''' Show containers information '''
def status():

    # Get container IDs
    containers = requests.get(API_ADDRESS + '/containers/json').json()
    containers = [container['Id'][:12] for container in containers]

    print(f'\n{Fore.GREEN}[+]{Fore.WHITE} Container usage information: ')
    print(f"\n{'CONTAINER ID':<12}  {'MEMORY USAGE':<12}  {'CPU USAGE':<9}")

    for _id in containers:
        data = requests.get(API_ADDRESS + f'/containers/{_id}/stats?stream=false').json()

        # Used memory porcentage
        used_memory = data['memory_stats']['usage'] - data['memory_stats']['stats']['cache']
        available_memory = data['memory_stats']['limit']
        memory_usage_percentage = (used_memory / available_memory) * 100.0

        # # Used CPU porcentage
        cpu_delta = data['cpu_stats']['cpu_usage']['total_usage'] - data['precpu_stats']['cpu_usage']['total_usage']
        system_cpu_delta = data['cpu_stats']['system_cpu_usage'] - data['precpu_stats']['system_cpu_usage']
        number_cpus = data['cpu_stats']['online_cpus']
        cpu_usage_pocentage = (cpu_delta / system_cpu_delta) * number_cpus * 100.0

        print(f"{_id:<12}  {memory_usage_percentage:<12.2%}  {cpu_usage_pocentage:<9.2%}")

    # Insert raw information into database
    try:
        print(f"\n{Fore.GREEN}[+]{Fore.WHITE} Uploading data to Mongo database...")
        data = [requests.get(API_ADDRESS + f'/containers/{_id}/stats?stream=false').json() for _id in containers]
        collection = database['docker_stats']
        collection.insert_many(data)
    except pymongo.errors.ServerSelectionTimeoutError:
        print(f"\n{Fore.RED}[!]{Fore.WHITE} Failed to upload data to database")
        

''' Default error message for invalid switcher options '''
def default():
    print(f'\n{Fore.RED}[!]{Fore.WHITE} Invalid option')


''' Exit program '''
def _exit():
    exit(f'\n{Fore.RED}[!]{Fore.WHITE} Program terminated')


''' Option switch '''
def switch():
    while True:
        try:
            option = int(input('\n>> '))
            options.get(option, default)()
        except ValueError:
            default()
        except KeyboardInterrupt:
            exit(f'\n\n{Fore.RED}[!]{Fore.WHITE} Program terminated')


''' Menu interface '''
def interface():
    print(f'''
{Style.BRIGHT}EDM - Easy Docker Manager

[1] Show containers
[2] Create container
[3] Delete container
[4] Delete all containers
[5] Show images
[6] Pull images
[7] Delete image
[8] Delete all images
[9] Status

[0] Menu
[99] Exit program''')


''' Menu options '''
options = {
    1: show_containers,
    2: create_container,
    3: delete_container,
    4: delete_all_containers,
    5: show_images,
    6: pull_image,
    7: delete_image,
    8: delete_all_images,
    9: status,
    0: interface,
    99: _exit
}


if __name__ == '__main__':

    if getuid() != 0: exit(f'{Fore.RED}[!]{Fore.WHITE} User must be root')

    interface()
    switch()