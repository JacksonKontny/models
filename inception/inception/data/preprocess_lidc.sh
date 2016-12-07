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

# Create the output and temporary directories.
# DATA_DIR="${1%/}"
BASE_DIR="/Users/jacksonkontny/Projects/DePaul/csc481/"
DATA_DIR="${BASE_DIR}/LIDC/LIDC_IDRI"
PREPROCESSED_DIR="${DATA_DIR}/preprocessed_data_even/"
PROCESSED_DIR="${DATA_DIR}/processed_data_even/"
mkdir -p "${DATA_DIR}"
mkdir -p "${PREPROCESSED_DIR}"
mkdir -p "${PROCESSED_DIR}"
WORK_DIR="$0.runfiles/inception/inception"

# Note the locations of the train and validation data.
TRAIN_DIRECTORY="${PREPROCESSED_DIR}train/"
VALIDATION_DIRECTORY="${PREPROCESSED_DIR}validation/"
LABELS_FILE="${WORK_DIR}/data/lidc_labels.txt"

# Build the TFRecords version of the ImageNet data.
BUILD_SCRIPT="${WORK_DIR}/build_lidc_data"
OUTPUT_DIRECTORY="${PROCESSED_DIR}"
LIDC_METADATA_FILE="${WORK_DIR}/data/lidc_annotations.txt"

"${BUILD_SCRIPT}" \
  --train_directory="${TRAIN_DIRECTORY}" \
  --validation_directory="${VALIDATION_DIRECTORY}" \
  --output_directory="${OUTPUT_DIRECTORY}" \
  --lidc_metadata_file="${LIDC_METADATA_FILE}" \
  --labels_file="${LABELS_FILE}" \
#   --bounding_box_file="${BOUNDING_BOX_FILE}"
