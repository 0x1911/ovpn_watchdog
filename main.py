import configparser
import platform 
import subprocess 
import sys
import pathlib
import time
from optparse import OptionParser

shouldRun = True
maxPingAttempts = 3
failedPingCount = 0
targetHost = ""
ovpnBinaryPath = ""
ovpnConfigFile = ""

#region helper methods
def isWindowsOS():
    return platform.system().lower() == 'windows'

def doesFileExist(filePath):
    return platform.os.path.exists(filePath)

def doesPathExist(absolutePath):
    return pathlib.path.exists(absolutePath)

def doSmartPing(host):
    #build the ping param string depending on operating system
    # -n for windows || nt os, -c on mac and unix
    param = '-n' if isWindowsOS() else '-c'
    command = ['ping', param, '1', host]

    # TODO: stdout and stderr are routed to devnull to shup up the console chatter.. maybe re-setup chatter as debug option?
    return subprocess.call(command, stdout=open(platform.os.devnull, 'wb')) == 0

def pingHasFailed(isFail = False):
    global failedPingCount

    if (isFail):
        failedPingCount += 1
    else:
        failedPingCount = 0
#endregion


#region main code entry
parser = OptionParser()
parser.add_option("-t", "--target", dest="targetHost",
                  help="host adress to ping", metavar="10.0.0.1", default="10.0.0.1")
parser.add_option("-b", "--binary", dest="binaryLocation",
                  help="absolute binary file path", metavar="C:\\Program Files\\OpenVPN\\bin\\openvpn-gui.exe", default="C:\\Program Files\\OpenVPN\\bin\\openvpn-gui.exe")
parser.add_option("-c", "--config", dest="configFile",
                  help="config file name without file extension", metavar="moon", default="Hollaender_real")
#parser.add_option("-d", "--debug",
#                  action="store_false", dest="verbose", default=False,
#                  help="don't print status messages to stdout")


#region set variables according to given params
(options, args) = parser.parse_args()

targetHost = options.targetHost
ovpnBinaryPath = options.binaryLocation
ovpnConfigFile = options.configFile + ".ovpn"
#endregion


#region lets do some basic checks before doing anything fancy..
print("+---- startup check -------+")
print("|".ljust(27) + "|")
if(isWindowsOS()):
    print("| Win OS detected".ljust(27) + "|")
if(doesFileExist(ovpnBinaryPath)):
    print("| Binary found - good".ljust(27) + "|")
print("|".ljust(27) + "|")
print("+---- startup check -------+")
#endregion


while(shouldRun): # <- bad practice
    pingResponse = doSmartPing(targetHost)

    if (pingResponse != True):
        pingHasFailed(True)
    else: # reset counter on success        
        pingHasFailed()
    
    # reset on x amount of failed attempts
    if (failedPingCount >= maxPingAttempts):
        pingHasFailed()
        print("| failed "+ str(maxPingAttempts) + " pings in a row")
        #region attempt to reconnect
        # on a windows OS?
        if(isWindowsOS()):            
            cmd = 'start /b cmd /c \"' + ovpnBinaryPath + '\" --connect ' + ovpnConfigFile
            # run and remember the process as 'x'
            x = subprocess.Popen(cmd, shell=True)
            #subprocess.call(["C:\\Program Files\\OpenVPN\\bin\\openvpn-gui.exe", "--connect testerino"])
            #callReturnValue = subprocess.call(ovpnBinaryPath + " --command connect " + ovpnConfigPath)
        else:
            #TODO: linux && mac process startup
            print("not implemented yet, boi. :(")            
        #endregion


        # ghetto sleep - waiting for connection to be established
        time.sleep(15) 
        print("| connected successfully?")        
        # TODO: check for running process?
        # TODO: maybe kill all running ovpn processes?


    # lets sleep for 5 seconds to avoid server spam and potencially getting blacklisted
    time.sleep(5) 
#endregion