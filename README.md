# OVPN Watchdog

## Description:
This blob of code is intended to ping a given OVPN server host. 
If failing to respond after a given number x of pings it attempts to reconnect via the OpenVPN-Gui client given a *.ovpn config file.
For more details check the code itself or use the implemted command help via "python main.py -h".
Please keep in mind: This code was chunked together by a noob python dev in an three hour night shift.. You should see it more like a cheat sheet || inspiration.


## Requirements:
* Win OS (only tested on Win OS so far! It'll break when trying to startup the ovpn-gui client on linux/mac <- 27.10.2022)
* OpenVPN-Gui client
* OpenVPN config file in ../config/ with added credentials || keys


## How To:
* Create a *.bat file
* pseudo example:
```
python Path\To\File\main.py -t 13.37.0.1 -c SecureMoonVPN
```
* add to Win OS autostart through your method of choice
* hopefully never end up with a disconnected client over a longer period of time
* ???
* Profit!


## ToDo (maybe):
* debug argument implementation for more intel chatter output in terminal/console
* support for linux and/or mac OS
* more performant check if we (re)connected succesfully without ghetto sleep usage
* check for running OVPN instances and kill "our" old disconnected instances
* code cleanup