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
        <param field="Mode2" label="Rejestry danych" width="400px" required="true" default="tkot_value,t,Temp. kocioł;tpow_value,t,Temp. powrotu;tpod_value,t,Temp. podajnika;tcwu_value,t,Temp. CVU;twew_value,t,Temp. wewnętrzna;tzew_value,t,Temp. zewnętrzna;tsp_value,t,Temp. spalin;fuel_level,p,Poziom paliwa"/>
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

class BasePlugin:
    self.units = {"t":"Temperature","p":"Percentage","b":"Barometer"}

    def onStart(self):
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
        Domoticz.Debug("onStart called")

        if (len(Devices) == 0):
            for i, x in enumerate(Parameters["Mode2"].split(";")):
                device_id, device_type, device_name = x.split(",")
                Domoticz.Debug("Create device: " + device_name)
                Domoticz.Device(Name=device_name, Unit=i+1, DeviceID=device_id, TypeName=self.units[device_type], Used=1).Create()

        # Utworzenie połączenia ze sterownikiem eCoal
        #Conn = Domoticz.Connection(Name="eCoal Connection", Transport="TCP/IP", Protocol="XML", Address=Parameters["Address"], Port=Parameters["Port"])
        #Conn.Connect()

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called. Status: " + str(Status))

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level) + "', Hue: " + str(Hue))

    def onNotification(self, Data):
        Domoticz.Debug("onNotification: " + str(Data))

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")

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

def onMessage(Connection, Data, status, extra):
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
