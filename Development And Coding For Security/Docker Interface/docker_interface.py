'''
Docker Interface
'''


from colorama import Fore, Style
import docker
from os import getuid


''' List available containers '''
def list_containers():
    containers = client.containers.list(True)
    print(f'\n{Fore.GREEN}[+]{Fore.WHITE} Available Containers:\n')
    print(f"{'CONTAINER_ID':<12}  {'IMAGE_NAME':<22}  {'STATUS':<10}  {'CONTAINER_NAME':<22}\n")
    for container in containers:
        _id = container.attrs['Id'][:12]
        name = container.attrs['Name'].replace('/','')
        image = container.attrs['Config']['Image']
        status = container.attrs['State']['Status']
        print(f"{_id:<12}  {image:<22}  {status:<10}  {name:<22}")


''' Run container in background with a pseudo-tty shell '''
def run_container():
    image = input(f'{Fore.GREEN}[+]{Fore.WHITE} Image name: ')
    container = client.containers.run(image, detach=True, tty=True, name=None)
    print(f'{Fore.GREEN}[+]{Fore.WHITE} Container running: {container.id}')


''' Start container and return it's ID '''
def start_container():
    _id = input(f'{Fore.GREEN}[+]{Fore.WHITE} Container ID: ')
    container = client.containers.get(_id)
    container.start()
    print(f'{Fore.GREEN}[+]{Fore.WHITE} Container started: {container.id}')


''' Stop container and return it's ID '''
def stop_container():
    _id = input(f'{Fore.GREEN}[+]{Fore.WHITE} Container ID: ')
    container = client.containers.get(_id)
    container.stop()
    print(f'{Fore.GREEN}[+]{Fore.WHITE} Container stopped: {container.id}')


''' Pull/Update image and return it's ID '''
def pull_image():
    repository = input(f'{Fore.GREEN}[+]{Fore.WHITE} Repository name: ')
    # TODO: Try/Except Treatment
    image = client.images.pull(repository)
    _id = image.attrs['Id'].split(':')[1]
    print(f'{Fore.GREEN}[+]{Fore.WHITE} Image successfully pulled with ID: {_id}')


''' Force remove container '''
def remove_container():
    _id = input(f'{Fore.GREEN}[+]{Fore.WHITE} Container ID: ')
    container = client.containers.get(_id)
    container.remove(force=True)
    print(f'{Fore.GREEN}[+]{Fore.WHITE} Container successfully removed')


''' Exit program '''
def _exit():
    exit(f'\n{Fore.RED}[!]{Fore.WHITE} Program terminated')


''' Option switch '''
def switch():
    while True:
        try:
            option = int(input('\n>> '))
            options[option]()
        except (ValueError, KeyError):
            print(f'{Fore.RED}[!]{Fore.WHITE} Invalid option')
        except KeyboardInterrupt:
            exit(f'\n\n{Fore.RED}[!]{Fore.WHITE} Program terminated')


''' Menu interface '''
def interface():
    print(f'''
{Style.BRIGHT}EDM - Easy Docker Manager

[1] List containers
[2] Run container
[3] Start container
[4] Stop container
[5] Pull container
[6] Remove container

[0] Menu
[99] Exit program''')


''' Menu option '''
options = {
    1: list_containers,
    2: run_container,
    3: start_container,
    4: stop_container,
    5: pull_image,
    6: remove_container,
    0: interface,
    99: _exit
}


if __name__ == '__main__':

    if getuid() != 0: exit(f'{Fore.RED}[!]{Fore.WHITE} User must be root')

    client = docker.from_env()
    interface()
    switch()