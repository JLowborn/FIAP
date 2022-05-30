import json
from os import getenv, getuid

import docker
import pymongo
import requests
from colorama import Fore, Style

""" Database information """
client = docker.from_env()
API_ADDRESS = "http://192.168.1.17:2375"
mongo = pymongo.MongoClient(getenv("MONGO_URI"))
database = mongo["docker_interface"]


def show_containers():
    """Show all available containers"""
    containers = requests.get(API_ADDRESS + "/containers/json?all=true").json()
    print(f"\n{Fore.GREEN}[+]{Fore.WHITE} Available Containers:\n")
    print(
        f"{'CONTAINER_ID':<12}  {'IMAGE_NAME':<22}  {'STATUS':<10}  {'CONTAINER_NAME':<22}"
    )
    for container in containers:
        _id = container["Id"][:12]
        name = container["Names"][0].replace("/", "")
        image = container["Image"]
        status = container["State"]
        print(f"{_id:<12}  {image:<22}  {status:<10}  {name:<22}")


def create_container():
    """Create container and automatically starts it"""
    image = input("[-] Image name: ")
    name = input("[-] Container name [leave blank for random name]: ")
    payload = json.dumps(
        {
            "Hostname": "",
            "Domainname": "",
            "User": "",
            "AttachStdin": False,
            "AttachStdout": True,
            "AttachStderr": True,
            "Tty": False,
            "OpenStdin": False,
            "StdinOnce": False,
            "Image": image,
        }
    )

    response = (
        requests.post(
            API_ADDRESS + "/containers/create",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        if not name
        else requests.post(
            API_ADDRESS + f"/containers/create?name={name}",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
    )

    # If the image does not exist
    if response.status_code == 404:
        exit(f"\n{Fore.RED}[!]{Fore.WHITE} No such image")

    _id = response.json()["Id"][:12]
    print(f"\n{Fore.GREEN}[+]{Fore.WHITE} Container successfully created: {_id}")


def delete_container():
    """Delete selected container"""
    _id = input("\n[-] Container ID: ")
    response = requests.post(
        API_ADDRESS + f"/containers/{_id}/stop"
    )  # Stop the container before deleting it

    # If the container does not exist
    if response.status_code == 404:
        exit(f"\n{Fore.RED}[!]{Fore.WHITE} No such container")

    response = requests.delete(
        API_ADDRESS + f"/containers/{_id}"
    )  # Delete the container
    print(f"{Fore.GREEN}[+]{Fore.WHITE} Container successfully removed: {_id}")


def delete_all_containers():
    """Stop and delete all existing containers"""
    confirm = input(
        f"\n{Fore.YELLOW}[i]{Fore.WHITE} You're about the delete all containers, are you sure? [y/N] "
    )

    if confirm.lower() in ("y", "yes"):
        containers = requests.get(API_ADDRESS + "/containers/json").json()
        containers = [container["Id"][:12] for container in containers]

        # Stop all containers before deletion
        [requests.post(API_ADDRESS + f"/containers/{_id}/stop") for _id in containers]

        # Delete all containers
        [requests.delete(API_ADDRESS + f"/containers/{_id}") for _id in containers]

        print(f"\n{Fore.GREEN}[+]{Fore.WHITE} All containers successfully deleted")
    else:
        print("[-] Canceled")


def show_images():
    """Show all pulled images"""
    images = requests.get(API_ADDRESS + "/images/json?all=true").json()
    print(f"\n{Fore.GREEN}[+]{Fore.WHITE} Available Images:\n")
    print(f"{'REPOSITORY':<12}  {'TAG':<12}  {'IMAGE ID':<12}")
    for image in images:
        _id = image["Id"].split(":")[1][:12]
        repository, tag = image["RepoTags"][0].split(":")
        print(f"{repository:<12}  {tag:<12}  {_id:<12}")


def pull_image():
    """Pull/Update image and return it's ID"""
    image = input("\n[-] Image name: ")
    response = requests.post(API_ADDRESS + f"/images/create?fromImage={image}")

    # If the image does not exist
    if response.status_code == 404:
        exit(f"\n{Fore.RED}[!]{Fore.WHITE} No such image")

    print(f"\n{Fore.GREEN}[+]{Fore.WHITE} Image successfully pulled: {image}")


def delete_image():
    """Delet selected image"""
    image = input("\n[-] Image name/id: ")

    if image == "":
        print(f"{Fore.RED}[!]{Fore.WHITE} User must input a image name or ID")
    else:
        response = requests.delete(API_ADDRESS + f"/images/{image}?force=true")

        if response.status_code == 404:
            exit(f"\n{Fore.RED}[!]{Fore.WHITE} No such image")

        print(f"{Fore.GREEN}[+]{Fore.WHITE} Image successfully deleted: {image}")


def delete_all_images():
    """Delete all pulled images"""
    confirm = input(
        f"{Fore.YELLOW}[i]{Fore.WHITE} You're about the delete all images, are you sure? [y/N] "
    )

    # User confirmation
    if confirm.lower() in ("y", "yes"):
        images = requests.get(API_ADDRESS + "/images/json?all=true").json()
        images = [image["Id"].split(":")[1][:12] for image in images]

        # Force delete all images
        [requests.delete(API_ADDRESS + f"/images/{_id}?force=true") for _id in images]

        print(f"{Fore.GREEN}[+]{Fore.WHITE} All images successfully deleted")
    else:
        print("[-] Canceled")


def status():
    """Show containers information"""

    # Get container IDs
    containers = requests.get(API_ADDRESS + "/containers/json").json()
    containers = [container["Id"][:12] for container in containers]

    print(f"\n{Fore.GREEN}[+]{Fore.WHITE} Container usage information: ")
    print(f"\n{'CONTAINER ID':<12}  {'MEMORY USAGE':<12}  {'CPU USAGE':<9}")

    for _id in containers:
        data = requests.get(
            API_ADDRESS + f"/containers/{_id}/stats?stream=false"
        ).json()

        # Used memory porcentage
        used_memory = (
            data["memory_stats"]["usage"] - data["memory_stats"]["stats"]["cache"]
        )
        available_memory = data["memory_stats"]["limit"]
        memory_usage_percentage = (used_memory / available_memory) * 100.0

        # # Used CPU porcentage
        cpu_delta = (
            data["cpu_stats"]["cpu_usage"]["total_usage"]
            - data["precpu_stats"]["cpu_usage"]["total_usage"]
        )
        system_cpu_delta = (
            data["cpu_stats"]["system_cpu_usage"]
            - data["precpu_stats"]["system_cpu_usage"]
        )
        number_cpus = data["cpu_stats"]["online_cpus"]
        cpu_usage_pocentage = (cpu_delta / system_cpu_delta) * number_cpus * 100.0

        print(
            f"{_id:<12}  {memory_usage_percentage:<12.2%}  {cpu_usage_pocentage:<9.2%}"
        )

    # Insert raw information into database
    try:
        print(f"\n{Fore.GREEN}[+]{Fore.WHITE} Uploading data to Mongo database...")
        data = [
            requests.get(API_ADDRESS + f"/containers/{_id}/stats?stream=false").json()
            for _id in containers
        ]
        collection = database["docker_stats"]
        collection.insert_many(data)
    except pymongo.errors.ServerSelectionTimeoutError:
        print(f"\n{Fore.RED}[!]{Fore.WHITE} Failed to upload data to database")


def default():
    """Default error message for invalid switcher options"""
    print(f"\n{Fore.RED}[!]{Fore.WHITE} Invalid option")


def _exit():
    """Exit program"""
    exit(f"\n{Fore.RED}[!]{Fore.WHITE} Program terminated")


def switch():
    """Option switch"""
    while True:
        try:
            option = int(input("\n>> "))
            options.get(option, default)()
        except KeyboardInterrupt:
            exit(f"\n\n{Fore.RED}[!]{Fore.WHITE} Program terminated")


def interface():
    """Menu interface"""
    print(
        f"""
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
[99] Exit program"""
    )


""" Menu options """
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
    99: _exit,
}


if __name__ == "__main__":

    if getuid() != 0:
        exit(f"{Fore.RED}[!]{Fore.WHITE} User must be root")

    interface()
    switch()
