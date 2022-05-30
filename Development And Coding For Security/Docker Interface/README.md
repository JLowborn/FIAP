# EDM - Easy Docker Manager

EDM is a docker interface created to communicate to docker via API. It's designed to be a faster way of managing  your containers and images without typing docker commands into your terminal. It was tested a Linux OS.

## How does it works:

It uses the docker service as an API in order to manage containers and images via HTTP requests. It is possible to delete/create images and containers as well as colleting data for future consulting. If the user wants to have an overview about one or more containers, EDM can list useful information such as Memory usage and CPU resources consuming.

## Usage:

To use docker service as an API, change the service configuration of the docker service daemon by editing `ExecStart` line in `/lib/systemd/system/docker.service` like so:

`ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2375`

Then restarting the service will initialize docker service as an API, and make it accessible by other machines.

Once started, the program will show a interactive menu in which the user can select options by typing in the equivalent number.

![EDM interface](https://user-images.githubusercontent.com/64245567/139431526-36813618-f122-4106-a310-9ff1379d0aa1.png)

The options are:

- **Show containers**

  List all available containers, showing IDs, image names, status and names.
  
  ![List of existing containers](https://user-images.githubusercontent.com/64245567/139433840-0d7edbd1-12c8-49bd-b0e3-771f626547eb.png)

- **Create container**

  Uses a current existing image to create a container with a custom name.

- **Delete container**

  Delete a container reffered by it's ID.

- **Delete all containers**

  Force delete all containers by stopping and completly removing them.

- **Show images**

  Show all available images pulled by the user.
  
  ![List of pulled images](https://user-images.githubusercontent.com/64245567/139434034-7a7b29ef-cca9-466f-a452-ea7f27b510bb.png)

- **Pull images**

  Pull an image from a repository inputed by the user.
  
  ![Pulled image message](https://user-images.githubusercontent.com/64245567/139434143-72d88a8b-ff6b-43e9-8870-df59cfc0167a.png)

- **Delete image**

  Delete an image based on it's ID.
  
  ![Deleted image message](https://user-images.githubusercontent.com/64245567/139434287-17c2d19c-1e95-4c9a-946f-4995a8e40234.png)

- **Delete all images**
  
  Force delete every available image, ignoring any image-using container.

- **Status**

  Collect containers resource usage data and upload to Mongo database.
  
  ![Container resource usage being shown](https://user-images.githubusercontent.com/64245567/139434474-d0da13e5-e73c-44f1-b9a1-6849a30cba53.png)
