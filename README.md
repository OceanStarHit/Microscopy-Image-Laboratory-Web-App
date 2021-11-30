# IAS-project
Image Analysis web application

Backend - FastApi

Frontend - Vue

## Environment Setup


### Use docker compose
- Run the following command in the IAS-project folder to start all backend services
  ```sh
  # If this is the first time running this command it will take some time while the docker images are downloaded.
  # Future uses will be very fast.
  $ docker compose up
  ```


- To start a development version of the front end, please input the following commands.
  ```sh
  $ cd vue
  
  # this will install all modules and could take some time
  $ npm install 
  
  # this will build and serve the project.
  $ npm run serve 
  ```
- [http://localhost:8080/]() to see the frontend


- [http://localhost:8000/docs]() to see the backend documentation


- [http://localhost:8081/devDB/]() to see the database

### Monitoring
To monitor the celery worker tasks / microservices. Go to [http://localhost:5555/]()

To monitor RabbitMQ, the message broker. Go to [http://localhost:15672/]()
And enter the username and password set in the celery_task.env file in ./env_files.
Default: 
- User: 'user'
- Password: 'password'


## License

Apache License 2.0

---
