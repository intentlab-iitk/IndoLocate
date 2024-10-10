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

Here is the code section from your document converted to Markdown:

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
   - On the AP, SSH into /jffs/CSI5G make all scripts and binaries executable. [ONLY For the First time]
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
   - Parameters for "config5GHz.sh":
     ```bash
     ./config5GHz.sh CHANNEL BW RXANT NSS TXANT
      ```
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
   - Configure the filter to indicate for which frames CSI should be extracted.

     ```bash
     ./setsourceinfo.sh eth7
     ```
   - Command `setsourceinfo.sh` configures the filter so that CSI is collected only for frames whose transmitter MAC address is `00:12:34:56:78:9b` and whose frame control starts with byte `0x88`. We will transmit frames like these below at point 10.

   - NOTE: `setsourceinfo.sh` must be run again every time the system is reconfigured as in point 6.

8. **Configure the Power:**  
   - The power is by default automatically chosen by the AP. To override this setting, run:

      ```bash
      cd /jffs/CSI5G
      ./settxpower.sh eth7 xy
      ```
   - where `xy` is a two-digit hexadecimal value ranging from `00` (max) to `7f` (min).

9. **Start Capturing at the Receiving AP:**  

      ```bash
      cd /jffs/CSI5G
      ./capture.sh trace.pcap eth7
      ```
   - Command `capture.sh` will save a trace with all collected CSI located in `/tmp/trace.pcap`

   - WARNING: Use this script instead of calling `tcpdump` yourself to avoid forgetting to save the trace under `/tmp`. Remember that if you leave the `jffs` with no space available, the AP enters a sort of "bricked" state and you have to re-flash the AP.

10. **Transmit Some Frames from the Transmitting AP:**  

    ```bash
    cd /jffs/CSI5G
    ./sendsta.sh eth7 100 250 80ac 1
    ```
   - Command `sendsta.sh` transmits 100 frames each long 250B encoded as 802.11ac frames at 80MHz, using a single spatial stream.
   - Frames are generated with transmitter address `00:12:34:56:78:9b` and their frame control field starts with `0x8802`. They will be matched by the receiver that will collect CSI for these frames.

   - The meaning of parameters is:

        ```bash
        ./sendsta.sh eth7 NUMFRAMES LENGTH ENCODING NSS
        ```

      - `NUMFRAMES`: Number of frames to transmit
      - `LENGTH`: Length of frames to transmit in bytes
      - `ENCODING`: Encoding as `BWPHY`, i.e., `BW` is the bandwidth (20/40/80/160) and `PHY` can be `a|n|ac|ax`
      - `NSS`: Number of spatial streams to transmit

   - NOTE: 250B is a long frame; you can reduce it, but if frames are too short, CSI cannot be captured.

11. **Convert Binary CSI Trace into a TXT File.**  
    - On the device that collected CSI, run:

      ```bash
      cd /jffs/CSI5G
      ./convertpcap.sh trace.pcap data.mat
      ```

    - NOTE: You can convert the file `trace.pcap` on an Ubuntu PC instead of the device by using the executable `csireader` included in the `matlab_scripts` folder, e.g., on the Ubuntu PC (not on the device):

      ```bash
      cd /path/to/matlab_scripts
      ./csireader -f trace.pcap -o data.mat -a
      ```

    - The executable has been tested on Ubuntu 18 and following, only for x86_64.

12. **Copy /tmp/data.mat to Your Computer and Start Analyzing It.**  
    - The data may not be very easy to analyze, as starting with 160MHz ac frames and for all ax encodings except for 20MHz, CSI may split over multiple lines.

    - For this reason, we include a Matlab script that parses the data and produces an easy-to-use Matlab struct array.

    - Copy the file `data.mat` to the same folder that contains the Matlab script called `extract.m`, then execute it:

      ```matlab
      >> extract
      ```

    - You will end up with a Matlab struct array `alldata` that contains all CSIs.

      `alldata` is a 1x100 struct array with fields:

      - `core`
      - `tones`
      - `phytype`
      - `rxts`
      - `rxtsslow`
      - `rxseqno`
      - `txts`
      - `sn`
      - `ts`
      - `srcmac`
      - `powers`
      - `phy0`

    - Try plotting the CSI with:

        ```matlab
        >> plot(abs(alldata(1).core{4}.nss{1}.data))
        ```

    - Remember in the example above, we configured the system to collect from antenna `8`, but this must be considered as a bitmask indicating core number `4` (starting from `1`), see A1) below for understanding.

### Important Fields in `alldata` Struct Array

  - `core`: Cell array containing separate data per receiving antenna. Check the meaning as in point 6) above:
    - `core{1}` corresponds to antenna bitmask `1`
    - `core{2}` corresponds to antenna bitmask `2`
    - `core{3}` corresponds to antenna bitmask `4`
    - `core{4}` corresponds to antenna bitmask `8`
  - `core{x}.nss`: Cell array with the captured spatial streams. Each `nss` in turn contains a data array with the real CSI data.
    - `core{x}.nss{1}` corresponds to first spatial stream
    - `core{x}.nss{2}` corresponds to second spatial stream
    - `core{x}.nss{3}` corresponds to third spatial stream
    - `core{x}.nss{4}` corresponds to fourth spatial stream

- Note that some of these fields might not exist because they were excluded from capture.

  - `phytype`: Indicates the type of captured frame, i.e.,
    - `0`: 802.11a
    - `1`: 802.11n
    - `2`: 802.11ac
    - `3`: 802.11ax

  - `rxtsslow`: Carries the timestamp of the radio

---
[Back to Main](README.md)
