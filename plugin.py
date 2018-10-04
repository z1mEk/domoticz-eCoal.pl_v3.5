"""
<plugin key="eCoal35" name="eCoal.pl v3.5 - Sterownik kotła" author="z1mEk" version="0.1.0" wikilink="" externallink="https://github.com/z1mEk/domoticz-eCoal.pl_v3.5">
    <description>
        <p>Dodatek zapewnia integrację z eCoal.pl, sterownikiem przeznaczonym do sterowania kotłów wodnych na paliwo stałe.</p>
        <p>Informacje o sterowniku: <a href="https://esterownik.pl/nasze-produkty/ecoal-v35">https://esterownik.pl/nasze-produkty/ecoal-v35</a></p>
    </description>
    <params>
        <param field="Address" label="Adres IP" width="200px" required="true" default="192.168.1.1"/>
        <param field="Port" label="Port" width="50px" required="true" default="80"/>
        <param field="Username" label="Użytkownik" width="50px" required="true" default="root"/>
        <param field="Password" label="Hasło" width="50px" required="true" default="root"/>
        <param field="Mode1" label="ID urządzenia" width="50px" required="true" default="0"/>
        <param field="Mode2" label="Rejestry danych" width="400px" required="true" default="tkot_value,t,Temp. kocioł;tpow_value,t,Temp. powrotu;tpod_value,t,Temp. podajnika;tcwu_value,t,Temp. CWU;twew_value,t,Temp. wewnętrzna;tzew_value,t,Temp. zewnętrzna;tsp_value,t,Temp. spalin;fuel_level,p,Poziom paliwa"/>
        <param field="Mode3" label="Częstotliwość odczytu" width="50px" required="true" default="300"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import base64
import xml.etree.ElementTree as et

class BasePlugin:
    eCoalConn = None
    #isConnect = false
    units = {"t":"Temperature", "p":"Percentage", "b":"Barometer", "c":"Custom"}

    def onStart(self):
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
        Domoticz.Debug("onStart called")

        if (len(Devices) == 0):
            for i, x in enumerate(Parameters["Mode2"].split(";")):
                Domoticz.Debug(x)
                device_id, device_type, device_name = x.split(",")
                Domoticz.Device(Name=device_name, Unit=i+1, DeviceID=device_id, TypeName=self.units[device_type], Used=1).Create()

        self.eCoalConn = Domoticz.Connection(Name="eCoal Connection", Transport="TCP/IP", Protocol="HTTP", Address=Parameters["Address"], Port=Parameters["Port"])
        self.eCoalConn.Connect()
        Domoticz.Heartbeat(int(Parameters["Mode3"]))

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called. Status: " + str(Status))

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called, Data: " + str(Data))
        if Data['Status'] == '200':
            httpBody = str(Data['Data'])
            #httpBody = """<?xml version="1.0" encoding="UTF-8"?><cmd status="ok"><device id="0"><reg vid="0" tid="tkot_value" v="64.20" min="-50.00" max="120.00" /><reg vid="0" tid="tpow_value" v="57.06" min="-50.00" max="120.00" /><reg vid="0" tid="tpod_value" v="47.12" min="-50.00" max="120.00" /><reg vid="0" tid="tcwu_value" v="60.33" min="-50.00" max="120.00" /><reg vid="0" tid="twew_value" v="23.95" min="-50.00" max="120.00" /><reg vid="0" tid="tzew_value" v="6.48" min="-50.00" max="120.00" /><reg vid="0" tid="tsp_value" v="109.38" min="-50.00" max="600.00" /></device></cmd>"""
            xmlBody = et.fromstring(httpBody)
            if 'status' in xmlBody.attrib:
                if xmlBody.attrib['status'] == "ok":
                    for child in xmlBody.iter('reg'):
                        for DeviceUnit in Devices:
                            if Devices[DeviceUnit].DeviceID == child.attrib['tid']:
                                Devices[DeviceUnit].Update(0, child.attrib['v'])

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level) + "', Hue: " + str(Hue))

    def onNotification(self, Data):
        Domoticz.Debug("onNotification: " + str(Data))

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")
        if  self.eCoalConn.Connected():
            Domoticz.Debug("onHeartbeat called, Connection is alive.")
        else:
            self.eCoalConn.Connect()
            Domoticz.Debug("onHeartbeat reconnect")

        data = 'device' + Parameters["Mode1"]
        for x in Devices:
            data += "&" + Devices[x].DeviceID
        b64Authentication = base64.b64encode((Parameters["Username"] + ":" + Parameters["Password"]).encode()).decode("utf-8")
        headers = { 'Content-Type': 'text/xml; charset=utf-8', \
                    'Connection': 'keep-alive', \
                    'Accept': 'Content-Type: text/html; charset=UTF-8', \
                    'Host': Parameters["Address"]+":"+Parameters["Port"], \
                    'Authentication':'Basic ' + b64Authentication, \
                    'User-Agent':'Domoticz/1.0', \
                    'Content-Length' : "%d"%(len(data)) }
        self.eCoalConn.Send({'Verb':'GET', 'URL':'/getregister.cgi?'+data, 'Headers':headers})

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Data):
    global _plugin
    _plugin.onNotification(Data)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

def UpdateDevice(Unit, nValue, sValue):
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it
    if (Unit in Devices):
        if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != str(sValue)):
            Domoticz.Log("Update " + str(Devices[Unit].nValue) + " -> " + str(nValue)+",'" + Devices[Unit].sValue + "' => '"+str(sValue)+"' ("+Devices[Unit].Name+")")
            Devices[Unit].Update(nValue, str(sValue))
    return

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device DeviceID:  " + str(Devices[x].DeviceID))
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
