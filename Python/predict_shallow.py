import argparse
from glob import glob
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix
from timeit import default_timer
from data_analysis import summarize_sensor_trace 
import os

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
    

# this function formats the sample we recieve so that it can fit into our ML model
def format_sample(data_file):
    # call our previous function from data_analysis file
    mean, var = summarize_sensor_trace(data_file)
    mean = np.array(mean)
    var = np.array(var)

    # RELEVANT FEATURES FOR MEAN
    # left and right controller angular velocity in y direction
    # left and right controller position in y direction
    # headset position in y direction
    features_mean_index = np.array([16, 28, 19, 31, 7])

    # RELEVANT FEATURES FOR VARIANCE
    # headset velocity in y direction
    # headset angular velocity in y direction
    # left and right controller velocities in all directions
    features_var_index = np.array([1, 12, 13, 14, 24, 25, 26, 4])

    extracted_features = np.concatenate((mean[features_mean_index.astype(int)], var[features_var_index.astype(int)]))
    return extracted_features

# this is where we create our classifier with the training data
train_folder = "Python/Train"
data_files = glob(f"{train_folder}/*.csv")
np.random.shuffle(data_files)

training_data = np.empty((len(data_files), 13)) # 13 because we chose 13 features
training_labels = np.chararray((len(data_files)), itemsize=3)

for i in range(len(data_files)):
    feature_vector = format_sample(data_files[i])
    training_data[i] = feature_vector
    training_labels[i] = os.path.basename(data_files[i])[:3]

rf = RandomForestClassifier(n_estimators=100)
rf.fit(training_data, training_labels)

"""
Create a non-deep learning classifier (e.g. multiclass SVM, decision tree, random forest)
to perform activity detection that improves upon your prior algorithm.

Usage:
    
    python3 Python/predict_shallow.py <sensor .csv sample>

    python3 Python/predict_shallow.py --label_folder <folder with sensor .csv samples>
"""
# store our predictions every time predict_shallow is called
prediction_labels = np.chararray(0, itemsize=3)

def predict_shallow(sensor_data: str) -> str:
    """Run prediction on an sensor data sample.

    Replace the return value of this function with the output activity label
    of your shallow classifier for the given sample. Feel free to load any files and write
    helper functions as needed.
    """
    feature_vector = format_sample(sensor_data)
    prediction = rf.predict(np.array(feature_vector).reshape(1, -1))
    
    global prediction_labels 
    prediction_labels = np.append(prediction_labels, prediction[0].decode('utf-8'))
    return prediction[0].decode('utf-8') 


def predict_shallow_folder(data_folder: str, output: str):
    """Run the model's prediction on all the sensor data in data_folder, writing labels
    in sequence to an output text file."""

    data_files = sorted(glob(f"{data_folder}/*.csv"))
    labels = map(predict_shallow, data_files)

    with open(output, "w+") as output_file:
        output_file.write("\n".join(labels))


if __name__ == "__main__":
    # Parse arguments to determine whether to predict on a file or a folder
    # You should not need to modify the below starter code, but feel free to
    # add more arguments for debug functions as needed.
    tstart = default_timer() # to time how long our algorithm takes to run
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
        default="Data/Lab2/Labels/shallow.txt",
        help="Output filename of labels when running predictions on a directory",
    )

    args = parser.parse_args()

    if args.sample:
        print(predict_shallow(args.sample))

    elif args.label_folder:
        predict_shallow_folder(args.label_folder, args.output)

    # create_validation_array()
    
    # precision score for each activity
    # p_score = precision_score(validation_labels, prediction_labels, labels=["JOG", "STD", "SIT", "STR", "OHD", "TWS"], average=None)

    # average precision score for all activities
    # p_score_avg = precision_score(validation_labels, prediction_labels, labels=["JOG", "STD", "SIT", "STR", "OHD", "TWS"], average='macro')
    
    # average accuracy score for all activities
    # a_score = accuracy_score(validation_labels, prediction_labels)

    # got from https://stackoverflow.com/questions/39770376/scikit-learn-get-accuracy-scores-for-each-class
    # this gives accuracy score for each activity
    # cm = confusion_matrix(validation_labels, prediction_labels)
    # cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    # print(["JOG", "STD", "SIT", "STR", "OHD", "TWS"])
    # print(cm.diagonal())

    # print(p_score)
    # print(p_score_avg)
    # print(a_score)

    tend = default_timer()
    # print("Total Runtime: %.2f sec"%(tend-tstart))
