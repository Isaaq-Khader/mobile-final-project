import numpy as np
import pandas as pd
import glob
import os
import shutil

labeled_folder = "../Data/Lab2/Labeled/"
train_folder = "../Data/Lab2/Train/"
validation_folder = "../Data/Lab2/Validation/"

activites = ["JOG_*", "OHD_*", "SIT_*", "STD_*", "STR_*", "TWS_*"]

'''
If there are existing files already in the training and validation folders,
this will remove them so that no duplicates occur.

Inputs: None
Returns: None
'''
def check_if_empty_folders():
    dir = os.listdir(train_folder)

    # if there is data in the train and validation folder, remove all the contents
    if len(dir) != 0:
        train_files = glob.glob(train_folder)
        validation_files = glob.glob(validation_folder)
        
        for file in train_files:
            os.remove(file)
        
        for file in validation_files:
            os.remove(file)

'''
Given a folder of data, will perform a 15%/85% train/test split in respective folders.

Input: a folder

Returns: None
'''
def split_data(folder_name):
    
    check_if_empty_folders()
    
    validate = 21 # 15% of 140 is 21

    # for each activity, split into train and validation datasets
    for activity in activites: 

        curr_glob = glob.glob(labeled_folder + activity)
        num_files = len(curr_glob)
              
        # creates a list of randomly permuated numbers
        random_split = np.random.permutation(num_files)
        
        validate_mask = random_split[:validate]
        train_mask = random_split[validate:]

        validate_csvs = np.array(curr_glob)[validate_mask.astype(int)]
        train_csvs = np.array(curr_glob)[train_mask.astype(int)]

        for csv in validate_csvs:
            shutil.copyfile(csv, validation_folder + os.path.basename(csv))
        
        for csv in train_csvs:
            shutil.copyfile(csv, train_folder + os.path.basename(csv))
            
    return


split_data(labeled_folder)