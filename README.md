# fast-api-sklearn-rapid-deployment
Ready to use project (and docker image) for deploying sklearn models using fastAPI


## What is this all about

**TLDR: POST on api/predict/ with a JSON {'data':{dict(str,float)}} and a header {'access_token': API_KEY} on the IP in the server and you will get a dictionary {'prediction': dict } with the predictions from sklearn model**

The API itself is composed by these capabilities

* `GET /` Serves as a hello world message. Useful to know if the server is up
* `GET /api/names/` Gets names of columns for the model

* `POST /api/predict/` predicts given a dictionary of infomration named `data`. The output is just the class prediction. The model imputs the missing data using a simple Imputer
  
All `/api/` responses need a header with the format `{'access_token':API_KEY}` to authenticate the usage. A default key is already in 

The pipeline has been tested on some cloud services.

## Some useful commands to run locally

To set up the virtual environment

```bat
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Run the app locally using uvicorn with

```bat
uvicorn main:app --port 5000 --reload
```

The option `--reload` is critical to solve bugs while you write the code on the same time

## Deployment with docker 

### Docker only

You can build the docker using

```bat
docker build -t fastapi-sklearn-local .
docker run -p 80:80 --name api-container fastapi-sklearn-deploy
```

This is the better method as the building also creates a custom `API_KEY` on the dot-env.

### Docker compose (recommended)

```bat
docker compose build
docker compose up
```

If `make` is installed on the OS, `make up` runs this from the `Makefile`


## Some useful advices and TODOs

* You may want to create the `requirements.txt` by using `pipreqs`, but it may be possible some specific packages are not installed (like `uvicorn`) ask me which version of the package we are using on the venv if you miss one on requirements

* Other security procedures are necesary, like using `https`

* **If you want to use this on production, be warned**