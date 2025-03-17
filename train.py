import indolocate
import pandas as pd
from indolocate.utils import preprocess_rssi

# Tampere RSSI dataset
tampere_dataset = pd.read_csv("/mnt/LabData/datasets/indoor_localization/Tampere/FINGERPRINTING_DB/tampere_main.csv")
X_train = tampere_dataset.iloc[:,:992].values
Y_train = tampere_dataset.iloc[:, 992:995].values
X_train, Y_train = preprocess_rssi(X_train, Y_train)

# # KNN Model
# KNNregressionModel = indolocate.create_model(algorithm="knn")
# KNNregressionModel.fit(X_train, Y_train)
# KNNregressionModel.save("models/knn_model.pkl")

# # RF Model
# RFRegressionModel = indolocate.create_model(algorithm="rf")
# RFRegressionModel.fit(X_train, Y_train)
# RFRegressionModel.save("models/rf_model.pkl")

# # DNN Model
# DeepNeuralNetModel = indolocate.create_model(algorithm="dnn")
# DeepNeuralNetModel.fit(X_train, Y_train)
# DeepNeuralNetModel.save("models/dnn_model.pkl")

# # GBDT Model
# GBDTModel = indolocate.create_model(algorithm="gbdt")
# GBDTModel.fit(X_train, Y_train)
# GBDTModel.save("models/gbdt_model.pkl")

# # LSTM Model
# LSTMModel = indolocate.create_model(algorithm="lstm")
# LSTMModel.fit(X_train, Y_train)
# LSTMModel.save("models/lstm_model.pkl")