# vps-cpu-monitor
This is a VPS CPU monitor application.

# Features
On the monitor application, it includes three sections.
### CPU Usage
It shows the CPU usage of your VPS, and it includes information about the name you set for your VPS and the CPU usage of the VPS in real time.

The label will show up in three different colors at three different CPU usage stages.

**Normal (Green) : 0% - 50%**

**Warning (Yellow) : 51% - 89%**

**Danger (Red) : 90% - 100%**

### Logs
If the VPS stays on the Danger stage for more than one minute, it will be recorded in the logs.

**Also, it will send a notification email to your mailbox if you set the Notification Email Setting in Settings.**

### Settings
All application settings are behind this section.

***Linking Devices Setting*** **-** Before you use the application, you need to upload your CSV file to link your VPS devices.

***Notification Email Setting*** **-** If you want to use the notification feature, you need to fill in your sender email address and recipient email address to set the notification email setting. **But the sender email is only supported in Outlook emails.**

# Installation
Before using this application, you need to set up different things on the VPS and local computer.

### VPS
Please install Python on your VPS. If you are using Linux (Ubuntu/Debian) vps, use the following command :
```
apt-get install python3 -y && apt-get install python3-pip -y
```

And please install the following package.
```
pip install psutil
```

If you got some error in installation in Python, the factor of error may be that you didn't update and upgrade the apt.
```
apt-get update && apt-get upgrade -y
```

After installing the packages in your VPS, you need to download 

**cpu.py** on */root/cpu.py* 

and 

**cpu.service** on */etc/systemd/system/cpu.service*

and finally run the following command to start the service.

```
systemctl enable cpu && systemctl start cpu
```

One command setup in Linux (ubuntu/debian) VPS :
```
apt-get install python3 -y && apt-get install python3-pip -y && pip install psutil && wget -O /root/cpu.py https://github.com/tsoichinghin/vps-cpu-monitor/raw/main/cpu.py && wget -O /etc/systemd/system/cpu.service https://github.com/tsoichinghin/vps-cpu-monitor/raw/main/cpu.service && systemctl enable cpu && systemctl start cpu
```
**If you open firewall on your VPS, please remember to allow port** ***3001.***

### Local computer
We also need Python and the following packages.
```
pip install requests
```

After everything is set up, download the monitor script on your local computer.
```
wget https://github.com/tsoichinghin/vps-cpu-monitor/raw/main/monitor.py
```

# Running
Before running the application, please download vps_list.csv to save your VPS IPs and names that you want to set in the application.
```
wget https://github.com/tsoichinghin/vps-cpu-monitor/raw/main/vps_list.csv
```

### ***After all the setup is finished, you can open your terminal and run Monitor script on your local computer.***
```
python monitor.py
```
```
python3 monitor.py
```


### ***If you don't want to manually type the command every time, you may make a Unix executable file or exe file with pyinstaller.***

The command for installing pyinstaller :
```
pip install pyinstaller
```

Make a Unix executable file on Mac and Linux, or make an exe file on Windows :
```
pyinstaller --onefile monitor.py
```

You will find a unix executable file or exe file name monitor in dist folder.

# Happy monitoring
When the GUI is loaded, open Settings to upload your CSV file and start using this application.

Also, fill in your sender email address and recipient email address if you want to use the notification email feature.

