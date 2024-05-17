# vps-cpu-monitor
This is a VPS cpu monitor software.

# Installation
Before using this software, you need to setup different things in VPS and local computer.

### VPS
Please install python in your VPS. If you using Linux（ubuntu/debian) vps, using the following command:
```
apt-get install python3 -y && apt-get install python3-pip -y
```
And please install the following package.
```
pip install psutil
```

After installed the packages in your VPS, you need to download cpu.py on /root/cpu.py and cpu.service on /etc/systemd/system/cpu.service. And run the following command to start the service.

```
systemctl enable cpu && systemctl start cpu
```

One command setup in Linux (ubuntu/debian) VPS:
```
apt-get install python3 -y && apt-get install python3-pip -y && pip install psutil && wget -O /root/cpu.py https://github.com/tsoichinghin/vps-cpu-monitor/raw/main/cpu.py && wget -O /etc/systemd/system/cpu.service https://github.com/tsoichinghin/vps-cpu-monitor/raw/main/cpu.service && systemctl enable cpu && systemctl start cpu
```
**If you open firewall in your VPS, please remember to allow the port** ***3001***

### Local compurter
Also need Python and the following packages.
```
pip install requests
```

After set all up, download the monitor sciprt in your local computer.

The download link:
```
https://github.com/tsoichinghin/vps-cpu-monitor/raw/main/monitor.py
```

# Running
