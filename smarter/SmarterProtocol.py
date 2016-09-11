# -*- coding: utf8 -*-

import traceback
import struct
import operator

#------------------------------------------------------
# SMARTER PROTOCOL INTERFACE
#
# Python protocol interface to iKettle 2.0 & Smarter Coffee Devices
#
# https://github.com/Tristan79/iBrew
#
# Copyright © 2016 Tristan (@monkeycat.nl)
#
# Out of order! (rev 7)
#------------------------------------------------------

# In the end I should have made classes of the types...

#------------------------------------------------------
# EXCEPTION CLASS
#------------------------------------------------------


KettleNoMachineHeat             = 30
KettleNoMachineOff              = 31
KettleNoMachineSettings         = 32
KettleNoMachineStoreSettings    = 33
KettleNoMachineHistory          = 34
CoffeeNoMachineStrength         = 50
CoffeeNoMachineGrinder          = 51
CoffeeNoMachineCups             = 52
CoffeeNoMachineHotplateOn       = 53
CoffeeNoMachineHotplateOff      = 54
CoffeeNoMachinesBrew            = 55
CoffeeNoMachineOff              = 56
CoffeeNoMachineSettings         = 57
CoffeeNoMachineStoreSettings    = 58
CoffeeNoMachineHistory          = 59
CoffeeNoMachineSingleCupMode    = 60
CoffeeNoMachineCarafe           = 61
KettleFailedStoreSettings       = 70
CoffeeFailedStoreSettings       = 90

ConvertRawNumber                = 110
ConvertNumberRaw                = 111
ConvertCodeNumber               = 112
ConvertNumberCode               = 113

WebServerListen                = 100
WebServerStartFailed           = 101

WebServerStopMonitor           = 102
WebServerStopMonitorWeb        = 103
WebServerStopWeb               = 104

SmarterClientFailedStop        = 105
SmarterClientFailedStopThread  = 106


class SmarterError(Exception):

    def __init__(self, err, msg):
        print(traceback.format_exc())
        print str(msg)
        self.msg = msg
        self.err = err


class SmarterErrorOld(Exception):
    def __init__(self, msg):
        print str(msg)
        print(traceback.format_exc())
        self.msg = msg


#------------------------------------------------------
# PROTOCOL CLASS
#------------------------------------------------------


class SmarterProtocol:

    DirectHost = "192.168.4.1"
    Port       = 2081
    Fahrenheid = False


    #------------------------------------------------------
    # MESSAGES CONSTANTS
    #------------------------------------------------------


    MessageTail               = 0x7e
    MessagePayloadTail        = 0x7d
    MessageOffBase            = 0x7f


    #------------------------------------------------------
    # MESSAGE INFO
    #------------------------------------------------------


    # device
    CommandDeviceTime         = 0x02
    CommandResetSettings      = 0x10
    CommandDeviceInfo         = 0x64
    CommandUpdate             = 0x6d
    Command69                 = 0x69

    # wifi
    CommandWifiNetwork        = 0x05
    CommandWifiPassword       = 0x07
    CommandWifiJoin           = 0x0c
    CommandWifiScan           = 0x0d
    CommandWifiLeave          = 0x0f
    CommandWifiFirmware       = 0x6a

    # coffee
    CommandBrew               = 0x33
    CommandCoffeeStop         = 0x34
    CommandStrength           = 0x35
    CommandCups               = 0x36
    CommandBrewDefault        = 0x37
    CommandCoffeeSettings     = 0x48
    CommandCoffeeStoreSettings = 0x38
    CommandGrinder            = 0x3c
    CommandHotplateOn         = 0x3e
    CommandCoffeeHistory      = 0x46
    CommandHotplateOff        = 0x4a
    CommandCarafe             = 0x4c
    CommandSetCarafe          = 0x4b
    CommandSingleCupMode      = 0x4f
    CommandSetSingleCupMode   = 0x4e
    CommandStoreTimer         = 0x40
    CommandTimers             = 0x41
    CommandDisableTimer       = 0x43
 
    # kettle
    CommandHeat               = 0x15
    CommandKettleStop         = 0x16
    CommandHeatFormula        = 0x19
    CommandHeatDefault        = 0x21
    Command20                 = 0x20
    Command22                 = 0x22
    Command23                 = 0x23
    Command30                 = 0x30
    CommandKettleStoreSettings = 0x1f
    CommandKettleHistory      = 0x28
    CommandKettleSettings     = 0x2e
    CommandStoreBase          = 0x2a
    CommandBase               = 0x2b
    CommandCalibrate          = 0x2c
    


    # device
    ResponseCommandStatus     = 0x03
    ResponseWirelessNetworks  = 0x0e
    ResponseKettleHistory     = 0x29
    ResponseDeviceInfo        = 0x65
    ResponseWifiFirmware      = 0x6b

    # coffee
    ResponseCoffeeSettings    = 0x49
    ResponseCoffeeStatus      = 0x32
    ResponseTimers            = 0x42
    ResponseCoffeeHistory     = 0x47
    ResponseCarafe            = 0x4d
    ResponseSingleCupMode     = 0x50
    
    # kettle
    ResponseKettleStatus      = 0x14
    ResponseBase              = 0x2d
    ResponseKettleSettings    = 0x2f
    
    # format kettle? coffee? response to command, description
    CommandMessages = {
        CommandDeviceTime       : (True,True,[ResponseCommandStatus],"Set device time"),
        CommandWifiNetwork      : (True,True,[ResponseCommandStatus],"Set wireless network name"),
        CommandWifiPassword     : (True,True,[ResponseCommandStatus],"Set wireless network password"),
        CommandWifiJoin         : (True,True,[],"Join wireless network"),
        CommandWifiScan         : (True,True,[ResponseWirelessNetworks],"Scan for wireless networks"),
        CommandWifiLeave        : (True,True,[],"Wireless network direct mode"),
        CommandResetSettings    : (True,True,[ResponseCommandStatus],"Reset default user settings"),
        CommandHeat             : (True,False,[ResponseCommandStatus],"Heat kettle"),
        CommandKettleStop       : (True,False,[ResponseCommandStatus],"Stop heating kettle"),
        CommandHeatFormula      : (True,False,[ResponseCommandStatus],"Heat kettle using formula mode"),
        CommandKettleStoreSettings : (True,False,[ResponseCommandStatus],"Set kettle default user settings"),
        Command20               : (True,False,[ResponseCommandStatus],"Working unknown command (turn on?)"),
        CommandHeatDefault      : (True,False,[ResponseCommandStatus],"Heat kettle with default settings"),
        Command22               : (True,False,[ResponseCommandStatus],"Working unknown command (turn on?)"),
        Command23               : (True,False,[ResponseCommandStatus],"Working unknown command (turn on?)"),
        CommandKettleHistory    : (True,False,[ResponseKettleHistory],"Get kettle history"),
        CommandStoreBase        : (True,False,[],"Set water sensor base value"),
        CommandBase             : (True,False,[ResponseBase,ResponseCommandStatus],"Get water sensor base value"),
        CommandCalibrate        : (True,False,[ResponseBase,ResponseCommandStatus],"Calibrate water sensor"),
        CommandKettleSettings   : (True,False,[ResponseKettleSettings],"Get default kettle user settings"),
        Command30               : (True,False,[ResponseCommandStatus],"Working unknown command"),
        CommandBrew             : (False,True,[ResponseCommandStatus],"Start coffee brewing"),
        CommandCoffeeStop       : (False,True,[ResponseCommandStatus],"Stop coffee brewing"),
        CommandStrength         : (False,True,[ResponseCommandStatus],"Set strength of the coffee to brew"),
        CommandCups             : (False,True,[ResponseCommandStatus],"Set number of cups to brew"),
        CommandBrewDefault      : (False,True,[ResponseCommandStatus],"Start coffee brewing using machine settings"),
        CommandCoffeeStoreSettings : (False,True,[],"Set coffee machine default user settings"),
        CommandGrinder          : (False,True,[ResponseCommandStatus],"Toggle grinder"),
        CommandHotplateOn       : (False,True,[ResponseCommandStatus],"Turn on hotplate"),
        CommandCarafe           : (False,True,[ResponseCoffeeStatus,ResponseCommandStatus],"Get coffee carafe required"),
        CommandSingleCupMode    : (False,True,[ResponseSingleCupMode,ResponseCommandStatus],"Get single coffee cup mode"),
        CommandStoreTimer       : (False,True,[ResponseCommandStatus],"Store timer"),
        CommandTimers           : (False,True,[ResponseTimers,ResponseCommandStatus],"Get timers"),
        CommandDisableTimer     : (False,True,[ResponseCommandStatus],"Timer event handled"),
        CommandSetCarafe        : (False,True,[ResponseCommandStatus],"Set coffee carafe required"),
        CommandSetSingleCupMode : (False,True,[ResponseCommandStatus],"Set single coffee cup mode"),
        CommandCoffeeSettings   : (False,True,[ResponseCoffeeSettings,ResponseCommandStatus],"Get default coffee machine user settings"),
        CommandCoffeeHistory    : (False,True,[ResponseCoffeeHistory],"Get coffee machine history"),
        CommandHotplateOff      : (False,True,[ResponseCommandStatus],"Turn off hotplate"),
        CommandDeviceInfo       : (True,True,[ResponseDeviceInfo],"Get device info"),
        Command69               : (True,True,[ResponseCommandStatus],"Working unknown command"),
        CommandWifiFirmware     : (True,True,[ResponseWifiFirmware],"Get wifi firmware info"),
        CommandUpdate           : (True,True,[],"Device firmware update")
    }



    def __con(self,coffee,kettle):
        if coffee and kettle:
            return [self.DeviceKettle,self.DeviceCoffee]
        if coffee and not kettle:
            return [self.DeviceCoffee]
        if not coffee and kettle:
            return [self.DeviceKettle]
        else:
            return []


    def CommandToJSON(self):
        json = dict()
        for command in self.CommandMessages:
            message = self.CommandMessages[command]
            json[command] = { 'device' : self.__con(message[0],message[1]), 'description' : self.message_description(command) }
        return json

    def ResponseToJSON(self):
        json = dict()
        for response in self.ResponseMessages:
            if self.message_is_response(response):
                message = self.ResponseMessages[response]
                json[response] = { 'device' : self.__con(message[0],message[1]), 'description' : self.message_description(response) }
        return json


    def StatusToJSON(self):
        return { self.ResponseKettleStatus : { 'device' : [self.DeviceKettle], 'description' : self.message_description(self.ResponseKettleStatus) },
                 self.ResponseCoffeeStatus : { 'device' : [self.DeviceCoffee], 'description' : self.message_description(self.ResponseCoffeeStatus) }
                }


    # format: kettle?, coffee? (None is unnknown), minimal length (0 = variable), response to command, description
    ResponseMessages = {
        #incomplete? ... chech the first one...
        ResponseCommandStatus   : (True,True,3,[CommandDeviceTime,CommandWifiNetwork,CommandWifiPassword,CommandResetSettings,CommandHeat,CommandKettleStop,CommandHeatFormula,CommandKettleStoreSettings,Command20,CommandHeatDefault,Command22,Command23,CommandBase,CommandCalibrate,Command69,CommandStoreTimer,CommandTimers,CommandDisableTimer,Command30,CommandSetCarafe,CommandSetSingleCupMode,CommandStrength,CommandCups,CommandGrinder,CommandHotplateOn,CommandSingleCupMode,CommandCarafe,CommandHotplateOff,CommandCoffeeSettings,CommandBrew,CommandCoffeeStop,CommandBrewDefault],"Command status",[]),
        ResponseWirelessNetworks: (True,True,0,[CommandWifiScan],"Wireless networks list",[]),
        ResponseKettleHistory   : (True,False,0,[CommandKettleHistory],"Kettle history",[]),
        ResponseCoffeeHistory   : (False,True,0,[CommandCoffeeHistory],"Coffee machine history",[]),
        ResponseBase            : (True,False,4,[CommandBase,CommandCalibrate],"Water sensor base value",[]),
        ResponseKettleSettings  : (True,False,9,[CommandKettleSettings],"Default kettle user settings",[]),
        ResponseKettleStatus    : (True,False,7,[],"Kettle status",[]),
        ResponseDeviceInfo      : (True,True,4,[CommandDeviceInfo],"Device info",[]),
        ResponseWifiFirmware    : (True,True,0,[CommandWifiFirmware],"Wifi firmware info",[]),
        ResponseCarafe          : (False,True,3,[CommandCarafe],"Carafe required",[]),
        ResponseCoffeeStatus    : (False,True,0,[],"Coffee machine status",[]),
        ResponseCoffeeSettings  : (False,True,6,[CommandCoffeeSettings],"Default coffee machine user settings",[]),
        ResponseSingleCupMode   : (False,True,3,[CommandSingleCupMode],"Single coffee cup mode",[]),
        ResponseTimers          : (False,True,0,[CommandTimers],"Stored timers",[])

    }


    def message_response_length(self,id):
        if self.message_is_response(id):
            return self.ResponseMessages[id][2]
        return 0
    
    
    def message_description(self,id):
        if self.message_is_response(id) or self.message_is_status(id):
            return self.ResponseMessages[id][4]
        elif self.message_is_command(id):
            return self.CommandMessages[id][3]
        else:
            return "Unknown message"


    def message_connection_type(self,id):
        if self.message_is_response(id):
            return "Command"
        elif self.message_is_command(id):
            return "Response"
        else:
            return ""

    def message_connection(self,id):
        if self.message_is_response(id):
            x = self.ResponseMessages[id][3]
            if x: x.sort()
            return x
        elif self.message_is_command(id):
            x = self.CommandMessages[id][2]
            if x: x.sort()
            return x
        else:
            return []


    def message_is_known(self,id):
        return self.message_is_response(id) or self.message_is_command(id) or self.message_is_status(id)


    def message_is_response(self,id):
        if id != self.ResponseKettleStatus and id != self.ResponseCoffeeStatus:
            return self.ResponseMessages.has_key(id)
        return False


    def message_is_status(self,id):
        if id == self.ResponseKettleStatus or id == self.ResponseCoffeeStatus:
            return True
        return False


    def message_is_command(self,id):
        return self.CommandMessages.has_key(id)


    def message_is_type(self,id):
        if self.message_is_command(id):
            return "Command"
        elif id == self.ResponseKettleStatus or id == self.ResponseCoffeeStatus:
            return "Status"
        else:
            return "Response"

    # internal use here only
    def message_supported(self,state):
        if state is None:
            return "?"
        if state:
            return "✓"
        else:
            return "✕"


    def message_kettle(self,id):
        if self.message_is_command(id):
            return self.CommandMessages[id][0]
        if self.message_is_response(id) or self.message_is_status(id):
            return self.ResponseMessages[id][0]


    def message_kettle_supported(self,id):
        return self.message_supported(self.message_kettle(id))


    def message_coffee_supported(self,id):
        return self.message_supported(self.message_coffee(id))


    def message_coffee(self,id):
        if self.message_is_command(id):
            return self.CommandMessages[id][1]
        if self.message_is_response(id) or self.message_is_status(id):
            return self.ResponseMessages[id][1]


    #------------------------------------------------------
    # RAW <-> BASIC TYPE
    #------------------------------------------------------

    def raw_to_number(self,raw):
        try:
            return struct.unpack('B',raw)[0]
        except Exception:
            # DEBUG LEN RAW!!! (probably tornado)
            raise SmarterError(ConvertRawNumber,"Could not convert raw data to number" + str(len(raw)))

    def number_to_raw(self,number):
        try:
            i = int(number)
        except Exception:
            raise SmarterError(ConvertNumberRaw,"Could not convert number to raw data")
        
        if number < 0 or number > 256:
            raise SmarterError(ConvertNumberRaw,"Could not to convert number " + str(number) + " to raw data, because it is out of range [0..255]")
        try:
            return struct.pack('B',number)
        except Exception:
            raise SmarterError(ConvertNumberRaw,"Could not convert number to raw data: " + str(number))


    def raw_to_code(self,raw):
        return self.number_to_code(self.raw_to_number(raw))


    def code_to_raw(self,code):
        return self.number_to_raw(self.code_to_number(code))


    def code_to_number(self,code):
        try:
            return int(code,16)
        except Exception:
            raise SmarterError(ConvertCodeNumber,"Could not convert code to number: " + code )


    def number_to_code(self,number):
        try:
            code = hex(number)[2:4]
        except Exception:
            raise SmarterError(ConvertNumberCode,"Could not convert number to code: " + str(number))
        if number < 16:
            return '0' + code
        return code


    def text_to_raw(self,text):
        return text
        # FIX ERROR CHECKING + CODE
        return 
        for i in range(0,len(text)):
            raw =+ number_to_raw(text[i])
        return raw


    def raw_to_text(self,raw):
        # FIX ERROR CHECKING + CODE
        for i in range(0,len(raw)):
            raw =+ raw_to_number(raw_[i])
        return raw


    #------------------------------------------------------
    # RAW HEX STRING <-> RAW
    #------------------------------------------------------

    # Convert raw data to hex string without 0x seperated by spaces
    def message_to_codes(self,message,space = False):
        raw = ""
        for i in range(0,len(message)):
            try:
                raw += self.raw_to_code(message[i])
            except Exception:
                raise SmarterErrorOld("Could not decode message at position: " + str(i))
            if space and i != len(message)-1:
                raw += " "
        return raw


    # Convert hex string without 0x input maybe seperated by spaces or not
    def codes_to_message(self,string):
        message = ""
        code = string.strip()
        
        if len(code) <= 2:
            return self.code_to_raw(code)
        
        if len(code) % 2 == 0 and code[2] != " ":
            for i in range(0,len(code) / 2):
                try:
                    message += self.code_to_raw(code[i*2]+code[i*2+1])
                except Exception:
                    raise SmarterErrorOld("Could not encode code \'" + code + "\' at position: " + str(i*2+1))
 
        elif len(code) % 3 == 2:
            for i in range(0,(len(code) / 3)+1):
                if i > 0:
                    if code[i*3-1] != ' ':
                        raise SmarterErrorOld("Expected space character in code  \'" + code + "\' at position: " + str(i*3)+1)
                try:
                    message += self.code_to_raw(code[i*3]+code[i*3+1])
                except Exception:
                    raise SmarterErrorOld("Could not encode code \'" + code + "\' at position: " + str(i*3+1))
    
        else:
            raise SmarterErrorOld("Missing character in code \'" + code + "\'  at position: " + str(len(code)+1))

        return message
    

    #------------------------------------------------------
    # RAW <-> TYPE
    #------------------------------------------------------


    #------------------------------------------------------
    # DEVICE & FIRMWARE ARGUMENT WRAPPER
    #------------------------------------------------------


    DeviceKettle              = 0x01
    DeviceCoffee              = 0x02

    DeviceStringKettle        = "iKettle 2.0"
    DeviceStringCoffee        = "Smarter Coffee"

    KettleFirmwareVerified    = [19]
    CoffeeFirmwareVerified    = [20,22]
    
    
    def is_kettle(self,device):
        return device == self.DeviceKettle


    def is_kettle_verified(self,firmware):
        return firmware in self.KettleFirmwareVerified
    
    
    def is_coffee_verified(self,firmware):
        return firmware in self.CoffeeFirmwareVerified
    
    
    def is_coffee(self,device):
        return device == self.DeviceCoffee


    def firmware_verified(self,device,firmware):
        if (device == self.DeviceCoffee and self.is_coffee_verified(firmware)) or (device == self.DeviceKettle and self.is_kettle_verified(firmware)):
            return "iBrew certified firmware"
        return "Unsupported firmware"


    def device_to_string(self,device):
        if self.is_kettle(device):
            return self.DeviceStringKettle
        elif self.is_coffee(device):
            return self.DeviceStringCoffee
        else:
            return "Unknown"


    def device_info(self,device,firmware):
        return self.device_to_string(device)  + " (" + self.firmware_verified(device,firmware) + " v" + str(firmware) + ")"


    #------------------------------------------------------
    # STRENGTH ARGUMENT WRAPPER
    #------------------------------------------------------


    CoffeeWeak                = 0x00
    CoffeeMedium              = 0x01
    CoffeeStrong              = 0x02
    
    CoffeeStringWeak          = "weak"
    CoffeeStringMedium        = "medium"
    CoffeeStringStrong        = "strong"

    # approx measure it?
    CoffeeGramsStrong         = 200
    CoffeeGramsMedium         = 150 #???
    CoffeeGramsWeak           = 100 #???


    def check_strength(self,strength):
        if strength == self.CoffeeMedium or strength == self.CoffeeStrong or strength == self.CoffeeWeak:
            return strength
        else:
            raise SmarterErrorOld("Invalid coffee strength ["+self.CoffeeStringWeak+", "+self.CoffeeStringMedium+", "+self.CoffeeStringStrong +"]: " + strength)


    def strength_to_raw(self,strength):
        return self.number_to_raw(self.check_strength(strength))


    def raw_to_strength(self,raw):
        return self.check_strength(self.raw_to_number(raw))
    
    def strength_to_string(self,number):
        if self.CoffeeWeak == number:
            return self.CoffeeStringWeak
        elif self.CoffeeMedium == number:
            return self.CoffeeStringMedium
        elif self.CoffeeStrong == number:
            return self.CoffeeStringStrong
        else:
            raise SmarterErrorOld("Invalid coffee strength ["+CoffeeStringWeak+", "+CoffeeStringMedium+", "+CoffeeStringStrong +"] " + self.number_to_code(strength))

    def string_to_strength(self,strength):
        if strength.strip().lower() == CoffeeStringWeak:
            return self.CoffeeWeak
        elif strength.strip().lower() == CoffeeStringMedium:
            return self.CoffeeMedium
        elif strength.strip().lower() == CoffeeStringStrong:
            return self.CoffeeStrong
        else:
            raise SmarterErrorOld("Invalid coffee strength ["+self.CoffeeStringWeak+", "+self.CoffeeStringMedium+", "+self.CoffeeStringStrong +"] " + strength)


    #------------------------------------------------------
    # TEMPERATURE ARGUMENT WRAPPER
    #------------------------------------------------------

    def is_on_base(self,raw):
        return self.raw_to_number(raw) != self.MessageOffBase
 
 
    def string_base_on_off(self,onbase):
        if onbase:
            return "On"
        else:
           return "Off"
           
    def celsius_to_fahrenheid(self,temperature):
        return ((temperature * 9) / 5) + 32
    
    
    def fahrenheid_to_celsius(self,temperature):
        return ((temperature - 32) * 5) / 9
    
    
    def check_temperature_celsius(self,temperature):
        # if fahrenheid then converto...
        # if self.Fahrenheid
        if temperature < 0 or temperature > 100 and not self.is_on_base(self.number_to_raw(temperature)):
            if self.Fahrenheid:
                raise SmarterErrorOld("Temperature out of range ["+self.celsius_to_fahrenheid(0)+".."+self.celsius_to_fahrenheid(100)+"] ºK: " + str(temperature))
            else:
                raise SmarterErrorOld("Temperature out of range [0..100] ºC: " + str(temperature))
        return temperature
    
    
    def check_temperature(self,temperature):
        if self.Fahrenheid:
            return self.fahrenheid_to_celsius(temperature)
        else:
            return temperature


    def raw_to_temperature(self,raw):
        if self.is_on_base(raw):
            return self.check_temperature_celsius(self.raw_to_number(raw))
        return 0


    def temperature_to_raw(self,temperature):
        return self.number_to_raw(self.check_temperature_celsius(temperature))


    def temperature_to_string(self,temperature):
        if self.Fahrenheid:
            return str(temperature)+" ºF"
        else:
            return str(temperature)+" ºC"


    def temperature_symbol_to_string(self):
        if self.Fahrenheid:
            return "ºF"
        else:
            return "ºC"

    def temperature_metric_to_string(self):
        if self.Fahrenheid:
            return "fahrenheid"
        else:
            return "celsius"

    def string_to_temperature(self,temperature):
        try:
            if self.Fahrenheid:
                return self.fahrenheid_to_celsius(int(temperature))
            else:
                return int(temperature)
        except Exception:
            raise SmarterErrorOld("Temperature is not a number: " + temperature)


    #------------------------------------------------------
    # HOTPLATE KEEPWARM ARGUMENT WRAPPER
    #------------------------------------------------------

    def string_to_hotplate(self,string):
        try:
            return int(string)
        except Exception:
            raise SmarterErrorOld("Hotplate timer is not a number: " + string)

    def check_hotplate(self,timer):
        if timer != 0 and (timer < 5 or timer > 35):
            raise SmarterErrorOld("Hotplate timer out of range [0=Off] or [5..35] minutes: " + str(timer))
        return timer

    def check_hotplate_on(self,timer):
        if timer > 0: return True
        else: return False

    def raw_to_hotplate(self,raw):
        return self.check_hotplate(self.raw_to_number(raw))


    def hotplate_to_raw(self,timer):
        return self.number_to_raw(self.check_hotplate(timer))


    #------------------------------------------------------
    # KEEPWARM ARGUMENT WRAPPER
    #------------------------------------------------------

    def string_to_keepwarm(self,string):
        try:
            return int(string)
        except Exception:
            raise SmarterErrorOld("Keepwarm timer is not a number: " + string)


    def check_keepwarm(self,timer):
        if timer != 0 and (timer < 1 or timer > 30):
            raise SmarterErrorOld("Kettle keep warm timer out of range [0=Off] or [5..30] minutes: " + str(timer))
        return timer


    def check_keepwarm_on(self,timer):
        if timer > 0: return True
        else: return False
    
    
    def raw_to_keepwarm(self,raw):
        return self.check_hotplate(self.raw_to_number(raw))


    def keepwarm_to_raw(self,timer):
        return self.number_to_raw(self.check_keepwarm(timer))


    #------------------------------------------------------
    # WATERSENSOR ARGUMENT WRAPPER
    #------------------------------------------------------

    def check_watersensor(self, watersensor):
        if watersensor < 0 or watersensor > 4095:
            raise SmarterErrorOld("Watersensor out of range [0..4095]")
        return watersensor
        
    def raw_to_watersensor(self,raw_low,raw_high):
        return self.check_watersensor(self.raw_to_number(raw_low) * 256 + self.raw_to_number(raw_high))


    def watersensor_to_raw(self,watersensor):
        return self.number_to_raw(watersensor / 256) + self.number_to_raw(watersensor % 256)

    def string_to_watersensor(self,string):
        try:
            watersensor = int(string)
        except Exception:
            raise SmarterErrorOld("Not a watersensor value")
        return self.check_watersensor(watersensor)
 
 
 
    #------------------------------------------------------
    # TIMER ARGUMENT WRAPPER
    #------------------------------------------------------

    TimerAll = 0x00
    Timer1 = 0x01
    Timer2 = 0x02
    Timer3 = 0x03
    Timer4 = 0x04
    
    Timer = {
        TimerAll : "Timer All",
        Timer1 : "Timer 1",
        Timer2 : "Timer 2",
        Timer3 : "Timer 3",
        Timer4 : "Timer 4"
    }
    
    #------------------------------------------------------
    # BOOLEAN ARGUMENT WRAPPER
    #------------------------------------------------------

    def raw_to_bool(self,raw):
        bool = self.raw_to_number(raw)
        if bool > 1:
            raise SmarterErrorOld("Not a boolean value: " + str(int))
        if bool == 1:
            return True
        return False
 
 
    def bool_to_raw(self,boolean):
        return self.number_to_raw(boolean)


    def string_to_bool(self,boolean):
        if boolean.lower() == "on" or boolean.lower() == "true" or boolean.lower() == "1":
            return True
        if boolean.lower() == "off" or boolean.lower() == "false" or boolean.lower() == "0":
            return False
        else:
            raise SmarterErrorOld("Unknown boolean [true/1/on/false/0/off]: " + str(boolean))

    #------------------------------------------------------
    # CUPS ARGUMENT WRAPPER
    #------------------------------------------------------

    def check_cups(self,cups_raw):
        cups = cups_raw % 16
        if cups < 1 or cups > 12:
            raise SmarterErrorOld("Unknown coffee cups [1..12]: " + str(cups))
        return cups

    def check_cups_brew(self,cups_raw):
        cups = cups_raw % 16
        if cups < 0 or cups > 12:
            raise SmarterErrorOld("Unknown brew(ed) coffee cups [0..12]: " + str(cups))
        return cups

    def raw_to_cups_brew(self,cups_raw):
        return self.check_cups_brew(self.raw_to_number(cups_raw) / 16)


    def raw_to_cups(self,raw):
        return self.check_cups(self.raw_to_number(raw))


    def cups_to_raw(self,cups):
        return self.number_to_raw(self.check_cups(cups))
    

    def string_to_cups(self,string):
        try:
            cups = int(string)
        except Exception:
            raise SmarterErrorOld("Unknown coffee cups [1..12]: " + string)
        return self.check_cups(cups)


    def cups_to_string(self,cups):
        if cups == 1:
            return "a cup"
        else:
            return str(cups) + " cups"


    #------------------------------------------------------
    # WATERLEVEL ARGUMENT WRAPPER
    #------------------------------------------------------


    CoffeeWaterEmpty = 0x00
    CoffeeWaterLow   = 0x01
    CoffeeWaterHalf  = 0x02
    CoffeeWaterFull  = 0x03

    WaterLevel = {
        CoffeeWaterEmpty : "empty",
        CoffeeWaterLow   : "low",
        CoffeeWaterHalf  : "half",
        CoffeeWaterFull  : "full"
    }

    def waterlevel(self,level):
        if self.WaterLevel.has_key(level):
            return self.WaterLevel[level]
        else:
            return "unknown water level [0..3]: " + self.number_to_code(level)


    def check_waterlevel(self,waterlevel_raw):
        water = waterlevel_raw % 16
        if water < 0 or water > 3:
            raise SmarterErrorOld("Unknown waterlevel [0..3]: " + str(water))
        return water


    def raw_to_waterlevel(self,raw):
        return self.check_waterlevel(self.raw_to_number(raw))


    def raw_to_waterlevel_bit(self,raw):
        return self.raw_to_number(raw) / 16

   
    #------------------------------------------------------
    # COMMAND STATUS INFO WRAPPER
    #------------------------------------------------------


    StatusSucces              = 0x00
    StatusBusy                = 0x01
    StatusNoCarafe            = 0x02
    StatusNoWater             = 0x03
    StatusFailed              = 0x04
    StatusNoCarafeUnknown     = 0x05
    StatusNoWaterUnknown      = 0x06
    StatusNoWaterAborted      = 0x07
    StatusInvalidTimer        = 0x0d
    StatusErrorWifi           = 0x68
    StatusInvalid             = 0x69
 
    StatusCommand = {
        StatusSucces           : "success",
        StatusBusy             : "busy",
        StatusNoCarafe         : "no carafe",
        StatusNoWater          : "no water",
        StatusFailed           : "failed",
        StatusNoCarafeUnknown  : "no carafe",  # which one?
        StatusNoWaterUnknown   : "no water",   # which one?
        StatusNoWaterAborted   : "low water could not finish",
        StatusInvalidTimer     : "timer error",
        StatusErrorWifi        : "wifi error",
        StatusInvalid          : "invalid command"
    }


    def status_command(self,status):
        if self.is_status_command(status):
            return self.StatusCommand[status]
        else:
            return "Unknown Command Status " + self.number_to_code(status)


    #------------------------------------------------------
    # KETTLE STATUS INFO WRAPPER
    #------------------------------------------------------


    KettleReady               = 0x00
    KettleHeating             = 0x01
    KettleKeepWarm            = 0x02
    KettleCycleFinished       = 0x03
    KettleBabyCooling         = 0x04

    StatusKettle = {
        KettleReady             : "ready",
        KettleHeating           : "heating",
        KettleKeepWarm          : "keep warm",
        KettleCycleFinished     : "cycle finished",
        KettleBabyCooling       : "baby cooling"
    }


    def status_kettle_description(self,status):
        if self.StatusKettle.has_key(status):
            return self.StatusKettle[status]
        else:
            return "Unknown Kettle Status " + self.number_to_code(status)


    def string_kettle_settings(self, temperature,  formula, formulatemperature, keepwarmtime):
        message = "Heat water to " + str(temperature) +  "ºC"
        if formula:
            sep = ""
            if keepwarmtime > 0:
                sep = ","
            else:
                sep = " and"
            message = message + sep + " let it cool down to " + self.temperature_to_string(formulatemperature)
        if keepwarmtime > 0:
            message = message + " and keep it warm for " + str(keepwarmtime) + " minutes"
        return message

    def is_status_command(self,status):
        return self.StatusCommand.has_key(status)


    #------------------------------------------------------
    # COFFEE STATUS INFO WRAPPER
    #------------------------------------------------------


    CoffeeStringFilter = "filter"
    CoffeeStringBeans  = "beans"

    CoffeeBeans  = True
    CoffeeFilter = False


    def grind_to_string(self,grind):
        s = self.CoffeeStringFilter
        if grind:
            s = self.CoffeeStringBeans
        return s


    def string_to_grind(self,grind):
        s = grind.lower()
        if s == self.CoffeeStringBeans:
            return True
        elif s == self.CoffeeStringFilter:
            return False
        else:
           raise SmarterErrorOld("Unknown grind ["+self.CoffeeStringBeans+"/"+self.CoffeeStringFilter+"] " + grind)


    def string_coffee_settings(self, cups, strength, grind, hotplate):
        s = ""
        if hotplate >= 5 and hotplate <= 40:
            s = " and keep hotplate warm for " + str(hotplate) + " minutes"
        t = " " + self.grind_to_string(grind) + " coffee"
        if grind:
            t = " " + self.strength_to_string(strength) + t
        return "brew " + self.cups_to_string(cups) + " of" + t + s


    def string_coffee_status(self,ready,cups,working,heating,hotPlateOn,carafe,grinderOn):
        s = ""
        if working:
            s += "working "
        if heating:
            s += "brewing " + self.cups_to_string(cups) + " cups"
        if hotPlateOn:
            s += "hotplate warming "
        if grinderOn:
            s += "grinding "
        if ready:
            s += "ready "
        if carafe:
            s+= "carafe on base"
        else:
            s+= "no carafe"
        return s


    #------------------------------------------------------
    # TYPE -> TYPE
    #------------------------------------------------------

    def watersensor_to_level(self,watersensor):
        # Fix Check value's
        #   calibrate nokettlebase:       1120     measure: kettle off: 2010 kettle empty: 2070 kettle full: 2140  (div 890 950 1020)
        #   calibrate emptykettlebase:    1070     measure: kettle off: 1975 kettle empty: 2020 kettle full: 2085  (div 905 950 1015)
        #   calibrate fullkettlebase:     1010     measure: kettle off: 1875 kettle empty: 1950 kettle full: 2015  (div 865 940 1005)
        # div = measure - base
        # need temperature in calclation...
        #   1.8l
        # is this accurate??? nope...
        # sometimes if placed on base it gives wrong levels
        if isKettle:
            waterlevel = (1.800/72) * (watersensor - self.watersensorBase - 1000)
            if waterlevel < 0:
                return 0.0
            if waterlevel > 2:
                return 1.8
            else:
                return waterlevel
        elif self.isCoffee:
            return 0


    def dbm_to_quality(self,dBm):
        # takes as input a dBm string (e.g. "-23")
        # quality = 2 * (dBm + 100)  where dBm: [-100 to -50]
        # dBm = (quality / 2) - 100  where quality: [0 to 100]
        try:
            if dBm <= -100:
                return 0
            elif dBm >= -50:
                return 100
            else:
                return 2 * (dBm + 100)
        except Exception:
            raise SmarterErrorOld("Unknown Wifi signal (dBm) strength: " + str(dBm))


    def bytes_to_human(self,size_bytes):
        
        # format a size in bytes into a 'human' file size, e.g. bytes, KB, MB, GB, TB, PB
        # Note that bytes/KB will be reported in whole numbers but MB and above will have greater precision
        # e.g. 1 byte, 43 bytes, 443 KB, 4.3 MB, 4.43 GB, etc
        
        if size_bytes == 1:
            # because I really hate unnecessary plurals
            return "1 byte"

        suffixes_table = [('bytes',0),('KB',0),('MB',1),('GB',2),('TB',2), ('PB',2)]

        num = float(size_bytes)
        for suffix, precision in suffixes_table:
            if num < 1024.0:
                break
            num /= 1024.0

        if precision == 0:
            formatted_size = "%d" % num
        else:
            formatted_size = str(round(num, ndigits=precision))

        return "%s %s" % (formatted_size, suffix)



    #------------------------------------------------------
    #
    # Protocol Information
    #
    # kinda a real, mess ;-)
    #------------------------------------------------------

    # merge and payload not finished...

    ArgCups       = 1000
    ArgStrength   = 1001
    ArgPassword   = 1002
    ArgSSID       = 1003
    ArgGrind      = 1004
    ArgTemperature= 1005
    ArgKeepWarm   = 1006
    ArgHotPlate   = 1007
    ArgFormulaTemperature= 1008
    ArgCommandStatus= 1009
    ArgFormula      = 1010
    ArgOffBase      = 1011
    ArgState        = 1012
    ArgMinute       = 1013
    ArgHour         = 1014
    ArgDay          = 1015
    ArgMonth        = 1016
    ArgSecond       = 1017
    ArgCentury      = 1020
    ArgHotPlateOn   = 1021
    ArgYear         = 1018
    ArgUnknown      = 1019
    ArgKettleStatus = 1022
    ArgVersion      = 1024
    ArgDevice       = 1025
    ArgWaterSensorLo= 1034
    ArgWaterSensorHi= 1035
    ArgIndex        = 1036
    ArgRequired     = 1037
    ArgSingleCup    = 1038
    ArgCounter      = 1027
    ArgDB           = 1032
    ArgCoffeeStatus = 1023
    ArgWaterLevel   = 1040
    ArgWaterEnough  = 1041
    ArgWaterLevelRaw= 1048
    ArgCupsCombi    = 1049
    ArgWorking      = 1042
    ArgHeater       = 1043
    ArgReady        = 1044
    ArgGrinder      = 1047
    ArgCarafe       = 1046
    ArgTimerEvent   = 1045
    ArgCupsBrew     = 1050
    ArgKeepWarmOn   = 1051
    ArgKeepWarmCombi= 1054
    ArgTemperatureCombi= 1052
    ArgHotplateCombi   = 1053
    ArgWifiFirmware    = 1055
    ArgPayloadTimer            = 1026
    ArgPayloadCoffeeHistory    = 1028
    ArgPayloadKettleHistory    = 1029
    ArgPayloadWifiScan         = 1039
    ArgWater  = 1033
    
    # NOT ADDED
    ArgSubList        = 1030
    ArgList           = 1031
    ArgValueOther = -1
    
    # ArgIndex needs combines with 0 index...???
    
    
    ArgType = {
        ResponseWirelessNetworks    : ('PROTOCOL',[ArgPayloadWifiScan],"416972476c6f772c2d38347d486f6d65576966692c2d37327d54502d4c494e4b5f3344443245362c2d39337d","List containing the wireless networks found with scanning"),
        ResponseKettleHistory       : ('PROTOCOL',[ArgPayloadKettleHistory],"020164000006001927250c1901000000000000000000000000000000000000007d\n015f000001001902260c1901000000000000000000000000000000000000007d",""),
        ResponseTimers              : ('PROTOCOL',[ArgCounter,ArgPayloadTimer],"000f0f01010114147d01030701010114137d01020501010114127d01010101010114117d",""),
        ResponseCoffeeHistory       : ('PROTOCOL',[ArgCounter,ArgPayloadCoffeeHistory],"03010000020200000b01010000000000000000000000000000000000000000007d\n010000020200012001010000000000000000000000000000000000000000007d\n010010010101000401010014000000000000000000000000000000000000007d",""),
        ResponseBase                : ('PROTOCOL',[ArgWater],"044c","Calibration base value, the base value in relation to the watersensor and temperature is unknown"),

        ArgPayloadTimer             : ('PAYLOAD',"PAYLOADTIMER",MessagePayloadTail,[]),
        ArgPayloadCoffeeHistory     : ('PAYLOAD',"PAYLOADHISTORYKETTLE",MessagePayloadTail,[]),
        ArgPayloadKettleHistory     : ('PAYLOAD',"PAYLOADHISTORYCOFFEE",MessagePayloadTail,[]),
        ArgPayloadWifiScan          : ('PAYLOAD',"PAYLOADWIFI",MessagePayloadTail,[]),
        
        ArgSubList                  : ('PAYLOAD',"TUPLE",",",[]),
        ArgList                     : ('PAYLOAD',"LIST","}",[]),


        ResponseCarafe              : ('PROTOCOL',[ArgCarafe],"00",""),
        ResponseSingleCupMode       : ('PROTOCOL',[ArgSingleCup],"01",""),
        ResponseCommandStatus       : ('PROTOCOL',[ArgCommandStatus],"04",""),
        ResponseDeviceInfo          : ('PROTOCOL',[ArgDevice,ArgVersion],"0113","Get the type of the device connected to and it's firmware. It is used for auto discovery over UDP broadcast. This fails on some routers, which don't propagate UDP broadcasts."),
        ResponseWifiFirmware        : ('PROTOCOL',[ArgWifiFirmware],"41542b474d525c6e41542076657273696f6e3a302e34302e302e302841756720203820323031352031343a34353a3538295c6e53444b2076657273696f6e3a312e332e305c6e636f6d70696c652074696d653a41756720203820323031352031373a31393a33385c6e4f4b5c6e",""),
        ResponseCoffeeSettings      : ('PROTOCOL',[ArgStrength,ArgCups,ArgGrind,ArgHotPlate],"01020005",""),
        ResponseCoffeeStatus        : ('PROTOCOL',[ArgCoffeeStatus,ArgWaterLevelRaw,ArgUnknown,ArgStrength,ArgCupsCombi],"0500000021",""),
        ResponseKettleStatus        : ('PROTOCOL',[ArgKettleStatus,ArgTemperatureCombi,ArgWater,ArgKeepWarmCombi],"14007f07d7007e",""),
        ResponseKettleSettings      : ('PROTOCOL',[ArgTemperature,ArgKeepWarmCombi,ArgFormulaTemperature],"641400","It sends a 0 between this response and the command status succes. (BUG)"),
        CommandDeviceTime           : ('PROTOCOL',[ArgSecond,ArgMinute,ArgHour,ArgUnknown,ArgDay,ArgMonth,ArgCentury,ArgYear],"1213030105021410",
                                        "Set the time on the device, is used in history and in the coffee scheduled timers messages. Unknown is Day of week index?"),
        CommandResetSettings        : ('PROTOCOL',[],"","For the kettle these are the default user settings: keepwarm 0 minutes, temperature 100ºC, formula mode off and formula temperature 75ºC. The Smarter Coffee does nothing."),
    
        CommandDeviceInfo           : ('PROTOCOL',[],"",""),
        CommandUpdate               : ('PROTOCOL',[],"","Disables wifi and creates a 'iKettle Update' wireless network and opens port 6000. A hard device reset (hold power button for 10 seconds) is sometimes required to fix this state, or just unplug the power for a moment."),
        Command69                   : ('PROTOCOL',[ArgUnknown],"00",""),  #REPEAT?

    # wifi
        CommandWifiNetwork          : ('PROTOCOL',[ArgSSID],"416363657373506f696e74",""),
        CommandWifiPassword         : ('PROTOCOL',[ArgPassword],"7040737377307264",""),
        CommandWifiJoin             : ('PROTOCOL',[],"","Sending this command without previous SSID/password commands will reset it to direct mode. Do not wait between sending the network name, the password and the join command, or else it will fail to join the wireless network. The apps actually sends: 0c7e000000000000."),
        CommandWifiScan             : ('PROTOCOL',[],"",""),
        CommandWifiLeave            : ('PROTOCOL',[],"","Leaves wireless network and reset wifi to direct mode. The app also send a firmware update command."),
        CommandWifiFirmware         : ('PROTOCOL',[],"","The firmware of the wifi module in text with control chars as new line."),

        # coffee
        CommandBrew                 : ('PROTOCOL',[ArgCups,ArgStrength,ArgHotplateCombi,ArgGrind],"04020001",""),
        CommandCoffeeStop           : ('PROTOCOL',[],"",""),
        CommandStrength             : ('PROTOCOL',[ArgStrength],"01","Sets the strength of the coffee to be brewed. Use command 37 to brew."),
        CommandCups                 : ('PROTOCOL',[ArgCups],"03","Select the number of cups to be brewed. Use command 37 to brew."),
        CommandBrewDefault          : ('PROTOCOL',[],"","Uses the settings not the default user settings."),
        CommandCoffeeSettings       : ('PROTOCOL',[ArgCups,ArgStrength,ArgGrind,ArgHotplateCombi],"03010100","Also return 00 message in an unconfigured state.??? CHECK"),
        CommandCoffeeStoreSettings  : ('PROTOCOL',[ArgStrength,ArgCups,ArgGrind,ArgHotplateCombi],"02050010",""),
        CommandGrinder              : ('PROTOCOL',[],"",""),
        CommandHotplateOn           : ('PROTOCOL',[ArgHotPlate],"05","Sets on the hotplate, you can specify how many minutes before it switch off. If no value it uses the default. "),
        CommandCoffeeHistory        : ('PROTOCOL',[],"","When called will erase this history."),
        CommandHotplateOff          : ('PROTOCOL',[],"",""),
        CommandCarafe               : ('PROTOCOL',[],"",""),
        CommandSetCarafe            : ('PROTOCOL',[ArgCarafe],"00",""),
        CommandSingleCupMode        : ('PROTOCOL',[],"",""),
        CommandSetSingleCupMode     : ('PROTOCOL',[ArgSingleCup],"01",""),
        CommandStoreTimer           : ('PROTOCOL',[ArgIndex,ArgMinute,ArgHour,ArgUnknown,ArgDay,ArgMonth,ArgCentury,ArgYear],"0401010101011411","Store time in timer schedule"),
        CommandTimers               : ('PROTOCOL',[ArgIndex],"00","Get scheduled timers. If index is not all timers it gets the first timer to go off."),
        CommandDisableTimer         : ('PROTOCOL',[ArgIndex],"00","Clear time event bit in timers schedule??? It beeps that's all then it brews, it needs investigating..."),
     
        # kettle
        CommandHeat                 : ('PROTOCOL',[ArgTemperature,ArgKeepWarmCombi],"3210",""),
        CommandKettleStop           : ('PROTOCOL',[],"",""),
        CommandHeatFormula          : ('PROTOCOL',[ArgFormulaTemperature,ArgKeepWarmCombi],"3219","Heats water to (default user temperature) and cool until the formula temperature and then keep it warm."),
        CommandHeatDefault          : ('PROTOCOL',[],"","Check arguments with wireshark"),
        Command20                   : ('PROTOCOL',[],"","This setting ignores the user setting and heats untill the tempeature is 100ºC"),
        Command22                   : ('PROTOCOL',[],"",""),
        Command23                   : ('PROTOCOL',[],"",""),
        Command30                   : ('PROTOCOL',[ArgUnknown],"",""),
        CommandKettleStoreSettings  : ('PROTOCOL',[ArgKeepWarmCombi,ArgTemperature,ArgFormula,ArgFormulaTemperature],"1f196401227e","Default user defaults message is [1f0064004b7e]. I think the correct message in v18 is without formula, since that value can take values up to 100 and nothing is returned for the 4th value. <[FORMULA]>"),
        CommandKettleHistory        : ('PROTOCOL',[],"","When called will erase this history."),
        CommandKettleSettings       : ('PROTOCOL',[],"","Also return 00 message in an unconfigured state.??? CHECK"),
        CommandStoreBase            : ('PROTOCOL',[ArgWater],"044c",""),
        CommandBase                 : ('PROTOCOL',[],"",""),
        CommandCalibrate            : ('PROTOCOL',[],"","Calibrates the base, only do this when the kettle is off base"),
 
 
        ArgWorking        : ('OPTION',"Working",[(0,"?"),(1,"?")]),
        ArgReady          : ('OPTION',"Ready",[(0,"Ready to brew"),(1,"Busy")]),
        ArgGrinder        : ('OPTION',"Grinder",[(0,"Grinder on"),(1,"Hotplate off")]),
        ArgCarafe         : ('OPTION',"Carafe",[(0,"Carafe on base"),(1,"Carafe off base or door open")]),
        ArgTimerEvent     : ('OPTION',"Timer",[(0,"Timer event tiggered"),(1,"No timer event")]),
        ArgHeater         : ('OPTION',"Heater",[(0,"Heater on"),(1,"Heater off")]),
        ArgWaterEnough    : ('OPTION',"WaterEnough",[(0,"Not enough to brew with this cups settings"),(1,"Enough water to brew  (WATERLEVEL*0.25*2)/CUPS)")]),
        ArgWaterLevel     : ('OPTION',"WaterLevel",[(CoffeeWaterEmpty,WaterLevel[CoffeeWaterEmpty]),
                                    (CoffeeWaterLow,WaterLevel[CoffeeWaterLow]),
                                    (CoffeeWaterHalf,WaterLevel[CoffeeWaterHalf]),
                                    (CoffeeWaterFull,WaterLevel[CoffeeWaterFull])]),
        ArgCoffeeStatus   : ('BIT',"CoffeeStatus",[(0,1,ArgCarafe),(1,1,ArgGrind),(2,1,ArgReady),(3,1,ArgGrinder),
                                                        (4,1,ArgHeater),(5,1,ArgHotPlateOn),(6,1,ArgWorking),(7,1,ArgTimerEvent)]),
        ArgWaterLevelRaw  : ('BIT',"WaterLevelAndEnough",[(0,4,ArgWaterLevel),(4,1,ArgWaterEnough)]),
        ArgCups           : ('NUMBER',"Cups",(1,12),"number of cups selected [1..12]"),
        ArgCupsBrew       : ('NUMBER',"CupsBrew",(1,12),"number of cups brew(ed) [1..12]"),
        ArgCupsCombi      : ('BIT',"CupsSettingAndBrew",[(0,4,ArgCups),(4,4,ArgCupsBrew)]),


        ArgWaterSensorHi     : ('NUMBER',"WaterSensorHigh",(0,16),""),
        ArgWaterSensorLo     : ('NUMBER',"WaterSensorLow",(0,255),""),
        ArgCounter           : ('NUMBER',"Counter",(0,8),""),
        ArgMinute            : ('NUMBER',"Minute",(0,60),""),
        ArgSecond            : ('NUMBER',"Second",(0,60),""),
        ArgHour              : ('NUMBER',"Hour",(0,24),""),
        ArgDay               : ('NUMBER',"Day",(1,32),""),
        ArgIndex             : ('OPTION',"Index",[
                                    (TimerAll,Timer[TimerAll]),
                                    (Timer1,Timer[Timer1]),
                                    (Timer2,Timer[Timer2]),
                                    (Timer3,Timer[Timer3]),
                                    (Timer4,Timer[Timer4])
                                ]
                              ),
        ArgMonth             : ('NUMBER',"Month",(1,12),""),
        ArgYear              : ('NUMBER',"Year",(0,99),""),
        ArgCentury           : ('NUMBER',"Century",(19,21),""),
        ArgUnknown           : ('NUMBER',"Unknown",(0,255),"Unknown number"),
        ArgVersion           : ('OPTION',"Version",[(18,"iKettle 2.0"),
                                    (20,DeviceStringCoffee),
                                    (22,DeviceStringCoffee),
                                    (19,DeviceStringKettle)
                                    ]
                              ),
        ArgDevice            : ('OPTION',"Device",[(DeviceCoffee,DeviceStringCoffee),(DeviceKettle,DeviceStringKettle)]),
        ArgKettleStatus      : ('OPTION',"KettleStatus",[
                                (KettleReady, StatusKettle[KettleReady]),
                                (KettleHeating, StatusKettle[KettleHeating]),
                                (KettleKeepWarm, StatusKettle[KettleKeepWarm]),
                                (KettleCycleFinished, StatusKettle[KettleCycleFinished]),
                                (KettleBabyCooling, StatusKettle[KettleBabyCooling])
                            ]),
        ArgTemperature        : ('NUMBER',"Temperature",(0,100),"temperature in celcius [0ºC..100ºC]"),
        ArgFormulaTemperature : ('NUMBER',"FormulaTemperature",(0,100),"formula temperature in celcius [0ºC..100ºC]"),
        ArgKeepWarm           : ('NUMBER',"Keepwarm",(5,35),"kettle keep warm time in minutes [5..35]"),
        ArgKeepWarmOn         : ('OPTION',"KeepwarmOn",[(0,"Keepwarm off"),(1,"Keepwarm on")]),

        ArgHotPlate           : ('NUMBER',"Hotplate",(5,30),"hotplate keep warm time in minutes [5..30]"),
        ArgFormula            : ('OPTION',"Formula",[(0,"Disabled"),(1,"Enabled")]),
        ArgOffBase            : ('OPTION',"Base",[(0,"Kettle on base"),(MessageOffBase,"Kettle off base")]),
        ArgRequired           : ('OPTION',"Required",[(0,"Carafe Required"),(1,"Can brew without carafe")]),
        ArgSingleCup          : ('OPTION',"SingleCup",[(0,"Single cup mode off"),(1,"Single cup mode on")]),

        ArgHotPlateOn         : ('OPTION',"HotplateOn",[(0,"Hotplate on"),(1,"Hotplate off")]),

        ArgState              : ('OPTION',"State",[(0,"Failed"),(1,"Succes")]),
        ArgStrength       : ('OPTION',"Strength",[(CoffeeWeak,CoffeeStringWeak),
                                    (CoffeeMedium,CoffeeStringMedium),
                                    (CoffeeStrong,CoffeeStringStrong)]
                            ),
        ArgPassword       : ('TEXT',"Password","wireless network password"),
        ArgDB             : ('TEXT',"DB","in dBm"),
        ArgWifiFirmware   : ('TEXT',"WifiFirmware","wifi firmware string"),
        ArgSSID           : ('TEXT',"SSID","wireless network name"),
        ArgGrind          : ('OPTION',"Grind",[(CoffeeFilter,CoffeeStringFilter),(CoffeeBeans,CoffeeStringBeans)]),
       
       
        ArgKeepWarmCombi    : ('RANGE',"KeepWarmMerged",ArgKeepWarm,ArgKeepWarmOn,0),
        ArgHotplateCombi    : ('RANGE',"HotplateMerged",ArgHotPlate,ArgHotPlateOn,0),
        ArgTemperatureCombi : ('RANGE',"TemperatureMerged",ArgTemperature,ArgOffBase,MessageOffBase),
        ArgWater            : ('INT',"WaterSensor",ArgWaterSensorHi,ArgWaterSensorLo),
       
        ArgCommandStatus  : ('OPTION',"CommandStatus",[
                            (StatusSucces,StatusCommand[StatusSucces]),
                            (StatusBusy,StatusCommand[StatusBusy]),
                            (StatusNoCarafe,StatusCommand[StatusNoCarafe]),
                            (StatusNoWater,StatusCommand[StatusNoWater]),
                            (StatusFailed,StatusCommand[StatusFailed]),
                            (StatusNoCarafeUnknown,StatusCommand[StatusNoCarafeUnknown]),
                            (StatusNoWaterUnknown,StatusCommand[StatusNoWaterUnknown]),
                            (StatusNoWaterAborted,StatusCommand[StatusNoWaterAborted]),
                            (StatusInvalidTimer,StatusCommand[StatusInvalidTimer]),
                            (StatusInvalid,StatusCommand[StatusInvalid])

                            ])
    }
    

    def message_example(self,id):
        return self.number_to_code(id) + self.ArgType[id][2] + self.number_to_code(self.MessageTail)

    def message_notes(self,id):
        return self.ArgType[id][3]

    # nice printab;e protocol info...
    

    def argument_messages(self,id):
        d = []
        for b in self.ArgType:
            if self.ArgType[b][0] == 'PROTOCOL':
                print "YEAH"
                if id in self.ArgType[b][1]:
                    print "DSS"
                    d += [b]
        return d

    
    def message_arguments(self,id):
        a = list()
        for b in self.ArgType[id][1]:
            a += [(b,self.ArgType[b][1].upper())]
        return a
        
        
    def message_protocol_arguments(self):
        a = list()
        for b in self.ArgType:
            if self.ArgType[b][0] == "PROTOCOL":
                a += self.ArgType[b][1]
    
        z = list()
        for x in a:
            
            z += [(x,self.ArgType[x][1])]
        z = set(z)
        a = list(z)
        z = sorted(a, key=lambda tup: tup[1])

        return [item[0] for item in z]

    # nice printab;e protocol info...

    def string_int(self,argument):
        s = ""
        s += "    <" + self.ArgType[argument[2]][1].upper() + ">" + " + "
        s += "<" + self.ArgType[argument[3]][1].upper() + ">" + "\n"
        s += self.string_argument(argument[2])
        s +=  self.string_argument(argument[3])
        return s


    def string_option(self,argument):
        s = ""
        for (x,y) in argument[2]:
                s += "  " + self.number_to_code(x).rjust(4, ' ') + "        " + y + "\n"
        return s + ""
    
    def string_combined(self,argument):
        s = ""
        for (x,y,z) in argument[2]:
            if y == 1:
                range = " bit " + str(x)
            if y > 1:
                range = "bits " + str(x) + ".." + str(x+y-1)
            s += ("    " + range).ljust(13, ' ') + " “" + self.ArgType[z][1].upper() + "”\n"
            # herer
        for (x,y,z) in argument[2]:
            s += self.string_argument(z,True)
        return s + ""
            

    def string_range(self,argument):
        s = ""
        s += ("    Merged byte <" + self.ArgType[argument[2]][1].upper() + ">").ljust(15, ' ')  + "<"
        s += self.ArgType[argument[3]][1].upper() + ">"  + "\n"
        s += self.string_argument(argument[2])
        s += self.string_argument(argument[3])
        return s + ""
 
    def string_text(self,argument):
            return "    TEXT      " + argument[2] + "\n"

    def string_protocol(self,argument,id):
        
        s = ""
        s += "\n"
        s += "  " + self.message_is_type(id) + " Message " + self.number_to_code(id) + ": " + self.message_description(id) + "\n"
        s +=  "  ─────────────────────────────────────────────────────────────────────────\n"
        d = ""
        if self.message_is_known(id):
            for i, iid in enumerate(self.message_connection(id)):
                d = d + "[" + self.number_to_code(iid) + "," + self.message_description(iid) + "] "
            if self.message_connection(id):
                if self.message_is_response(id):
                    s += "  Response to command messages: " + d + "\n"
                elif self.message_is_command(id):
                    s += "  Response messages: " + d + "\n"
            s += "\n  " + self.message_kettle_supported(id) + " " + self.DeviceStringKettle +  " " + self.message_coffee_supported(id) + " " + self.DeviceStringCoffee + "\n"
            if self.message_is_response(id):
                length = self.message_response_length(id)
                if length > 0:
                    s += "\n  Message size: " + str(length) + " bytes\n"
            
        if argument[3] != "":
            s += "\n  " + argument[3] + "\n"
        
        if len(argument[1]) != 0:
            
            s += "\n\n  Arguments: "
            
            for a in argument[1]:
                s += "<" + self.ArgType[a][1].upper() + ">"
            s += "\n"
            for a in argument[1]:
                s += "\n" + self.string_argument(a)


    
        s += "\n\n  Example: [" + self.number_to_code(id) + argument[2] + self.number_to_code(self.MessageTail) + "]"
        return s + "\n\n"

    def string_number(self,argument):
        return "    " + self.number_to_code(argument[2][0]) + ".." + self.number_to_code(argument[2][1]) + "    " + argument[3] + "\n"

    
    def string_argument(self,argument,bit=False):
        if self.ArgType.has_key(argument):
            s = ""
            a = self.ArgType[argument]
            if a[0] == 'PROTOCOL':
                return self.string_protocol(a,argument)
        
            if bit:
                s += "\n  “" + a[1].upper() + "”\n"
            else:
                s += "\n  <" + a[1].upper() + ">\n"
            if a[0] == 'OPTION':
                s += ""
                s += self.string_option(a)
            elif a[0] == 'TEXT':
                s += self.string_text(a)
            elif a[0] == 'NUMBER':
                s += self.string_number(a)
            elif a[0] == 'BIT':
                s += self.string_combined(a)
            elif a[0] == 'INT':
                s += self.string_int(a)
            elif a[0] == 'RANGE':
                s += self.string_range(a)
            else:
                print "AAAAARRGGHHH"
            
        else:
            s = "No information on: " + self.number_to_code(argument)
        return s + ""

    def all(self):
        s = ""
        for id in range(0,255):
            if self.message_is_known(id):
                print str(id)
                s += self.string_argument(id)
        return s


    def message(self,id):
        return self.string_argument(id)


    def messages(self,coffee=True,kettle=True):
        s = ""
        if coffee:

            s +=  "\n\n    ID Coffee Machine Command Message\n"
            s +=  "    ___________________________________________\n"
            for id in range(0,255):
                if Smarter.message_is_command(id) and Smarter.message_coffee(id): # and not Smarter.message_kettle(id):
                    s +=  "    " + Smarter.number_to_code(id) + " " + Smarter.message_description(id) + "\n"

            s +=  "\n    ID Coffee Machine Response Message\n"
            s +=  "    ___________________________________________\n"
            for id in range(0,255):
                if Smarter.message_is_response(id) and Smarter.message_coffee(id): # and not Smarter.message_kettle(id):
                    s += "    " + Smarter.number_to_code(id) + " " + Smarter.message_description(id) + "\n"

            s += "\n    ID Coffee Machine Status Message\n"
            s += "    ___________________________________________\n"
            for id in range(0,255):
                if Smarter.message_is_status(id) and Smarter.message_coffee(id):
                    s +=  "    " + Smarter.number_to_code(id) + " " + Smarter.message_description(id) + "\n"

        if kettle:

            s += "\n\n    ID Kettle Command Message\n"
            s += "    ___________________________________________\n"
            for id in range(0,255):
                if Smarter.message_is_command(id) and Smarter.message_kettle(id):
                    s += "    " + Smarter.number_to_code(id) + " " + Smarter.message_description(id) + "\n"

            s += "\n    ID Kettle Response Message\n"
            s += "    ___________________________________________\n"
            for id in range(0,255):
                if Smarter.message_is_response(id) and Smarter.message_kettle(id):
                    s +=  "    " + Smarter.number_to_code(id) + " " + Smarter.message_description(id) + "\n"


            s +=  "\n    ID Kettle Status Message\n"
            s +=  "    ___________________________________________\n"
            for id in range(0,255):
                if Smarter.message_is_status(id) and Smarter.message_kettle(id):
                    s +=  "    " + Smarter.number_to_code(id) + " " + Smarter.message_description(id) + "\n"

        return s + "\n"

    def protocol(self):
        return self.structure() + self.messages() + self.all() + self.notes()

    def structure(self):
        return """
       
       
  Smarter iKettle 2.0 & Smarter Coffee  Protocol
  _____________________________________________

    Smarter uses a binary message protocol

    Messages use the syntax:

     <ID>[ARGUMENTS]<TAIL>

    Payloads use the syntax
    
      ([ARGUMENTS]<PAYLOADTAIL>){0..*}

    Arguments use this syntax:

      <ARGUMENT>     is a single mandatory byte
      <[ARGUMENT]>   is a single optional byte
      <ARGUMENT>{x}  is mandatory, between 1 and x bytes
      ''             is a single bit
      
    The tail is always 7e or ~ in ASCII, everything else are ASCII literals
    The tail payload is always 7d or } in ASCII, everything else are ASCII literals
    
    There are some value's like the watersensor that can contains the tail
    so check the length of the response message!
    
               """
    
    def notes(self):
        return """


  Smarter iKettle 2.0 & Smarter Coffee  Notes
  __________________________________________
    
  WaterSensor Calibration:

    If the kettle is on the base during calibration, the numbers change to be higher,
    but the differences between levels seem the same. This means that the water level
    detection is probably weight based and that calibration is done at the base,
    which then remembers the weight for \'off base\'. To detect an empty kettle,
    the connecting device must account for the weight of the kettle.
    
    (yeah, not! the watersensor becomes higher if the temperature becomes higher...)


  Wireless Network:

    If the device (coffee?) is configured to access an wifi access point which is not available
    It will try to connect to it every so minutes. If it tries to connect it beeps three
    times the wifi access point of the device will remain active but unreachable,
    if it fails to access the access point it beeps once, and it opens up its own default
    open unencrypted wifi access point.access

    If connected to the kettle tcp 192.168.4.1:2081 is the default connection.

    The iKettle 2.0 creates an access point with the name iKettle 2.0:c0 where c0 is part
    of the mac address of the kettle. When connected directly to the kettle its connection is very flacky.


  Device Detection:
  
    To detect a device broadcast a device info command (message 64) on UDP. It will reply
    if the router permits it with a device info response (message 65) and being UDP 
    with its IP address!
    
    
  Capturing the protocol using WireShark:

     OSX:  (Home Network Only)
           Step 1: Download wireshark (https://www.wireshark.org/) for mac and install it.
           Step 2: Setup your kettle or coffee machine to use your home network.
           Step 3: Connect you mac to your network NOT using the build in wifi adapter.
                   Use either a cable (ethernet recommended) or a second wifi adapter.
           Step 4: Enable and setup internet sharing in system preferences, sharing.
           Step 5: Connect with your phone to the internet sharing wireless access point.
           Step 6: Run wiresharp it and select your build in wifi adapter and start the capture.
           Step 7: Look for connection with messages ending in 7e

    iOS & OSX: (Home network & Direct mode)
           Step 1: Connect your iOS device to your Mac via USB.
           Step 2: Get the <udid> for the connected device from iTunes (click on the serial).
           Step 3: Open terminal in your Mac and run the following commands, which creates a virtual network
                   adapter mirroring the iOS network, which we can dump and inspect:
           Step 4: rvictl -s <udid>
           Step 5: tcpdump -i rvi0 -w ~/Desktop/output.pcap
           Step 6: Connect to kettle's wifi network (or your home network if already setup) on the iOS device.
           Step 7: Run setup for smarter device setup, or any commands
           Step 8: When done or the device setup disconnected to switch to your home network, disconnect with ctrl-c
           Step 9: rvictl -x <udid>
           Step A: Download wireshark (https://www.wireshark.org/) for mac and install it.
           Stap B: Open ~/Desktop/output.pcap with Wireshark
           Step C: Look for connection with messages ending in 7e
 

  Security:

    iKettle 2.0:
         *  It will heat up empty, making the lights bulbs to flikker.
         *  You can easily knock out it's connection to the wireless network,
            if it fails to connect it creates an default open unencrypted wifi access point 
            (check!, could be that wifi was not connecting, then this is rubbish ;-).

            Attack Vectors
            1. Repeat sending heat to 100ºC temperature commands, if we're lucky
               there is no water and it will heat up empty, if not it will take a while.
               plus the kettle will get warmer and warmer. If you do not expect that when touching.
            2. Alternating heat and stop commands.
            3. (Check) Wait until the owner of the kettle log in on the kettle, since its an
               open access point and the password are send in the open you can read it.
            4. Repeat scan for wifi commands, it will crash the wifi esp module.


  Coffee Brewing:

    Between setting the number of cups, the strength of the coffee and start of brewing
    atleast 500ms is recommended.
    

  Water Heating:
  
    From smarter website the temperature that can be set is between 20 and 100. We still need to read lower 
    values for cold water in the kettle
     
 
               """

    def license(self):
        return """
Copyright (c) 2016, Tristan Crispijn
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. You may not use source, binary forms or derivative work, with or without modification, for commercial purposes. 

4. Written consent of the original author with his/her signature on paper.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. YOU AGREE TO NOT USE THIS SOFTWARE IN ANY WAY. SMARTER EMPLOYEES OR SMARTER AFFILIATED PEOPLE ARE NOT ALLOWED TO USE THIS SOFTWARE OR DERIVATIVE WORK. YOU AGREE THAT THE SOFTWARE CAN MONITOR THE USAGE OF THE SOFTWARE ITSELF AND OR THE DEVICES ATTACHED TO THE SOFTWARE, AND SEND IT BACK TO A MONITOR SERVER FOR BETTER SUPPORT. ENJOY!
               """

Smarter = SmarterProtocol()
