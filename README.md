# OVPN Watchdog

## Description:
This blob of code is intended to ping a given OVPN server host. 
If failing to respond after a given number x of pings it attempts to reconnect via the OpenVPN-Gui client given a *.ovpn config file.
For more details check the code itself or use the implemted command help via "python main.py -h".
Please keep in mind: This code was chunked together by a noob python dev in an three hour night shift.. You should see it more like a cheat sheet || inspiration.

![console help output screenshot](https://github.com/0x1911/ovpn_watchdog/blob/main/_img/help_output.png)


## Requirements:
* Win OS (only tested on Win OS so far! It'll break when trying to startup the ovpn-gui client on linux/mac <- 27.10.2022)
* OpenVPN-Gui client
* OpenVPN config file in ../config/ with added credentials || keys


## Windows OS How To:
* Create a *.bat file
* pseudo batch code example:
```
python Path\To\File\main.py -c SecureMoonVPN -t 13.37.0.1
```
* add to Win OS autostart through your method of choice
* hopefully never end up with a disconnected client over a longer period of time

## Linux OS How To:
* make sure your user has the rights to execute the openvpn binary file either via sudo or chmod usage
  for reference check: https://serverfault.com/questions/647231/getting-cannot-ioctl-tunsetiff-tun-operation-not-permitted-when-trying-to-con
 --> sudo chmod u+s $(path/to/openvpnBinary)
```
python3 main.py -b /usr/sbin/openvpn -c /home/0x1911/Testerino -t 13.37.0.1
```


### Tested on:
- Windows 10
- Linux Mint


### ToDo:
* more performant check if we (re)connected succesfully without ghetto sleep usage
* check for running OVPN instances and kill "our" old disconnected instances
