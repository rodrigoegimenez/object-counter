#!/usr/bin/env sh

set -e

model_name=rfcn
cores_per_socket=$(lscpu | grep "Core(s) per socket" | cut -d':' -f2 | xargs)
num_sockets=$(lscpu | grep "Socket(s)" | cut -d':' -f2 | xargs)
num_physical_cores=$((cores_per_socket * num_sockets))
echo $num_physical_cores

docker rm -f tfserving

docker run \
    --name=tfserving \
    -d \
    -p 8500:8500 \
    -p 8501:8501 \
    -v "$(pwd)/tmp/model:/models/$model_name" \
    -e MODEL_NAME=$model_name \
    -e OMP_NUM_THREADS=$num_physical_cores \
    -e TENSORFLOW_INTER_OP_PARALLELISM=2 \
    -e TENSORFLOW_INTRA_OP_PARALLELISM=$num_physical_cores \
    intel/intel-optimized-tensorflow-serving:2.3.0
