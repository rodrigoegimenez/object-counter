#!/usr/bin/env sh

ostype=$(uname)

if [ $ostype == "Linux" ]; then
  echo "Linux OS detected..."
  cores_per_socket=`lscpu | grep "Core(s) per socket" | cut -d':' -f2 | xargs`
  num_sockets=`lscpu | grep "Socket(s)" | cut -d':' -f2 | xargs`
  num_physical_cores=$((cores_per_socket * num_sockets))
elif [ $ostype == "Darwin" ]; then
  echo "Darwin OS detected..."
  num_physical_cores=$(sysctl -a | grep hw.physicalcpu: | cut -d':' -f2 | xargs)
fi
echo "The number of physical cores is: $num_physical_cores"
echo "Set TENSORFLOW_INTRA_OP_PARALLELISM=$num_physical_cores and \c"
echo "OMP_NUM_THREADS=$num_physical_cores inside the .env file"