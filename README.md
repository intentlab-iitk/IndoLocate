# Robust Indoor Localization :: INTENT Labs

### **Ongoing Project**

This project focuses on designing a robust indoor localization system leveraging the advanced capabilities of **Wi-Fi 6 (802.11ax)** devices. By harnessing **Channel State Information (CSI)** and **Angle of Arrival (AoA) estimation**, we aim to achieve precise and reliable localization in challenging indoor environments.


## **Project Overview**

Indoor localization has become essential for various applications, such as navigation, asset tracking, and location-based services. This project explores how **CSI data** from Wi-Fi 6 devices can be processed to compute **AoA**, enabling accurate device positioning through **triangulation techniques**.

### **Workflow Phases**
1. **CSI Data Collection**  
   Leveraging the **axcsi tool**, developed by **Imdea Networks**, to extract CSI data from Wi-Fi 6 devices.  
   
2. **AoA Estimation**  
   Using the collected CSI data to calculate AoA and implementing **triangulation algorithms** for precise location determination.


## **Setup Instructions**

### **Requirements**
- **Wi-Fi 6 Router**  
  Compatible models include ASUS RTX86U or any router equipped with the **Broadcom 43684 Wi-Fi chipset**.  
- **Transmitter Device**  
  A Wi-Fi 6-enabled device capable of sending Wi-Fi frames (serves as the target for localization).  


### **Installation & Usage**

1. Clone the repository:
   ```bash
   git clone https://github.com/intentlab-iitk/IndoLocate.git
   cd IndoLocate
   ```
2. Follow the detailed setup guide for the axcsi tool in the [**axcsi-tool.md**](./axcsi-tool.md) file.
3. For processing the CSI data into AoA, instrcutions will be added here.


## **Key Features**

- **High Precision**: Combines CSI and AoA techniques to minimize errors in location estimation.  
- **Real-Time Processing**: Designed to handle dynamic indoor environments.  


## **License**

This project is open-sourced under the [**MIT License**](./LICENSE).  


## **References**

- [AX-CSI: Enabling CSI Extraction on Commercial 802.11ax Wi-Fi Platforms](https://dl.acm.org/doi/10.1145/3477086.3480833)  
