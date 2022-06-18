# Machine Learning & Hexagonal Architecture

The goal of this repo is demonstrate how to apply Hexagonal Architecture in a ML based system

The model used in this example has been taken from
[IntelAI](https://github.com/IntelAI/models/blob/master/docs/object_detection/tensorflow_serving/Tutorial.md)

## Documentation

Functional documentation can be found [here](docs)

## Download the model

```
make download_model
```

This will download
the [RFCN FP32 inference](https://github.com/IntelAI/models/blob/master/benchmarks/object_detection/tensorflow/rfcn/inference/fp32/README.md)
model under the name rfcn.

### Using different models

To use different models you can place them under the `tmp/model/` path using the following structure:
`tmp/model/modelname/versionnumber/`. Then append the model name when making a request and the app will use the
specified model, if it exists.

## Testing the app

### Using docker

The easiest way to launch the app is using docker compose, first you'll need to create an `.env` file using
the `.env_example` provided and then launching

```bash
docker compose up
```

and then opening the web interface at http://localhost:5000

### Using make

#### Setup and run Tensorflow Serving

```
make tensorflow_serving
```

#### Run mongo

```bash
make mongo
```

#### Setup virtualenv

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the application

### Using docker

If using docker, the application will start automatically on port 5000, you can then open
[http://localhost:5000/](http://localhost:5000/) to test the application using the Swagger UI

### Using fakes

Set the ENV variable to dev inside the `docker-compose.yml` file or run the following:

```
python -m counter.entrypoints.webapp
```

### Using real services in docker containers

Set the ENV variable to prodc inside the `docker-compose.yml` file or run the following:

```
ENV=prod python -m counter.entrypoints.webapp
```

## Call the service

### Using the REST endpoints

You can call the service using the Swagger UI or using cURL:

```shell script
 curl -F "threshold=0.9" -F "file=@resources/images/boy.jpg" http://0.0.0.0:5000/object-count
 curl -F "threshold=0.9" -F "file=@resources/images/cat.jpg" http://0.0.0.0:5000/object-count
 curl -F "threshold=0.9" -F "file=@resources/images/food.jpg" http://0.0.0.0:5000/object-count
```

If you wish to specify the model name to use for inference you can do so passing the `model_name` option:

```shell script
 curl -F "model_name=rfcn" -F "threshold=0.9" -F "file=@resources/images/boy.jpg" http://0.0.0.0:5000/object-count
```

### Using the CLI

#### Counting objects

```bash
python -m counter.entrypoints.main count --img-path resources/images/food.jpg --threshold 0.9
```

#### Getting predictions

```bash
python -m counter.entrypoints.main predict --img-path resources/images/food.jpg --threshold 0.9
```

## Run the tests

```
pytest
```