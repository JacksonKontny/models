#!/bin/bash
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# Create the output and temporary directories.
BASE_DIR="${1%/}"
EXPERIMENT_NAME="base"
EXPERIMENT_DIR="${BASE_DIR}/inception/${EXPERIMENT_NAME}"
PROCESSED_DATA_PATH="${EXPERIMENT_DIR}/processed_data/"
DATE_TIME=`date '+%Y.%m.%d-%H.%M.%S'`
TRAIN_DIR="${EXPERIMENT_DIR}/${DATE_TIME}-train"

mkdir -p "${TRAIN_DIR}"
WORK_DIR="$0.runfiles/inception/inception"

BUILD_SCRIPT="${WORK_DIR}/lidc_train"

"${BUILD_SCRIPT}" \
  --num_gpus=1 \
  --batch_size=32 \
  --train_dir="${TRAIN_DIR}" \
  --data_dir="${DATA_DIR}"
