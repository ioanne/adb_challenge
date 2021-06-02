Apptim challenge
=================

Development enviroment setup with docker and docker-compose (Ubuntu 20.04.2 LTS)
-------------------------------------

1. ```$ git clone https://github.com/ioanne/adb_challenge.git```
2. ```$ docker-compose build```
3. ```$ docker-compose up```
 
 Run test
-------------------------------------
All the tests are mocked, so it is not necessary to have an emulator.
-------------------------------------
1. ```$docker_compose up```
2. ```docker-compose exec web_apptim pytest -v app/api/v1/test/test_main.py```
