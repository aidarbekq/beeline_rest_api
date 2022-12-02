# beeline_rest_api

<!-- ABOUT THE PROJECT -->
## About The Project

### REST API WITHOUT ANY FRAMEWORKS. 
Pure python. 

Based on socket and http.server libraries. 

METHODS : POST

## Getting Started

## clone
 `git clone https://github.com/aidarbekq/beeline_rest_api.git` 

#### Important !  You need to create and activate the virtualenv before next step.
* [virtualenv](https://pypi.org/project/virtualenv/)

## Install all required dependencies from requirements file

 `pip install -r requirements.txt`


# run the server

`python server.py`



# send post request
send to http://127.0.0.1:8000 

important! post request must be json format. E: {"name": "test", "time": "2022-12-2 23:05"}

time - must be in FUTURE

you can use postman, curl etc. to send requests. 

* [postman](https://learning.postman.com/docs/getting-started/introduction/)

* [curl](https://reqbin.com/req/c-d2nzjn3z/curl-post-body)




# stop the server
ctrl+c
