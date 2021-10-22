# Flask + MongoDB API



Python RESTful API developed by using Flask and MongoDB, it has all basic CRUD (Create, Read, Update, Delete) as well as reading every entry from databases and ID auto generation.

### How to use:

This API requires you to have In order to run the API you have to create an account in [MongoDB Cloud](https://www.mongodb.com/en/cloud), create a database as well as a collection.  Once you've created it, just type in the terminal:

```
$ export MONGO_URI="YOUR_MONGO_URI"
$ FLASK_APP=Flask\ API flask run
```

### Create

  A **POST** request sent to the API containing JSON data with the fields "nome", "banda", "ano" e "categorias".

![Create operation](https://github.com/JLowborn/FIAP/blob/uploads/create.gif)



#### Read All

  A **GET** request sent to the API with no parameter passed in the URL.

![Create operation](https://github.com/JLowborn/FIAP/blob/uploads/read_all.gif)



#### Read One

  A **GET** request sent to the API with the desired entry ID.

![Create operation](https://github.com/JLowborn/FIAP/blob/uploads/read_entry.gif)



#### Update

  A **PUT** request sent to the API with the entry ID for update.

![Create operation](https://github.com/JLowborn/FIAP/blob/uploads/update_entry.gif)



#### Delete

  A **DELETE** request sent to the API with the entry ID for deletion.

![Create operation](https://github.com/JLowborn/FIAP/blob/uploads/delete_entry.gif)
