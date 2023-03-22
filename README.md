# fast-api-sklearn-rapid-deployment
Ready to use project (and docker image) for deploying sklearn models using fastAPI


## What the hell is this all about

**TLDR: It's an API, just use a POST response on api/predict with a JSON {'data':{dict(str,float)}} and a header {'access_token': API_KEY} on the IP in the server and you will get a dictionary {'prediction': str} with the prediction**


The API itself is composed by these capabilities

* `GET` Serves as a hello world message. Useful to know if the server is up
* `POST api/predict/` predicts given a dictionary of infomration named `data`. The 
  
All of the `api/*` responses need a header with the format ´{'access_token':API_KEY}´ to improve security. In order to not save the ´API_KEY´ on ´.env´, the dockerfile runs a script to generate an ´API_KEY´ as soon as the build is finished. You can check it by inspecting the container

The pipeline has been tested on some cloud services.

## Some useful commands to run locally

Set virtual environment running the `setup_venv.bat` or copy-pasting these commands on the terminal (works for windows)

```bat
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Run the app using uvicorn with

```bat
uvicorn main:app --port 5000 --reload
```

The option `--reload` is critical to solve bugs while you write the code on the same time

To run the build and run the docker (on local)

```bat
docker build -t fastapi-sklearn-deploy .
docker run -p 80:80 --name api-container fastapi-sklearn-deploy
```

## Some useful advices and TODOs

* You may want to create the `requirements.txt` by using `pipreqs`, but it may be possible some specific packages are not installed (like `uvicorn`) ask me which version of the package we are using on the venv if you miss one on requirements

* This proyect is as safe as using a condom made of seaweed. Take it as a shortcut to start doing some other stuff you need to focus on.**If you want to use this on production, be warned** 