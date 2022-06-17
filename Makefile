PHONY=serving mongo app

model_download:
	./scripts/model_download.sh

serving:
	./scripts/run_tensorflow_serving.sh

mongo:
	./scripts/run_mongo_docker.sh

app:
	python -m counter.entrypoints.webapp