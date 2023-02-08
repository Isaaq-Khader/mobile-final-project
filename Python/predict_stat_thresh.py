import numpy as np
import pandas as pd
import argparse
from glob import glob
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix
from timeit import default_timer
from data_analysis import summarize_sensor_trace 
import os

"""
Examine the mean and variance of each activity’s sensor data, and build a statistical 
threshold-based classifier for activity detection.

Usage:
    
    python3 Python/predict_stat_thresh.py <sensor .csv sample>

    python3 Python/predict_stat_thresh.py --label_folder <folder with sensor .csv samples>
"""

# this is where we create our validation labels to be compared within the classfier
test_folder = "Data/Lab2/Validation"
validation_files = sorted(glob(f"{test_folder}/*.csv"))
validation_labels = np.chararray(0, itemsize=3)

# this function creates the validation labels for the global variable storing these values
def create_validation_array():
    global validation_files
    global validation_labels

    for i in range(len(validation_files)):
        new_name = os.path.basename(validation_files[i])[:3]
        validation_labels = np.append(validation_labels, new_name)

# folder locations for data
data_folder = "Python/csv_data/"
means_csv = "mean_samples.csv"
vars_csv = "var_samples.csv"
sd_csv = "sd_samples.csv"
labeled_folder = "Python/Train/"

# grab means, vars, and SDs for each activity that we calculated per training sample 
df_means = pd.read_csv(data_folder + means_csv)
df_vars = pd.read_csv(data_folder + vars_csv)
df_sd = pd.read_csv(data_folder + sd_csv)

# store our predictions every time predict_stat_thresh is called
prediction_labels = np.chararray(0, itemsize=3)

def predict_stat_thresh(sensor_data_path: str) -> str:
    """Run prediction on a sensor data sample.

    Replace the return value of this function with the output activity label
    of your stat-based threshold model. Feel free to load any files and write
    helper functions as needed.
    """

    global prediction_labels

    # get the mean and var from the given sample
    mean, var = summarize_sensor_trace(sensor_data_path)

    # calculate standard deviation from var
    sd = np.sqrt(var)

    # get left and right controller variances for velocity in y direction for predicting overhead
    ohd_l_controller_vel_y_var = df_vars.iloc[1, 15]
    ohd_r_controller_vel_y_var = df_vars.iloc[1, 27]

    # take difference in vars for predicting overhead
    ohd_l_controller_vel_y_var_diff = abs(ohd_l_controller_vel_y_var - var[13])
    ohd_r_controller_vel_y_var_diff = abs(ohd_r_controller_vel_y_var - var[25])

    # get headset standard deviation for angular velocity in y direction
    tws_headset_ang_vel_y_sd = df_sd.iloc[5, 6]

    # take difference of SD's for predicting twist activity
    tws_sd_diff = abs(tws_headset_ang_vel_y_sd - sd[4])

    # get left and right controller mean for angular velocity in y direction for predicting stretch
    str_l_controller_angularvel_y_mean = df_means.iloc[4, 18]
    str_r_controller_angularvel_y_mean = df_means.iloc[4, 30]

    # if the variances for velocity are low, this means we are either sitting or standing
    r_controller_vel_var = var[24] < 0.01 and var[25] < 0.01 and var[26] < 0.01
    l_controller_vel_var = var[12] < 0.01 and var[13] < 0.01 and var[14] < 0.01

    # get headset variances for velocity in y direction for predicting jogging
    jog_headset_vel_y_var = df_vars.iloc[0, 3]
    jog_headset_vel_y_cond_var = abs(jog_headset_vel_y_var - var[1]) < 0.15
    
    if (tws_sd_diff < 0.75 or sd[4] > tws_headset_ang_vel_y_sd):
        prediction_labels = np.append(prediction_labels, "TWS")
        return "TWS"
    elif (r_controller_vel_var and l_controller_vel_var):
        # if we enter here, the activity is either sitting or standing

        # take difference of y-direction distances from headset to each controller
        sit_headset_to_l_controller_y_dist_diff_mean = abs(df_means.iloc[2, 9] - df_means.iloc[2, 21])
        sit_headset_to_r_controller_y_dist_diff_mean = abs(df_means.iloc[2, 9] - df_means.iloc[2, 33])
            
        # get headset mean and SD for y position for standing 
        sit_headset_y_pos_mean = df_means.iloc[2, 9]
        sit_headset_y_pos_sd = df_sd.iloc[2, 9]

        # get headset mean and SD for y position for sitting
        stand_headset_y_pos_mean = df_means.iloc[3, 9]
        stand_headset_y_pos_sd = df_sd.iloc[3, 9]

        if(sit_headset_y_pos_mean - 10*sit_headset_y_pos_sd) <= (mean[7]) <= (sit_headset_y_pos_mean + 10*sit_headset_y_pos_sd):
            prediction_labels = np.append(prediction_labels, "SIT")
            return "SIT"
        elif (stand_headset_y_pos_mean - 7*stand_headset_y_pos_sd) <= (mean[7]) <= (stand_headset_y_pos_mean + 7*stand_headset_y_pos_sd):
            prediction_labels = np.append(prediction_labels, "STD")
            return "STD"
        else:
            if (abs(sit_headset_to_l_controller_y_dist_diff_mean - abs(mean[7] - mean[19])) < 0.25 and
                    abs(sit_headset_to_r_controller_y_dist_diff_mean - abs(mean[7] - mean[31])) < 0.25):
                prediction_labels = np.append(prediction_labels, "SIT")
                return "SIT"
            else:
                prediction_labels = np.append(prediction_labels, "STD")
                return "STD"
    elif (jog_headset_vel_y_cond_var):
        prediction_labels = np.append(prediction_labels, "JOG")
        return "JOG"
    elif (ohd_l_controller_vel_y_var_diff < 0.5 and ohd_r_controller_vel_y_var_diff < 0.5):
        prediction_labels = np.append(prediction_labels, "OHD")
        return "OHD"
    elif(abs(str_l_controller_angularvel_y_mean - mean[16]) < 0.15 and abs(str_r_controller_angularvel_y_mean - mean[28]) < 0.15):
        prediction_labels = np.append(prediction_labels, "STR")
        return "STR"
    else: 
        prediction_labels = np.append(prediction_labels, "JOG")
        return "JOG" # default case is JOG


def predict_stat_thresh_folder(data_folder: str, output_file: str):
    """Run the model's prediction on all the sensor data in data_folder, writing labels
    in sequence to an output text file."""

    data_files = sorted(glob(f"{data_folder}/*.csv"))
    labels = map(predict_stat_thresh, data_files)

    with open(output_file, "w") as output_file: #changed from append to rewrite entire thing add"+" when you wanna go back
        output_file.write("\n".join(labels))


if __name__ == "__main__":
    # Parse arguments to determine whether to predict on a file or a folder
    # You should not need to modify the below starter code, but feel free to
    # add more arguments for debug functions as needed.
    tstart = default_timer()
    parser = argparse.ArgumentParser()

    sample_input = parser.add_mutually_exclusive_group(required=True)
    sample_input.add_argument(
        "sample", nargs="?", help="A .csv sensor data file to run predictions on"
    )
    sample_input.add_argument(
        "--label_folder",
        type=str,
        required=False,
        help="Folder of .csv data files to run predictions on",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="Data/Lab2/Labels/stat.txt",
        help="Output filename of labels when running predictions on a directory",
    )

    args = parser.parse_args()
    if args.sample:
        print(predict_stat_thresh(args.sample))

    elif args.label_folder:
        predict_stat_thresh_folder(args.label_folder, args.output)


    # create_validation_array()

    # got from https://stackoverflow.com/questions/39770376/scikit-learn-get-accuracy-scores-for-each-class
    # this gives accuracy score for each activity
    # cm = confusion_matrix(validation_labels, prediction_labels)
    # cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    # print(["JOG", "STD", "SIT", "STR", "OHD", "TWS"])
    # print(cm.diagonal())

    # precision score for each activity
    # p_score = precision_score(validation_labels, prediction_labels, labels=["JOG", "STD", "SIT", "STR", "OHD", "TWS"], average=None)

    # average precision score for all activities
    # p_score_avg = precision_score(validation_labels, prediction_labels, labels=["JOG", "STD", "SIT", "STR", "OHD", "TWS"], average='macro')

    # average accuracy score for all activities
    # a_score = accuracy_score(validation_labels, prediction_labels)
    # print(p_score)
    # print(p_score_avg)
    # print(a_score)

    tend = default_timer()
    # print("Total Runtime: %.2f sec" % (tend-tstart))

