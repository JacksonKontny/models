import shutil
import random
import dicom
import os
import numpy
from PIL import Image
import matplotlib.cm as cm
import pylab
import sqlite3


BASE_PATH = '/Users/jacksonkontny/Projects/DePaul/csc481/'
DATA_PATH = os.path.join(BASE_PATH, 'LIDC', 'LIDC_IDRI')
DB_FILENAME = os.path.join(BASE_PATH, 'CT_norm_002.sql3')
RAW_DATA_PATH = os.path.join(DATA_PATH, 'raw_data')
PREPROCESSED_DATA_PATH = os.path.join(DATA_PATH, 'preprocessed_data_even_split')
CLASSIFICATION_TYPES = ['malignant', 'benign']
TRAINING_SETS = ['train', 'validation']
NUM_SAMPLES = 0 # set to a number if you only want to get a small sample


def get_lidc_files():
    dcm_files_list = []  # create an empty list
    for dirName, subdirList, fileList in os.walk(RAW_DATA_PATH):
        for filename in fileList:
            if ".dcm" in filename.lower():  # check whether the file's DICOM
                dcm_files_list.append(os.path.join(dirName, filename))
    if NUM_SAMPLES:
        dcm_files_list = dcm_files_list[:NUM_SAMPLES]
    return dcm_files_list

def create_or_clean_data_directories():
    ''' creates directories for each training set and subdirectories for each
        classification type under each training set, for a total of trainig
        set * classification type directores.

        CAUTION: this will delete all training data you have populated in the
        training and classification directories.
    '''
    def create_or_clean(dir_name):
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
        else:
            shutil.rmtree(dir_name)
            os.mkdir(dir_name)
    create_or_clean(PREPROCESSED_DATA_PATH)
    for training_dir in TRAINING_SETS:
        training_dir_name = os.path.join(PREPROCESSED_DATA_PATH, training_dir)
        create_or_clean(training_dir_name)
        for classification in CLASSIFICATION_TYPES:
            classification_dir_name = os.path.join(training_dir_name, classification)
            create_or_clean(classification_dir_name)

def create_training_and_validation_sets(preprocessed_files, training_pct=.95):
    training = random.sample(lidc_files, int(len(lidc_files) * training_pct))
    validation = set(lidc_files) - set(training)
    return sorted(list(training)), sorted(list(validation))

def process_lidc_files(lidc_files, conn):
    def process_file_set(data_set, data_set_name):
        num_malignant = 0
        num_benign = 0
        for lidc_file in data_set:
            dc = dicom.read_file(lidc_file , force=True)
            classification = get_classification(dc.SOPInstanceUID, conn)
            if classification == 'malignant':
                num_malignant += 1
            else:
                if num_benign > num_malignant:
                    continue
                num_benign += 1
            classification_dir = os.path.join(PREPROCESSED_DATA_PATH, data_set_name, classification)
            px_array = dc.pixel_array
            out_file_name = '{}_{}.jpeg'.format(str(dc.PatientID), str(dc.InstanceNumber))
            out_file_path = os.path.join(classification_dir, out_file_name)
            pylab.imsave(out_file_path, px_array, cmap=cm.Greys_r)

    training_set, validation_set = create_training_and_validation_sets(lidc_files)
    process_file_set(training_set, 'train')
    process_file_set(validation_set, 'validation')

def get_classification(image_sop_uid, conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        select count(imageSOP_UID) from master
        where malignancy > 2 and imageSOP_UID=:imageSOP_UID;
        """, {'imageSOP_UID': image_sop_uid}
    )
    count = cursor.fetchone()[0]
    return 'malignant' if count else 'benign'


if __name__ == "__main__":
    lidc_files = get_lidc_files()
    create_or_clean_data_directories()
    with sqlite3.connect(DB_FILENAME) as conn:
        process_lidc_files(lidc_files, conn)
