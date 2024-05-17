# vps-cpu-monitor
This is VPS CPU monitor software.

# Features
On the monitor software, it includes three sections.
### CPU Usage
It shows the CPU usage of your VPS, and it includes information about the name you set for your VPS and the CPU usage of the VPS in real time.

The label will show up in three different colors at three different CPU usage stages.

**Normal (Green) : 0% - 50%**

**Warning (Yellow) : 51% - 89%**

**Danger (Red) : 90% - 100%**

### Logs
If the VPS stays on the Danger stage for more than one minute, it will be recorded in the logs.

**Also, it will send a notification email to your mailbox if you set the notification email in Settings.**

*The email feature uses the API of Guerrilla Mail to create a new temporary email to send an email to your mailbox. I didn't test the feature before, so I didn't know if it worked or not.*

### Settings


# Installation
Before using this software, you need to set up different things on the VPS and local computer.

### VPS
Please install Python on your VPS. If you are using Linux (Ubuntu/Debian) vps, use the following command:
```
apt-get install python3 -y && apt-get install python3-pip -y
```
And please install the following package.
```
pip install psutil
```

After installing the packages in your VPS, you need to download cpu.py on /root/cpu.py and cpu.service on /etc/systemd/system/cpu.service. And run the following command to start the service.

```
systemctl enable cpu && systemctl start cpu
```

One command setup in Linux (ubuntu/debian) VPS:
```
apt-get install python3 -y && apt-get install python3-pip -y && pip install psutil && wget -O /root/cpu.py https://github.com/tsoichinghin/vps-cpu-monitor/raw/main/cpu.py && wget -O /etc/systemd/system/cpu.service https://github.com/tsoichinghin/vps-cpu-monitor/raw/main/cpu.service && systemctl enable cpu && systemctl start cpu
```
**If you open firewall on your VPS, please remember to allow port** ***3001.***

### Local compurter
We also need Python and the following packages.
```
pip install requests
```

After everything is set up, download the monitor script on your local computer.

The download link is:
```
https://github.com/tsoichinghin/vps-cpu-monitor/raw/main/monitor.py
```

# Running
