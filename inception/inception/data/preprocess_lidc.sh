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

set -e

BASE_DIR="${1%/}"
EXPERIMENT_NAME="even_split"
RAW_DATA_DIR="${BASE_DIR}/LIDC_IDRI"
DB_FILENAME="${BASE_DIR}/sqlite_db/CT_norm_002.sql3"
PREPROCESSED_DATA_OUTPUT_PATH="${BASE_DIR}/inception/${EXPERIMENT_NAME}/preprocessed_data/"
PROCESSED_DATA_OUTPUT_PATH="${DATA_DIR}/inception/${EXPERIMENT_NAME}/processed_data/"
mkdir -p "${PREPROCESSED_DATA_OUTPUT_PATH}"
mkdir -p "${PROCESSED_DATA_OUTPUT_PATH}"
WORK_DIR="$0.runfiles/inception/inception/"

# Parse out trainig and validation records into labeled directories
PREPROCESS_SCRIPT="${WORK_DIR}preprocess_lidc_data"

"${PREPROCESS_SCRIPT}" \
  "${RAW_DATA_DIR}" \
  "${DB_FILENAME}" \
  "${PREPROCESSED_DATA_OUTPUT_PATH}" \

# Note the locations of the train and validation data.
TRAIN_DIRECTORY="${PREPROCESSED_DATA_OUTPUT_PATH}train/"
VALIDATION_DIRECTORY="${PREPROCESSED_DATA_OUTPUT_PATH}validation/"
LABELS_FILE="${WORK_DIR}data/lidc_labels.txt"

# Build the TFRecords version of the ImageNet data.
BUILD_SCRIPT="${WORK_DIR}build_lidc_data"
OUTPUT_DIRECTORY="${PROCESSED_DATA_OUTPUT_PATH}"
LIDC_METADATA_FILE="${WORK_DIR}data/lidc_annotations.txt"

"${BUILD_SCRIPT}" \
  --train_directory="${TRAIN_DIRECTORY}" \
  --validation_directory="${VALIDATION_DIRECTORY}" \
  --output_directory="${OUTPUT_DIRECTORY}" \
  --lidc_metadata_file="${LIDC_METADATA_FILE}" \
  --labels_file="${LABELS_FILE}" \
#   --bounding_box_file="${BOUNDING_BOX_FILE}"
