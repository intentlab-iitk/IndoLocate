# AX-CSI: Enabling CSI Extraction on Commercial 802.11ax Wi-Fi Platforms - **V0.0.4**

---

## What is AX-CSI?

AX-CSI is a tool developed to transform Asus RT-AX86U Access Points into devices that can collect Channel State Information (CSI) from OFDM frames transmitted in the 5GHz band and compliant with 802.11a/n/ac/ax encodings.

## Notes

- **Note 0:** This tool is released for research purposes. By using this tool, you agree to:

  - Use it only for research. Any other type of use is not recommended.
  - Not distribute the tool to others.
  - Delete the tool if it is no longer in use.

  The tool is provided for free to researchers or practitioners who request it. We do not sell the tool or guarantee support.

- **Note 1:** While the tool is stable, it is still under development, and new features may be added. Traces captured with a given version must be processed using the software released with that version, as new versions may not preserve backward compatibility.

- **Note 2:** AX-CSI requires saving a modified version of the drivers on the Access Point (AP). If used improperly, it may damage your hardware and void its warranty. **Use the tool at your own risk and responsibility!** If you disagree with these terms, stop immediately and do not use this tool.

- **Note 3:** For compatibility, ensure your AP is running firmware version 3.0.0.4.384_9262. If your AP is running a different version, upgrade or downgrade to this exact version. If you cannot find the suggested version on the Asus website, try fetching it with utilities like `wget` or `curl` by manually composing the URL with the version string.

## Installation and Usage

In the following steps, it is assumed you have a device used to collect CSI from frames transmitted by other devices. You need to know the channel configuration and MAC addresses of these other devices. When "eth7" appears, it refers to the 5GHz interface.

1. **Check AP Firmware:**
   - Ensure your AP is running firmware version **3.0.0.4.384_9262**. If not, download and flash this version.

2. **AP Configuration:**
   - "Parent AP status" must read "**AP Mode**".
   - 2.4GHz and 5GHz **interfaces MUST be separate**.
   - In "Advanced Settings" > "Wireless" > 5GHz band:
     - "802.11ax/ Wi-Fi 6 mode" should be "**Enabled**".
     - In Channel bandwidth "Enable 160 MHz" should be ticked.

3. **Copy Files to AP:**
   - Copy all files in the "CSI5G" folder from the axcsi tool to `/jffs/CSI5G` on the AP using `scp`.  
      ```bash
      scp -r ./CSI5G asus@192.168.50.1:/jffs/
      ```

4. **Setup the ENV:**
   - On the AP, SSH into /jffs/CSI5G make all scripts and binaries excuatable. [ONLY For the First time]
     ```bash
     cd /jffs/CSI5G
     chmod +x *
     ```
5. **Load the Modified Driver:** 
   - Load it from /jffs/CSI5G. [SHOULD BE DONE AFTER EVERY REBOOT/SHUTDOWN OF DEVICE]  
     ```bash
     /jffs/CSI5G/reload.sh
     ```
   - Note: Reload the driver only once after a reboot, as reloading twice can crash the AP.

6. **Configure AP Channel and Bandwidth:**
   - Configure the AP on the same channel/bandwidth as the devices from which you want to capture CSI:
     ```bash
     /jffs/CSI5G/config5GHZ.sh 157 80 8 1 8
     ```
   - Parameters for `config5GHz.sh`:
     - `CHANNEL`: Primary Wi-Fi channel to use (e.g., 36, 140, 157).
     - `BW`: Maximum bandwidth for capturing frames and their CSI (20/40/80/160 MHz).
     - `RXANT`: Bitmask for receiving antennas.
       - `1`: Antenna in the middle.
       - `2`: Internal antenna (between mid and rightmost).
       - `4`: Antenna to the left (looking at the AP from the front).
       - `8`: Antenna to the right.
     - `NSS`: Bitmask for spatial streams to capture.
       - `1`: First spatial stream.
       - `2`: Second spatial stream.
       - `4`: Third spatial stream.
       - `8`: Fourth spatial stream.
     - `TXANT`: Bitmask for transmitting antennas (applies only to one spatial stream transmissions).

7. **Configure the MAC Filter:**
   - Indicate the frames for which CSI should be extracted:
     ```bash
     /jffs/CSI5G/setmacfilter.sh eth7 88:00 00:11:22:33:44:55
     ```
   - Note: Run `setmacfilter.sh` again after reconfiguring as in step 6.
   - Note: You can specify up to three MAC addresses. 
   - To reset filters:
     ```bash
     /jffs/CSI5G/resetfilters.sh eth7
     ```

8. **Start Capturing CSI:**
   - On the AP:
     ```bash
     /jffs/CSI5G/capture.sh trace.pcap eth7
     ```
   - Warning: Use this script instead of calling `tcpdump` directly to avoid filling up the jffs, which could "brick" the AP.

9.  **Transmit Frames from Other Devices:**
    - Use your own tools to start transmitting frames from other devices.

10. **Convert Binary CSI Trace to TXT:**  
    *Method 1*:  
      - On the device that collected CSI:
          ```bash
          /jffs/CSI5G/convertpcap.sh trace.pcap data.mat
          ```
      - Copy `/tmp/data.mat` to your computer's scripts/matlabData folder.

    *Method 2*:  
      - Alternatively, on an Ubuntu PC place that trace.pcap file in scripts/captureData and use preprocess.sh:
          ```bash
          ./preprocess.sh
          ```
          NOTE: You can provide Args for the names of input and output files - {OPTIONAL: trace.pcap} {OPTIONAL: data.mat}
      - "data.mat" will be generated inside scripts/matlabData folder.
  - The executable has been tested on Ubuntu 18 and later, only for x86_64.

11. **Analyze Data:**
    - The data may be challenging to analyze, especially for 160MHz ac frames and all ax encodings except 20MHz.
    - A Matlab script is included to parse the data:
      ```matlab
      >> extract.m
      ```
    - This will create a Matlab struct array `alldata` containing all CSIs.

    - Example to plot the CSI:
      ```matlab
      >> plot(abs(alldata(1).core{4}.nss{1}.data))
      ```

### Important Fields in `alldata` Struct Array

- **core:** Cell array containing separate data per receiving antenna.
  - `core{1}`: Corresponds to antenna Middile.
  - `core{2}`: Corresponds to antenna Internal.
  - `core{3}`: Corresponds to antenna Left.
  - `core{4}`: Corresponds to antenna Right.
  
- **core{x}.nss:** Cell array with the captured spatial streams.
  - `core{x}.nss{1}`: First spatial stream.
  - `core{x}.nss{2}`: Second spatial stream.
  - `core{x}.nss{3}`: Third spatial stream.
  - `core{x}.nss{4}`: Fourth spatial stream.
  
- **phytype:** Indicates the type of captured frame:
  - `0`: 802.11a.
  - `1`: 802.11n.
  - `2`: 802.11ac.
  - `3`: 802.11ax.
  
- **rxtsslow:** Timestamp of the radio in microseconds.
- **rxseqno:** Frame sequence number for which CSI was captured.
- **sn:** Internal sequence number of the receiver when CSI was captured.
- **ts:** System timestamp when CSI was collected.
- **srcmac:** Source MAC address of the frame for which CSI was captured.
- **powers:** Array with power levels of the four antennas (work-in-progress, measured in dB).

---
[Back to Main](README.md)
