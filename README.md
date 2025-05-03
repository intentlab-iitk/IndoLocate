# Indolocate (Work in progress)

Indolocate is a Python package designed for **indoor localization**, leveraging **Wi-Fi Channel State Information (CSI) and Received Signal Strength Indicator (RSSI)** to estimate precise indoor positions. Traditional GPS fails in indoor environments due to signal obstructions, making Wi-Fi-based localization a reliable alternative.  

### **🔹 Features**  
- **Wi-Fi CSI-based Localization**: Utilizes fine-grained CSI measurements for more accurate positioning compared to RSSI-based methods.  
- **RSSI-based Positioning**: Implements fingerprinting and trilateration techniques using Wi-Fi signal strength.  
- **Multi-AP Fusion**: Combines signals from multiple access points (APs) for improved localization accuracy.  
- **Signal Processing & Filtering**: Supports smoothing techniques such as Kalman Filter and Particle Filter to reduce noise in CSI and RSSI data.  
- **Customizable API**: Easy-to-use functions for training models and predicting indoor positions.  

### **🔹 Applications**  
- **Smart Buildings & Indoor Navigation**: Assists in real-time navigation inside malls, airports, and offices.  
- **Asset Tracking**: Helps locate objects, robots, and personnel in warehouses and factories.  
- **Activity Recognition & Sensing**: Enhances human activity detection and environmental monitoring using Wi-Fi signals.  

By integrating **CSI and RSSI**, `indolocate` provides a robust and scalable solution for **Wi-Fi-based indoor localization**, enabling researchers and developers to build efficient real-world positioning systems. 🚀
