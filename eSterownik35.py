"""
 author: Gabriel Zima
 e-mail: gabriel.zima@wp.pl

"""
import sys
import subprocess
import datetime

class eSterownik35:
    def __init__(self, IP, port=80, user="root", password="root", interval=30):
        self.Data = {}
        self.LastUpdate = 0
        self.IP = IP
        self.port = port
        self.user = user
        self.password = password
        self.interval = interval

    def sParse(self, s):
        if len(s) > 10:
            return s
        try:
            return int(s)
        except:
            try:
                 return float(s)
            except:
                 return s

    def SyncValues(self):
        bash_command = 'curl -s -H "Host: ' + self.IP + ':' + str(self.port) + \
                       '" -H "User-Agent: Domoticz/1.0" -H "Accept: */*" -H "Authorization: Basic `echo -n ' + \
                       self.user + ':' + self.password + ' | base64`" http://' + \
                       self.IP + ':' + str(self.port) + '/syncvalues.cgi'
        rawdata = subprocess.check_output(['bash','-c', bash_command]).decode("utf-8")
        if rawdata.find("device_name") > 0:
            for line in rawdata.split('\r'):
                if line != "":
                    regs = {}
                    arLine = line.split(";")
                    for arElem in arLine:
                        if arElem.find(":") > 0:
                            key, value = arElem.split(":")
                            regs[key] = self.sParse(value)
                    regs['TimeStamp'] = int(arLine[1])
                    self.Data[int(arLine[0])] = regs
            self.Data['LastUpdate'] = int(datetime.datetime.now().timestamp())
            self.LastUpdate = self.Data['LastUpdate']

    def GetData(self):
        if  self.LastUpdate + self.interval < int(datetime.datetime.now().timestamp()):
            self.SyncValues()
        return self.Data

    def Refresh():
        self.GetData();

    def GetValue(self, device=0, value="device_name"):
        self.GetData()
        result = "--err--"
        if device in self.Data:
            if value in self.Data[device]:
                result = self.Data[device][value]
        return result

    def SetValue(self, key, value, device=0):
        bash_command = 'curl -s -H "Host: ' + self.IP + ':' + str(self.port) + \
                       '" -H "User-Agent: Domoticz/1.0" -H "Accept: */*" -H "Authorization: Basic `echo -n ' + \
                       self.user + ':' + self.password + ' | base64`" http://' + \
                       self.IP + ':' + str(self.port) + '/setregister.cgi?device=' + str(device) + "&" + key + "=" & value
        rawdata = subprocess.check_output(['bash','-c', bash_command]).decode("utf-8")
