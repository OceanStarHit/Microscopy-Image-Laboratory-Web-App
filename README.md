# IAS-project
Image Analysis web application

Backend - Django  
Frontend - Vue

## Environment Setup
### Windows
**Install `python3`**
- To download Python 3.9.x, go to [Download Python](https://www.python.org/downloads/) page and then click on the button to download the latest version of Python
- Next, run the installation file that you just downloaded
- You can now start the installation of Python by clicking on **Install Now** ( You have to also check the box to `Add Python to the Path` in this step)
- After a short period of time, your setup would be completed  
  [See more detail](https://datatofish.com/install-python/)

**Install `MySQL`**
- Download the latest Mysql Community server from [MySQL official website](https://dev.mysql.com/downloads/mysql/)
- Go to your downloads folder where you can see the `mysql-installer-community` file, right click on that file and click Install option
- Proceed the installation wizard with default configurations
- On `Accounts and Roles` step of **MySQL Installer**, you can set your MySQL root user password.  To create a new user, you can click on `Add User` button under MySQL user accounts section. Then, please create a new user with following information
  | Category | Value |
  | ------ | ------ |
  | Username | myprojectuser |
  | Host | localhost |
  | Role | DB Admin |
  | Password | Password1 |
- Finish the installation by completing the next steps  
  [See more detail](https://www.onlinetutorialspoint.com/mysql/install-mysql-on-windows-10-step-by-step.html)

Next, create a new database(database name: **myproject**) in `MySQL Workbench`

### MacOS
**Install `python3` and some tools**
```sh
$ brew update
$ brew install python3
```
Along with python 3 (the latest version), these commands will install `pip`, `setuptools` and `wheel`
Make sure if python3 and pip3 was installed successfully
```sh
$ python3 --version
$ pip3 --version
```

**Install and setup `MySQL`**
```
$ brew info mysql
$ brew install mysql
```
Load and start the MySQL service
```
$ brew services start mysql
```
Create new user and new database for the project
```sh
$ mysql -u root -p
mysql> CREATE USER 'myprojectuser'@'localhost' IDENTIFIED BY 'Password1';
mysql> GRANT ALL ON *.* to 'myprojectuser'@'localhost';
mysql> CREATE DATABASE myproject;
mysql> exit
```

## First configuration for excuting the project
This step is only necessary the first time

### Windows
- Open Github app, go to `Repository` menu and click `Pull` button. **Pulling** will take some seconds
- Open Command Prompt in `IAS-project/django` directory and run the following commands
  ```sh
  $ pip install -r requirement.txt
  $ pip install python-bioformats
  $ python manage.py migrate
  ```

### MacOS
Clone this repository and run the following commands  in Terminal
```sh
$ ...
$ cd IAS-project/django
$ pip install -r requirement.txt
$ pip install python-bioformats
$ python manage.py migrate
```

## Run the application
Should proceed this step each time to run the project

### Windows
- Open Github app, go to `Repository` menu and click `Pull` button. **Pulling** will take some seconds
- Open Command Prompt in `IAS-project/django` directory and run the following commands
  ```sh
  $ python manage.py runserver
  ```

### MacOS
- Go to `IAS-project/django` directory in Terminal and pull the updates from github
  ```sh
  $ cd IAS-project/django
  $ git pull
  ```
- Run the django backend
  ```sh
  $ python manage.py runserver
  ```

You can check the app at `http://127.0.0.1:8000` on your browser

### Use docker compose
- Run the following command in the IAS-project folder to start all backend services
  ```sh
  $ docker compose up
  ```
- If it's the first time running, you must also migrate the database. Please input the following command to get open a shell into the django container
  ```sh
  $ docker container exec -it ias-project-api-1 bash
  ```
- Once you are in the shell please input the following commands. You might have to Ctrl+C to exit a command once it's been run.
  ```sh
  $ python manage.py makemigrations
  $ python manage.py migrate
  ```
- Exit the django shell by pressing Ctrl+D


- To start a development version of the front end, please input the following command. This might take some time to build the app.
  ```sh
  $ cd vue
  $ npm run serve
  ```

### Monitoring
To monitor the celery worker tasks / microservices. Go to [http://localhost:5555/]()

To monitor RabbitMQ, the message broker. Go to [http://localhost:15672/]()
And enter the username and password set in the .env file.
Default: 
- User: 'user'
- Password: 'password'


## Runbook
  ```sh
  $ cd project_dir
  $ git pull origin dev
  $ docker-compose build ui
  $ docker-compose up
  ```

## License

Apache License 2.0

---
