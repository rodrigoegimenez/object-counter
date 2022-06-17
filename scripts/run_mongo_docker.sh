docker rm -f test-mongo
docker run --name test-mongo --rm --net host -d mongo:latest