#!/usr/bin/env sh

set -e

wget \
  --no-verbose \
  --show-progress \
  --progress=dot:giga \
  https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/rfcn_resnet101_fp32_coco_pretrained_model.tar.gz

tar -xzvf rfcn_resnet101_fp32_coco_pretrained_model.tar.gz -C tmp
rm rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
chmod -R 777 tmp/rfcn_resnet101_coco_2018_01_28
mkdir -p tmp/model/rfcn/1
mv tmp/rfcn_resnet101_coco_2018_01_28/saved_model/saved_model.pb tmp/model/rfcn/1
rm -rf tmp/rfcn_resnet101_coco_2018_01_28
echo "Delete this file to force model download." >download_model

echo "Model downloaded, to download it again delete the file download_model from the root folder."
