import numpy as np 
import pandas as pd 
import glob
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from natsort import index_natsorted
import os

'''
Reconfigs rotation degrees to go from [0, 360) to [-180, 180) for the sake of
graphing.

Inputs:
    csvFile: a csvFile

Returns:
    new dataframe
'''
def reconfig_rot(csvFile):
    df = pd.read_csv(csvFile)

    df["controller_left_rot.x"] = np.where(df["controller_left_rot.x"] > 180, df["controller_left_rot.x"] - 360, df["controller_left_rot.x"])
    df["controller_left_rot.y"] = np.where(df["controller_left_rot.x"] > 180, df["controller_left_rot.x"] - 360, df["controller_left_rot.x"])
    df["controller_left_rot.z"] = np.where(df["controller_left_rot.x"] > 180, df["controller_left_rot.x"] - 360, df["controller_left_rot.x"])


    df["controller_right_rot.x"] = np.where(df["controller_right_rot.x"] > 180, df["controller_right_rot.x"] - 360, df["controller_right_rot.x"])
    df["controller_right_rot.y"] = np.where(df["controller_right_rot.y"] > 180, df["controller_right_rot.y"] - 360, df["controller_right_rot.y"])
    df["controller_right_rot.z"] = np.where(df["controller_right_rot.z"] > 180, df["controller_right_rot.z"] - 360, df["controller_right_rot.z"])


    df["headset_rot.x"] = np.where(df["headset_rot.x"] > 180, df["headset_rot.x"] - 360, df["headset_rot.x"])
    df["headset_rot.y"] = np.where(df["headset_rot.y"] > 180, df["headset_rot.y"] - 360, df["headset_rot.y"])
    df["headset_rot.z"] = np.where(df["headset_rot.z"] > 180, df["headset_rot.z"] - 360, df["headset_rot.z"])

    return df

'''
Provides a statistical summary for a given csv file.

Input:
    csv_file: a csv file

returns:
    Mean and variance arrays

'''
def summarize_sensor_trace(csv_file: str):
    df = pd.read_csv(csv_file)
  
    means = []
    vars = []

    for column in df:
        mean = df[column].mean() 
        var = df[column].var()

        means.append(mean)
        vars.append(var)
    
    return means[1:-1], vars[1:-1]

'''
Visualizes an attribute for a given activity.

Input:
    csv_file: a csv file
    attribute: desired attribute to be graphed
    activity: activity for which the attribute is being graphed

'''
def visualize_sensor_trace(csv_file: str, attribute: str, activity: str):

    df = pd.read_csv(csv_file)

    attribute_arr = np.array(df[attribute])
    times = np.array(df["time"])

    plt.xlabel("time (ms)")
    plt.ylabel(attribute)
    plt.title(attribute + " vs. time for " + activity)
    plt.scatter(times, attribute_arr, s=5, alpha= 0.5)

    plt.show()

'''
Agglomerates all data for a given activity across all trials and all persons.

Inputs:
    files: glob array of csv files corresponding to an activity
    columns: array of feature names

Returns:
    agglomerated csv file
'''
def concat_data(files, columns):
    
    return_df = pd.DataFrame(columns=columns)

    for file in files:

        df = pd.read_csv(file)
        return_df = pd.concat([return_df, df], axis=0, ignore_index=True)

    #source: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html
    return_df.sort_values(
                by="time",
                key=lambda x: np.argsort(index_natsorted(return_df["time"]))
                )
    
    return return_df

concat_dir = '../concated_data/'

get_columns = ["time", "headset_vel.x", "headset_vel.y", "headset_vel.z", 
               "headset_angularVel.x" ,"headset_angularVel.y" ,"headset_angularVel.z" ,
               "headset_pos.x", "headset_pos.y", "headset_pos.z", 
               "headset_rot.x", "headset_rot.y", "headset_rot.z", 
               "controller_left_vel.x", "controller_left_vel.y", "controller_left_vel.z",
               "controller_left_angularVel.x", "controller_left_angularVel.y", "controller_left_angularVel.z", 
               "controller_left_pos.x,", "controller_left_pos.y", "controller_left_pos.z", 
               "controller_left_rot.x", "controller_left_rot.y", "controller_left_rot.z", 
               "controller_right_vel.x", "controller_right_vel.y", "controller_right_vel.z",
               "controller_right_angularVel.x", "controller_right_angularVel.y", "controller_right_angularVel.z",
               "controller_right_pos.x", "controller_right_pos.y", "controller_right_pos.z", 
               "controller_right_rot.x", "controller_right_rot.y", "controller_right_rot.z"]

'''
Creates and stores agglomerated csv files.

Inputs:
    csvFiles: csv files to be agglomerated
    csvName: name of features

'''
def create_compiled_csv(csvFiles, csvName):
 
    concat_activity = concat_data(csvFiles, get_columns)

    os.makedirs(concat_dir, exist_ok=True)  
    concat_activity.to_csv(concat_dir + csvName)


def calc_mean_per_sample(files):
    df_concat = pd.DataFrame(columns=get_columns)
    for file in files:
        df = pd.read_csv(file)
        curr_df_mean = df.mean()
        df_concat = pd.concat([df_concat, pd.DataFrame(curr_df_mean).T], axis=0, ignore_index=True)
    
    df_mean_mean = df_concat.mean()
    
    return df_mean_mean

def calc_var_per_sample(files):
    df_concat = pd.DataFrame(columns=get_columns)
    for file in files:
        df = pd.read_csv(file)
        df_var = df.var()
        df_concat = pd.concat([df_concat, pd.DataFrame(df_var).T], axis=0, ignore_index=True)
    df_var_mean = df_concat.mean()

    return df_var_mean



#below is some example use of the above functions.

super_mean_samples_csv = pd.DataFrame(columns=get_columns)
super_var_samples_csv = pd.DataFrame(columns=get_columns)

# jog = glob.glob("../Data/Lab2/Train/JOG_*")
# create_compiled_csv(jog, "/concat_jog.csv")
# #jog_mean, jog_var = summarize_sensor_trace(concat_dir + "/concat_jog.csv")
# #visualize_sensor_trace(concat_dir + "/concat_jog.csv", "headset_angularVel.y", "jogging")
# jog_means = calc_mean_per_sample(jog)
# jog_vars = calc_var_per_sample(jog)
# super_mean_samples_csv = pd.concat([super_mean_samples_csv, pd.DataFrame(jog_means).T], axis=0, ignore_index=True)
# super_var_samples_csv = pd.concat([super_var_samples_csv, pd.DataFrame(jog_vars).T], axis=0, ignore_index=True)


# ohd = glob.glob("../Data/Lab2/Train/OHD_*")
# create_compiled_csv(ohd, "/concat_overhead.csv")
# #ohd_mean, ohd_var = summarize_sensor_trace(concat_dir + "/concat_overhead.csv")
# #visualize_sensor_trace(concat_dir + "/concat_overhead.csv", "headset_angularVel.y", "overhead")
# ohd_means = calc_mean_per_sample(ohd)
# ohd_vars = calc_var_per_sample(ohd)
# super_mean_samples_csv = pd.concat([super_mean_samples_csv, pd.DataFrame(ohd_means).T], axis=0, ignore_index=True)
# super_var_samples_csv = pd.concat([super_var_samples_csv, pd.DataFrame(ohd_vars).T], axis=0, ignore_index=True)



#sit = glob.glob("../Data/Lab1/SIT_*") // for the data we recorded
sit = glob.glob("../Data/Lab2/Train/SIT_*")
create_compiled_csv(sit, "concat_sit.csv")
sit_mean, sit_var = summarize_sensor_trace(concat_dir + "/concat_sit.csv")
#visualize_sensor_trace(concat_dir + "/concat_sit.csv", "headset_angularVel.y", "sitting")
sit_means = calc_mean_per_sample(sit)
sit_vars = calc_var_per_sample(sit)
# print(sit_means)
# print(sit_vars)
# super_mean_samples_csv = pd.concat([super_mean_samples_csv, pd.DataFrame(sit_means).T], axis=0, ignore_index=True)
# super_var_samples_csv = pd.concat([super_var_samples_csv, pd.DataFrame(sit_vars).T], axis=0, ignore_index=True)


# std = glob.glob("../Data/Lab2/Train/STD_*")
# create_compiled_csv(std, "/concat_stand.csv")
# #std_mean, std_var = summarize_sensor_trace(concat_dir + "/concat_stand.csv")
# #visualize_sensor_trace(concat_dir + "/concat_stand.csv", "headset_angularVel.y", "stand")
# std_means = calc_mean_per_sample(std)
# std_vars = calc_var_per_sample(std)
# super_mean_samples_csv = pd.concat([super_mean_samples_csv, pd.DataFrame(std_means).T], axis=0, ignore_index=True)
# super_var_samples_csv = pd.concat([super_var_samples_csv, pd.DataFrame(std_vars).T], axis=0, ignore_index=True)


# stretch = glob.glob("../Data/Lab2/Train/STR_*")
# create_compiled_csv(stretch, "/concat_stretch.csv")
# #stretch_mean, stretch_var = summarize_sensor_trace(concat_dir + "/concat_stretch.csv")
# #visualize_sensor_trace(concat_dir + "/concat_stretch.csv", "controller_right_angularVel.y", "stretch")
# stretch_means = calc_mean_per_sample(stretch)
# stretch_vars = calc_var_per_sample(stretch)
# super_mean_samples_csv = pd.concat([super_mean_samples_csv, pd.DataFrame(stretch_means).T], axis=0, ignore_index=True)
# super_var_samples_csv = pd.concat([super_var_samples_csv, pd.DataFrame(stretch_vars).T], axis=0, ignore_index=True)

# tws = glob.glob("../Data/Lab2/Train/TWS_*")
# create_compiled_csv(tws, "/concat_twist.csv")
# #twist_mean, twist_var = summarize_sensor_trace(concat_dir + "/concat_twist.csv")
# #visualize_sensor_trace(concat_dir + "/concat_twist.csv", "controller_left_angularVel.y", "twist")
# tws_means = calc_mean_per_sample(tws)
# tws_vars = calc_var_per_sample(tws)
# super_mean_samples_csv = pd.concat([super_mean_samples_csv, pd.DataFrame(tws_means).T], axis=0, ignore_index=True)
# super_var_samples_csv = pd.concat([super_var_samples_csv, pd.DataFrame(tws_vars).T], axis=0, ignore_index=True)


# super_mean_samples_csv.to_csv("../concated_data/super_mean_samples.csv")
# super_var_samples_csv.to_csv("../concated_data/super_var_samples.csv")