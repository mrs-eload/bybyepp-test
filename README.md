# Installation
## Requirements
- Python >= 3.7
- Docker (https://docs.docker.com/engine/install/ubuntu/)
- Redis
- Rabbit MQ
- Netdata (optional)

## Python env
In order to avoid having global dependencies installed on your system use env

1   . Install venv

`mrs-eload:~$ sudo apt install -y python3-venv`

2   . Create a folder in your work directory (outside of project directory) and install your virtual env (i called it byebyepp)

`mrs-eload:~$ mkdir environments`

`mrs-eload:~$ python3 -m venv byebyepp`

`mrs-eload:~$ ls my_env`

Output:

`bin include lib lib64 pyvenv.cfg share`

3   .  Activate your env

`source byebyepp/bin/activate`

Should change your console as: 

`(byebyepp) mrs-eload:~$`


## Poetry (Package manage)

`(byebyepp) mrs-eload:~$ pip install wheel`

`(byebyepp) mrs-eload:~$ pip install poetry`

 
## Redis (runtime)

`(byebyepp) mrs-eload:~$ sudo apt install -y redis`
 
## RabbitMQ (runtime)

`(byebyepp) mrs-eload:~$ docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management`

## Project dependencies
This should install celery, flower etc...

`(byebyepp) mrs-eload:~$ cd byebyepp-test` (project root directory)

`(byebyepp) mrs-eload:~/byebyepp-test$ poetry install`

To activate sample data and debug:
`(byebyepp) mrs-eload:~/byebyepp-test$ export DEV=True`


# Run project

### Background services

`(byebyepp) mrs-eload:~$ sudo service redis-server start`

`(byebyepp) mrs-eload:~$ docker run -itd --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management`

### Foreground services

`(byebyepp) mrs-eload:~/byebyepp-test$  celery worker -A app.services.tasks -l debug -E`

`(byebyepp) mrs-eload:~/byebyepp-test$  flower -A app.services.tasks -l debug -E`

Flower will be available on http://localhost:5555

### Start main server

`(byebyepp) mrs-eload:~/byebyepp-test$ python main.py`

Server will be available on http://localhost:8080

### (Optional) Netdata ibbitnstallation

`(byebyepp) mrs-eload:~/byebyepp-test$ bash <(curl -Ss https://my-netdata.io/kickstart.sh)`