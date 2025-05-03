# Imports
import os
import h5py
import argparse
import numpy as np
import indolocate
import indolocate.utils as utils

# Supress TF warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Dataset (WILD v2): https://www.kaggle.com/c/wild-v2

# Env 1
dataset1 = h5py.File("/mnt/LabData/datasets/indoor_localization/wild-v2/training_data_env1.h5", "r")
data1 = {
    "csi": np.array(dataset1["channels/real"]).T + 1j * np.array(dataset1["channels/imag"]).T,        # (samples, carriers, antennas, APs)
    "rssi": np.array(dataset1["rssi"]).T,                                                            # (samples, rssi)
    "labels": np.array(dataset1["labels"]).T,                                                        # (samples, true_pos)
    "opt": {
        "ant_sep": np.array(dataset1["opt/ANT_SEP"]).flatten()[0],                                   # scalar
        "center_freq": np.array(dataset1["opt/CENTER_FREQ"]).flatten()[0],                           # scalar
        "bw": np.array(dataset1["opt/BW"]).flatten()[0],                                             # scalar
    },
    "ap_locs": np.mean(np.array(dataset1["AP_locs"]), axis=1).T,                                     # (samples, coordinates)
}

# Env 2
dataset2 = h5py.File("/mnt/LabData/datasets/indoor_localization/wild-v2/training_data_env2.h5", "r")
data2 = {
    "csi": np.array(dataset2["channels/real"]).T + 1j * np.array(dataset2["channels/imag"]).T,        # (samples, carriers, antennas, APs)
    "rssi": np.array(dataset2["rssi"]).T,                                                            # (samples, rssi)
    "labels": np.array(dataset2["labels"]).T,                                                        # (samples, true_pos)
    "opt": {
        "ant_sep": np.array(dataset2["opt/ANT_SEP"]).flatten()[0],                                   # scalar
        "center_freq": np.array(dataset2["opt/CENTER_FREQ"]).flatten()[0],                           # scalar
        "bw": np.array(dataset2["opt/BW"]).flatten()[0],                                             # scalar
    },
    "ap_locs": np.mean(np.array(dataset2["AP_locs"]), axis=1).T,                                     # (samples, coordinates)
}

# Training Functions
def train_knn_rssi():

    if data1['rssi'] is None:
        print("Skipping KNN_RSSI with Env 1 (no data).")
    else:
        X_train1, Y_train1 = utils.get_trainset(data1['rssi'], data1['labels'])
        model1 = indolocate.init("knn")
        model1.fit(X_train1, Y_train1)
        model1.save("models/knn_rssi_env1_model.pkl")

    if data2['rssi'] is None:
        print("Skipping KNN_RSSI with ENV 2 (no data).")
    else:
        X_train2, Y_train2 = utils.get_trainset(data2['rssi'], data2['labels'])
        model2 = indolocate.init("knn")
        model2.fit(X_train2, Y_train2)
        model2.save("models/knn_rssi_env2_model.pkl")

# def train_knn_csi():
#     if csi_data is None:
#         print("Skipping KNN_CSI (no CSI data).")
#         return

#     csi_data_processed = indolocate.preprocess_csi_data(csi_data)
#     X_train, Y_train = indolocate.get_trainset(csi_data_processed, labels)
#     model = indolocate.init("knn")
#     model.fit(X_train, Y_train)
#     model.save("models/knn_csi_model.pkl")

# def train_rf():
#     if rssi_data is None:
#         print("Skipping RF (no RSSI data).")
#         return
#     X_train, Y_train = indolocate.get_trainset(rssi_data, labels)
#     model = indolocate.init("rf")
#     model.fit(X_train, Y_train)
#     model.save("models/rf_model.pkl")

# def train_dnn():
#     if csi_data is None:
#         print("Skipping DNN (no CSI data).")
#         return
#     X_train, Y_train = indolocate.get_trainset(csi_data, labels)
#     model = indolocate.init("dnn")
#     model.fit(X_train, Y_train)
#     model.save("models/dnn_model.pkl")

def main():
    parser = argparse.ArgumentParser(description="Train the configured ML models")
    parser.add_argument("--models", type=str, help="Comma-separated list of models to train (e.g., knn,dnn,rf). Default: all")
    
    args = parser.parse_args()
    
    # Get all functions that start with "train_"
    available_models = [func[6:] for func in globals() if func.startswith("train_") and callable(globals()[func])]

    if args.models:
        model_types = args.models.split(",")
    else:
        model_types = available_models  # Train all if no specific model is passed

    for model_type in model_types:
        model_type = model_type.strip().lower()
        function_name = f"train_{model_type}"  # Dynamically construct function name

        print(f"\n[$] Training {model_type.upper()} model...")
        
        # Check if function exists and call it
        if function_name in globals() and callable(globals()[function_name]):
            globals()[function_name]()  # Call the function dynamically
        else:
            print(f"Unknown model: {model_type}")

if __name__ == "__main__":
    main()
