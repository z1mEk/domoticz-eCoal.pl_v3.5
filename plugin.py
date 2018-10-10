"""
<plugin key="eSterownik" name="eSterownik.pl v3.5" author="z1mEk" version="0.9.2" wikilink="https://github.com/z1mEk/domoticz-eCoal.pl_v3.5.git" externallink="https://esterownik.pl/nasze-produkty/ecoal-v35">
    <description>
        <h2>eSetrownik v3.5 - Domoticz plugin ver. 0.9.1</h2>
        <p>Dodatek zapewnia integrację z eSterownik, sterownikami firmy eSterownik.pl przeznaczonym do sterowania kotłów wodnych na paliwo stałe takich jak Pello, eCoal, DEFRO SMART II, bruli.pl oraz systemu Bero</p>
        <p>Więcej informacji o sterowniku znajduje się na stronie <a href="https://esterownik.pl/nasze-produkty/ecoal-v35">https://esterownik.pl/nasze-produkty/ecoal-v35</a></p>
        <p>Opis konfiguracji znajduje się w repozytorium kodu GitHub <a href="https://github.com/z1mEk/domoticz-eSterownik_v3.5/blob/master/README.md">z1mEk/domoticz-eSterownik_v3.5</a></p>
        <p>Wszelkie błędy i pomysły proszę zgłaszać jako <a href="https://github.com/z1mEk/domoticz-eSterownik_v3.5/issues/new">nowy issue na GitHub</a> (szybsza reakcja autora) lub bezpośrednio na e-mail: gabriel.zima@wp.pl</p>
        <p>Zapszaszam do współpracy przy rozwoju pluginu jak również do opracowania pluginów do innych sterowników i urządzeń.</p>
    </description>
    <params>
        <param field="Address" label="Adres IP" width="100px" required="true" default="192.168.1.1"/>
        <param field="Port" label="Port" width="30px" required="true" default="80"/>
        <param field="Username" label="Użytkownik" width="80px" required="true" default="root"/>
        <param field="Password" label="Hasło" width="80px" required="true" default="root"/>
        <param field="Mode1" label="ID urządzenia" width="30px" required="true" default="0"/>
        <param field="Mode2" label="Rejestry danych" width="400px" required="true" default="tkot_value,t,Temp. kocioł;tpow_value,t,Temp. powrotu;tpod_value,t,Temp. podajnika;tcwu_value,t,Temp. CWU;twew_value,t,Temp. wewnętrzna;tzew_value,t,Temp. zewnętrzna;tsp_value,t,Temp. spalin;fuel_level,p,Poziom paliwa"/>
        <param field="Mode3" label="Częstotliwość odczytu" width="30px" required="true" default="30"/>
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
import xml.etree.ElementTree as et
import subprocess

class BasePlugin:
    eCoalConn = None
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

        #self.eCoalConn = Domoticz.Connection(Name="eCoal Connection", Transport="TCP/IP", Protocol="HTTP", Address=Parameters["Address"], Port=Parameters["Port"])
        #self.eCoalConn.Connect()
        Domoticz.Heartbeat(int(Parameters["Mode3"]))

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called. Status: " + str(Status))

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called")
        if Data['Status'] == '200':
            httpBody = Data['Data']
            xmlBody = et.fromstring(httpBody)
            if 'status' in xmlBody.attrib:
                if xmlBody.attrib['status'] == "ok":
                    for child in xmlBody.iter('reg'):
                        for DeviceUnit in Devices:
                            if Devices[DeviceUnit].DeviceID == child.attrib['tid'] and 'v' in child.attrib:
                                Devices[DeviceUnit].Update(0, child.attrib['v'])

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level) + "', Hue: " + str(Hue))

    def onNotification(self, Data):
        Domoticz.Debug("onNotification: " + str(Data))

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect called")
        #Connection.Connect()

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")
        data = 'device=' + Parameters["Mode1"]
        for x in Devices:
            data += "&" + Devices[x].DeviceID
#        headers = {
#                    'Accept': '*/*', \
#                    'Host': Parameters["Address"]
#                   }
#        self.eCoalConn.Send({'Verb':'GET', 'URL':'/getregister.cgi?'+data, 'Headers':headers})
        # Workaround - curl instead Domoticz.Cennection :(
        bash_command = 'curl -v -H "Host: '+Parameters["Address"]+':'+Parameters["Port"]+'" -H "User-Agent: Domoticz/1.0" -H "Accept: */*" -H "Authorization: Basic `echo -n '+Parameters["Username"]+':'+Parameters["Password"]+' | base64`" "http://'+Parameters["Address"]+':'+Parameters["Port"]+'/getregister.cgi?'+data+'"'
        output = subprocess.check_output(['bash','-c', bash_command]).decode("utf-8")
        if output.find('status="ok"') > 0:
            status = '200'
        else:
            status = '400'
        Data = {
            'Status': status,
            'Data': output
        }
        Domoticz.Debug(str(Data))
        onMessage(self.eCoalConn, Data)

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
