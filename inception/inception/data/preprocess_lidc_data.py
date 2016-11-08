import shutil
import random
import dicom
import os
import numpy
from PIL import Image
import matplotlib.cm as cm
import pylab
import sqlite3


db_filename = '/Users/jacksonkontny/Projects/DePaul/csc481/CT_norm_002.sql3'
dicom_path = '/Users/jacksonkontny/Projects/DePaul/csc481/' # LIDC/LIDC_IRDI/'
TRAINING_DATA_DIR = 'raw_data'
CLASSIFICATION_TYPES = ['malignant', 'benign']
TRAINING_SETS = ['train', 'validation']


def get_lidc_files(lidc_path):
    dcm_files_list = []  # create an empty list
    for dirName, subdirList, fileList in os.walk(lidc_path):
        for filename in fileList:
            if ".dcm" in filename.lower():  # check whether the file's DICOM
                dcm_files_list.append(os.path.join(dirName, filename))
    return dcm_files_list

def create_or_clean_data_directories(dicom_Path):
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
    data_dir_name = os.path.join(dicom_path, TRAINING_DATA_DIR)
    create_or_clean(data_dir_name)
    for training_dir in TRAINING_SETS:
        training_dir_name = os.path.join(data_dir_name, training_dir)
        create_or_clean(training_dir_name)
        for classification in CLASSIFICATION_TYPES:
            classification_dir_name = os.path.join(training_dir_name, classification)
            create_or_clean(classification_dir_name)

def create_training_and_validation_sets(preprocessed_files, training_pct=.95):
    training = random.sample(lidc_files, int(len(lidc_files) * training_pct))
    validation = set(lidc_files) - set(training)
    return list(training), list(validation)

def process_lidc_files(lidc_files, conn):
    data_dir = os.path.join(dicom_path, TRAINING_DATA_DIR)
    def process_file_set(data_set, data_set_name):
        for lidc_file in data_set:
            dc = dicom.read_file(lidc_file , force=True)
            classification = get_classification(dc.SOPInstanceUID, conn)
            classification_dir = os.path.join(data_dir, data_set_name, classification)
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
    lidc_files = get_lidc_files(dicom_path)
    create_or_clean_data_directories(dicom_path)
    with sqlite3.connect(db_filename) as conn:
        process_lidc_files(lidc_files, conn)
