import platform 
import subprocess 
import pathlib
import time
from optparse import OptionParser

shouldRun = True
maxPingAttempts = 3
failedPingCount = 0
showDebugOutput = False
pingTargetHost = ""
ovpnBinaryPath = ""
ovpnConfigFile = ""

ovpnPID = 0

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

    if(showDebugOutput):
        return subprocess.call(command) == 0

    return subprocess.call(command, stdout=open(platform.os.devnull, 'wb')) == 0

def doSubProcessStartup(parameterString):
    cmd = parameterString
    x = subprocess.Popen(cmd, shell=True)

    return x.pid

def pingHasFailed(isFail = False):
    global failedPingCount

    if (isFail):
        failedPingCount += 1
    else:
        failedPingCount = 0
#endregion


#region main code entry
parser = OptionParser()
parser.add_option("-t", "--target", dest="targetHost", metavar="13.37.0.1", default="10.0.0.1",
                  help="host adress to ping")
parser.add_option("-b", "--binary", dest="binaryLocation", metavar="C:\\Program Files\\OpenVPN\\bin\\openvpn-gui.exe", default="C:\\Program Files\\OpenVPN\\bin\\openvpn-gui.exe",
                  help="absolute binary file path")
parser.add_option("-c", "--config", dest="configFile", metavar="moon", default="Hollaender_real",
                  help="config file name without file extension")
parser.add_option("-d", "--debug", dest="debugOutput", metavar=True, default=False,
                  help="print status messages to console")


#region set variables according to given params
(options, args) = parser.parse_args()

pingTargetHost = options.targetHost
ovpnBinaryPath = options.binaryLocation
ovpnConfigFile = options.configFile + ".ovpn"
showDebugOutput = options.debugOutput
#endregion


#region lets do some basic checks before doing anything fancy..
print("+----- startup check -----+")
print("|")
if(isWindowsOS()):
    print("| win OS detected")
else:
    print("| unix OS detected")
if(doesFileExist(ovpnBinaryPath)):
    print("| binary found - good")
else:
    print("| binary not found")
if(doesFileExist(ovpnConfigFile) and not isWindowsOS()):
    print("| config found - good")
elif not isWindowsOS():
    print("| config not found")
print("|")
print("+----- startup check -----+")
#endregion


while(shouldRun): # <- bad practice
    pingResponse = doSmartPing(pingTargetHost)

    if (pingResponse != True):
        pingHasFailed(True)
    else: # reset counter on success        
        pingHasFailed()
    
    # reset on x amount of failed attempts
    if (failedPingCount >= maxPingAttempts):
        pingHasFailed()
        print("| failed "+ str(maxPingAttempts) + " pings in a row")
        #region attempt to reconnect
        # windows OS process startup
        if(isWindowsOS()):            
            cmd = 'start /b cmd /c \"' + ovpnBinaryPath + '\" --connect ' + ovpnConfigFile

        # linux && mac process startup
        else:            
            #TODO: include into readme -> https://serverfault.com/questions/647231/getting-cannot-ioctl-tunsetiff-tun-operation-not-permitted-when-trying-to-con
            #                        |--> sudo chmod u+s $(which openvpn)
            # Linux mint: python3 main.py -b /usr/sbin/openvpn -c /home/drb/Testerino
            cmd = ovpnBinaryPath + " " + ovpnConfigFile
        
        ovpnPID = doSubProcessStartup(cmd)
        print("| new ovpn process id: " + str(ovpnPID))
        #endregion


        # ghetto sleep - waiting for connection to be established
        time.sleep(15) 
        print("| connected successfully?")        
        # TODO: check for running process?
        # TODO: maybe kill all running ovpn processes?


    # lets sleep for 5 seconds to avoid server spam and potencially getting blacklisted
    time.sleep(5) 
#endregion