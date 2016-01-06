#!/usr/bin/env python

import sys
import os
import tweepy
import ConfigParser

os.environ['TERM'] = "xterm"

# Return CPU temperature as a float
def getCPUtemperature():
#    try:
#        s = subprocess.check_output(["/opt/vc/bin/vcgencmd","measure_temp"], shell=False)
#        return float(s.split('=')[1][:-3])
#    except:
#        return 0
    res = os.popen('/opt/vc/bin/vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==3:
		return(line.split()[1:4])

# Return % of CPU used by user as a character string
def getCPUuse():
    # Return the inverse of CPU idle, instead of part of usage
	cpuUsePrc=str(100-float(os.popen("top -n1 -b | awk '/Cpu\(s\):/ {print $8}'").readline().strip()))
	return(cpuUsePrc)

# Return information about disk space as a list (unit included)
# Index 0: total disk space
# Index 1: used disk space
# Index 2: remaining disk space
# Index 3: percentage of disk used
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])


#Main program
if __name__ == "__main__":
    ramInfo=getRAMinfo()
    usedMem=int(ramInfo[1])
    freeMem=int(ramInfo[2])
    #calculate the free memory percentage
    freeMemPerc=int((float(freeMem)/(usedMem+freeMem))*100)
    #get hostname
    hostname = os.popen('hostname').readline().rstrip()
    #build the info string
    sysInfoString= hostname + ": CPUTemp " + getCPUtemperature() + ", CPU U " + getCPUuse()+ "%, FreeDisk " + getDiskSpace()[2] + ", FreeMemPrc " + str(freeMemPerc) + "%"
    #print(sysInfoString)

    #read config file for twitter keys (so not to include them on github)
    try:
        config = ConfigParser.ConfigParser()
        config.read("~/.twitter.conf")
        #get options from section
        options = config.options('TwitterAccount')

        #Initialise Twitter API
        auth = tweepy.OAuthHandler(options[1], options[2])
        auth.set_access_token(options[3], options[4])
        api = tweepy.API(auth)

        # tweet the sys info
        api.update_status(sysInfoString) #Tweet status
    except:
        exit()
