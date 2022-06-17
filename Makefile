PHONY=serving mongo app

download_model:
	./scripts/download_model.sh

tensorflow_serving:
	./scripts/run_tensorflow_serving.sh

mongo:
	./scripts/run_mongo_docker.sh

app:
	python -m counter.entrypoints.webapp