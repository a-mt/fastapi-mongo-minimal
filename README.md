
# About

...

# Install

* Create src/.env
* Create the image

  ``` bash
  docker-compose build
  ```

* Initialize the database

  ``` bash
  docker run -it --rm --env-file src/.env -v $PWD/data:/data mongo:4.2 bash

  mongoimport \
    --drop \
    --uri "mongodb+srv://$DB_USERNAME:$DB_PASSWORD@${DB_HOST%/*}/$DB_NAME${DB_HOST##*/}" \
    --collection $COLL_NAME \
    --file=/data/city.json \
    --jsonArray

  exit
  ```

# Run

* Run the container

  ``` bash
  docker-compose run
  ```

* Go to localhost:8001 for the app  
  Go to localhost:8001/docs for the documentation
