import npath
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
dicom_path = '/Users/jacksonkontny/Projects/DePaul/csc481/LIDC/LIDC_IRDI/'

def get_lidc_files(lidc_path):
    dcm_files_list = []  # create an empty list
    for dirName, subdirList, fileList in os.walk(lidc_path):
        for filename in fileList:
            if ".dcm" in filename.lower():  # check whether the file's DICOM
                dcm_files_list.append(os.path.join(dirName, filename))
    return dcm_files_list

def process_lidc_files(lidc_files, conn):
    preprocessed_files = []
    for lidc_file in lidc_files:
        dc = dicom.read_file(lidc_file , force=True)
        classification = get_classification(dc.SOPInstanceUID, conn)
        px_array = dc.pixel_array
        out_file_name = '%sraw_data/%s/%s_%s.jpeg' % (dicom_path, classification, str(dc.PatientID), str(dc.InstanceNumber))
        pylab.imsave(out_file_name, px_array, cmap=cm.Greys_r)
        preprocessed_files.append(out_file_name)
    return preprocessed_files

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

def create_training_and_validation_sets(preprocessed_files):
    training = random.sample(lidc_files, int(len(lidc_files) * .95))
    validation = set(lidc_files) - set(training)
    for fn in training:
        shutil.move(fn, '%sraw_data/train/%s' % (dicom_path, npath.basename(fn)))
    for fn in validation:
        shutil.move(fn, '%sraw_data/validation/%s' % (dicom_path, npath.basename(fn)))

if __name__ == "__main__":
    lidc_files = get_lidc_files(dicom_path)
    with sqlite3.connect(db_filename) as conn:
        preprocessed_files = process_lidc_files(lidc_files, conn)
    create_training_and_validation_sets(preprocessed_files)
