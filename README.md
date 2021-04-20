# IAS-project
Image Analysis web application

Backend - Django

Frontend - Vue

## Environment Setup
### Linux
Install `python3` and some tools
```sh
$ sudo apt-get update
$ sudo apt-get install python3.6
```
Along with python 3, these commands will install **pip**, **setuptools** and **wheel**
Make sure if python3 and pip3 was installed successfully
```sh
$ python3 --version
$ pip3 --version
```

Install `node`
```
$ curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
$ sudo apt update
$ sudo apt install nodejs
```
Make sure if node was installed successfully
```sh
$ node -v
$ npm -v
```

Install `vue-cli`
```
$ npm install -g @vue/cli @vue/cli-service-global
```
Make sure if vue-cli was installed successfully
```sh
$ vue --version
```

### MacOS
Install `python3` and some tools
```sh
$ brew update
$ brew install python3
```
Along with python 3, these commands will install **pip**, **setuptools** and **wheel**
Make sure if python3 and pip3 was installed successfully
```sh
$ python3 --version
$ pip3 --version
```

Install `node`
```
$ brew install node
```
Make sure if node was installed successfully
```sh
$ node -v
$ npm -v
```

Install `vue-cli`
```
$ npm install -g @vue/cli @vue/cli-service-global
```
Make sure if vue-cli was installed successfully
```sh
$ vue --version
```

## Run the application
Go to `IAS-project` directory in Terminal
```sh
$ ...
$ cd IAS-project
```
### Backend
Create a Virtual Environment in the directory and install some dependencies
```sh
$ cd django
$ python3 -m venv myenv
$ source myenv/bin/activate
$ pip install -r requirement.txt
```

Run the project
```sh
$ python manage.py migrate
$ python manage.py runserver
```

### Frontend
Install some dependencies
```
$ cd vue
$ yarn install
```

Compiles and hot-reloads for development
```
$ yarn serve
```
You will see the app at `http://127.0.0.1:8080` on your browser.

Compiles and minifies for production
```
$ yarn build
```

Lints and fixes files
```
$ yarn lint
```

---
