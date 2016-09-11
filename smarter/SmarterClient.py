# -*- coding: utf8 -*-

import socket
import os
import sys
import string
import random
import time
import datetime
import logging
import logging.handlers

try:
    import win_inet_pton
except Exception:
    pass
    
from ConfigParser import SafeConfigParser

import traceback
import threading

from SmarterProtocol import *

#------------------------------------------------------
# SMARTER CLIENT INTERFACE
#
# Python interface to iKettle 2.0 & Smarter Coffee Devices
#
# https://github.com/Tristan79/iBrew
#
# Copyright © 2016 Tristan (@monkeycat.nl)
#
# Out of order! (rev 7)
#------------------------------------------------------


def threadsafe_function(fn):
    """decorator making sure that the decorated function is thread safe"""
    lock = threading.Lock()
    def new(*args, **kwargs):
        
        lock.acquire()
        try:
            r = fn(*args, **kwargs)
        except Exception as e:
            s = traceback.format_exc()
            logging.debug(s)
            logging.debug(e)
            raise e
        finally:
            lock.release()
        return r
    return new

#------------------------------------------------------
# CLIENT INTERFACE CLASS
#------------------------------------------------------

class SmarterClient:
    
    def init(self):
    
    
        # network
        self.port                       = Smarter.Port
        
        # device
        self.commandStatus              = Smarter.StatusSucces
        self.sendMessage                = None
        self.responseMessage            = None
        self.readMessage                = None
        self.statusMessage              = None
        self.historySuccess             = 0
        
        # device info
        self.heaterOn                   = False
        self.countHeater                = 0

        
        # unknown status byte
        self.unknown                    = 0
    
        self.isKettle                   = False
        self.isCoffee                   = False
 
        # kettle
        self.kettleStatus               = Smarter.KettleReady
        
        self.onBase                     = False
        
        self.countKettleRemoved         = 0
        
        self.keepWarmOn                 = False
        self.countKeepWarm              = 0
        
        self.temperature                = 0
        self.temperatureStable          = 0
        
        self.defaultTemperature         = 100
        self.defaultKeepWarmTime        = 0
        self.defaultFormula             = False
        self.defaultFormulaTemperature  = 75
        
        # watersensor
        self.waterSensorBase            = 0
        self.waterSensor                = 0
        self.waterSensorStable          = 0
        
        # coffee
        self.coffeeStatus               = 0 # unknown

        self.waterLevel                 = 0

        self.cups                       = 1
        self.strength                   = Smarter.CoffeeMedium
        self.hotPlate                   = 0
        self.grind                      = False

        self.defaultCups                = 1
        self.defaultStrength            = Smarter.CoffeeMedium
        self.defaultGrind               = False
        self.defaultHotPlate            = 0

        self.singlecup                  = False
        self.carafeMode                 = False

        self.cupsBrew                   = 0
        self.waterEnough                = False
        self.carafe                     = True
        self.timerEvent                 = False
        self.ready                      = True
        self.hotPlateOn                 = False
        self.grinderOn                  = False
        self.working                    = False
        
        self.countCarafeRemoved         = 0
        self.countCupsBrew              = 0
        self.countGrinderOn             = 0
        self.countHotPlateOn            = 0
        
        # Wifi
        self.Wifi                       = []
        self.WifiFirmware               = "None"
        isDirect                        = False

        self.writeLock                  = threading.Lock()
        self.socketLock                 = threading.Lock()
    

        
        # session
        self.sendCount                  = 0
        self.readCount                  = 0
        self.sendBytesCount             = 0
        self.readBytesCount             = 0

        # already written to total from session
        self.deltaSendCount             = 0
        self.deltaReadCount             = 0
        self.deltaReadBytesCount        = 0
        self.deltaSendBytesCount        = 0


        self.deltaCountCarafeRemoved         = 0
        self.deltaCountCupsBrew              = 0
        self.deltaCountGrinderOn             = 0
        self.deltaCountHotPlateOn            = 0
        self.deltaCountKettleRemoved         = 0
        self.deltaCountHeater                = 0
        self.deltaCountKeepWarm              = 0
        self.deltaSessionCount               = 0


    def __init__(self):
        # total for device
        self.totalSendCount             = 0
        self.totalReadCount             = 0
        self.totalReadBytesCount        = 0
        self.totalSendBytesCount        = 0
        
        
        self.totalCountCarafeRemoved         = 0
        self.totalCountCupsBrew              = 0
        self.totalCountGrinderOn             = 0
        self.totalCountHotPlateOn            = 0
        self.totalCountKettleRemoved         = 0
        self.totalCountHeater                = 0
        self.totalCountKeepWarm              = 0
        self.totalSessionCount               = 0
        
        
        
        self.host                       = Smarter.DirectHost
        self.dump_status                = True
        self.dump                       = False
        #set this to try is you want to connect send receive and don't care about the new status or other messages the about the out come, its disconnect afterwards....
        self.fast                       = False
        #set this to try is you want to connect send and really do not care about the about the out come, its disconnect afterwards....
        self.shout                      = False
        
        self.device                     = "None"
        self.deviceId                   = 0
        self.version                    = 0
        self.sessionCount               = 0
        self.commandCount               = dict()
        self.responseCount              = dict()
        
        # Threading info
        self.writeLock                  = threading.Lock()
        self.socketLock                 = threading.Lock()
        self.connected                  = False
        self.monitor                    = None
        self.socket                     = None
        self.run                        = False
        
        self.init()
        self.settingsPath               = "devices/"


    def __del__(self):
        self.disconnect()


    #------------------------------------------------------
    # CONNECTION
    #------------------------------------------------------


    def init_default(self):
        self.fast = False
        self.shout = False
        self.device_info()
        if self.isKettle:
            self.kettle_settings()
            self.kettle_calibrate_base()
        elif self.isCoffee:
            self.coffee_settings()
            self.hotPlate = self.defaultHotPlate
            self.coffee_single_cup_mode()
            self.coffee_carafe()
        self.wifi_firmware()


    def monitor_device(self):
        if self.dump:
            logging.info("[" + self.host + "] Monitor Running")
        
        previousResponse = ""
        previousWaterSensor = self.waterSensor
        
        prevPreviousTemperature = self.temperature
        previousTemperature = self.temperature
        previousAverage = self.temperature
        
        self.waterSensorStable  = self.waterSensor
        self.temperatureStable  = self.temperature
        
        monitorCount = 0
   
        timeout = 60
        self.run = True
        while self.run:
                try:
                    self.writeLock.acquire()
                except Exception, e:
                    s = traceback.format_exc()
                    logging.debug(s)
                    logging.debug(e)
                    logging.error("[" + self.host + "] ERROR")
                    self.disconnect()
                    #print(traceback.format_exc())
 
                    break
                    raise SmarterErrorOld("Monitor Error")
                try:
                    if not self.connected:
                        #print(traceback.format_exc())
                        break
                    
                    response = self.read()
                    monitorCount += 1
                    if previousResponse != response:
                        previousResponse = response
                        # call monitor function
                        # ...else got one! yeah! print it!
  
                except Exception, e:
                    s = traceback.format_exc()
                    logging.debug(s)
                    logging.debug(e)
                    logging.error("[" + self.host + "] ERROR")

                    if self.writeLock.locked():
                        self.writeLock.release()
                    self.disconnect()
                    break
                    raise SmarterErrorOld("Monitor Error")
                
                self.writeLock.release()
                
                dump = self.dump
                
                if self.dump_status:
                    self.dump = True;
                else:
                    self.dump = False;

                try:
                    if monitorCount % timeout == timeout - 9:
                        if self.isKettle:   self.kettle_calibrate_base()
                        if self.isCoffee:   self.coffee_carafe()
 
                    if monitorCount % timeout == timeout - 19:
                        if self.isCoffee:   self.coffee_single_cup_mode()
 
                    if monitorCount % timeout == timeout - 29:
                        self.device_settings()
 
                    if monitorCount % timeout == timeout - 39:
                        self.write_stats()
                    
                    if monitorCount % timeout == timeout - 49:
                        pass #self.coffee_timers()
                    
                    if monitorCount % timeout == timeout - 50:
                        pass #self.device_history()
                        
                except Exception, e:
                    s = traceback.format_exc()
                    logging.debug(s)
                    logging.debug(e)
                    logging.error("[" + self.host + "] ERROR")
                    self.disconnect()
                    self.dump = dump
                    break
                    raise SmarterErrorOld("Monitor Error")


                self.dump = dump


                if previousWaterSensor - 3 > self.waterSensor or previousWaterSensor + 3 < self.waterSensor:
                    self.waterSensorStable = self.waterSensor
                    previousWaterSensor = self.waterSensor
                
                average = int(round(float((float(previousTemperature) + float(prevPreviousTemperature) + float(self.temperature))/3),0))

                if previousAverage != average:
                    self.temperatureStable = average
                    previousAverage = average

                prevPreviousTemperature = previousTemperature
                previousTemperature = self.temperature
        if self.dump:
            logging.info("[" + self.host + "] Monitor Stopped")
 
     #------------------------------------------------------
    # TRANSMISSION
    #------------------------------------------------------


    # MESSAGE READ
    def read_message(self):
        try:
            message = ""
            raw = self.socket.recv(1)
            id = Smarter.raw_to_number(raw)
            # debug
            #print "[" + Smarter.number_to_code(id) + "]",
            minlength = Smarter.message_response_length(id)

            i = 1
            while raw != Smarter.number_to_raw(Smarter.MessageTail) or (minlength > 0 and raw == Smarter.number_to_raw(Smarter.MessageTail) and i < minlength):
                message += raw
                raw = self.socket.recv(1)
                # debug
                #print "[" + Smarter.raw_to_code(raw) + "]",
                i += 1
            message += raw
            self.readMessage = message
            
            self.readCount += 1
            self.readBytesCount += i
            if id in self.responseCount:
                self.responseCount[id] += 1
            else:
                self.responseCount[id] = 1
 
            return message

        except socket.error, msg:
            raise SmarterErrorOld("Could not read message") # (" + msg + ")")


    # MESSAGE READ PROTOCOL
    def read(self):
        if not self.connected:
            raise SmarterErrorOld("Could not read message not connected")
   
    
        try:
            self.socketLock.acquire()
        except Exception:
            raise SmarterErrorOld("Could not read message")
    
        if self.connected:
     
            message = self.read_message()
            id = Smarter.raw_to_number(message[0])
            
            if Smarter.message_kettle(id) and not Smarter.message_coffee(id):
                self.switch_kettle_device()
            elif Smarter.message_coffee(id) and not Smarter.message_kettle(id):
                self.switch_coffee_device()
            try:
                if   id == Smarter.ResponseKettleStatus:    self.decode_ResponseKettleStatus(message)
                elif id == Smarter.ResponseCoffeeStatus:    self.decode_ResponseCoffeeStatus(message)
                elif id == Smarter.ResponseCommandStatus:   self.decode_ResponseCommandStatus(message)
                elif id == Smarter.ResponseBase:            self.decode_ResponseBase(message)
                elif id == Smarter.ResponseTimers:          self.decode_ResponseTimers(message)
                elif id == Smarter.ResponseCarafe:          self.decode_ResponseCarafe(message)
                elif id == Smarter.ResponseSingleCupMode:   self.decode_ResponseSingleCupMode(message)
                elif id == Smarter.ResponseKettleHistory:   self.decode_ResponseKettleHistory(message)
                elif id == Smarter.ResponseCoffeeHistory:   self.decode_ResponseCoffeeHistory(message)
                elif id == Smarter.ResponseKettleSettings:  self.decode_ResponseKettleSettings(message)
                elif id == Smarter.ResponseCoffeeSettings:  self.decode_ResponseCoffeeSettings(message)
                elif id == Smarter.ResponseDeviceInfo:      self.decode_ResponseDeviceInfo(message)
                elif id == Smarter.ResponseWifiFirmware:    self.decode_ResponseWifiFirmware(message)
                elif id == Smarter.ResponseWirelessNetworks:self.decode_ResponseWirelessNetworks(message)
            except Exception:
                s = traceback.format_exc()
                logging.debug(s)
                raise SmarterErrorOld("Could not read message disconnected")
 
            if self.unknown != 0:
                print "***********************"
                print "*                     *"
                print "* Unknown byte is set *"
                print "*                     *"
                print "***********************"
                print
                print Smarter.number_to_code(self.unknown) + "-" + str(self.unknown)
            
            if self.dump:
                if self.dump_status:
                    self.print_message_read(message)
                else:
                    #fix
                    if id != Smarter.ResponseCoffeeStatus and id != Smarter.ResponseKettleStatus:
                        self.print_message_read(message)
        
            self.socketLock.release()
            return message
        else:
            self.socketLock.release()
            raise SmarterErrorOld("Could not read message disconnected")


    # MESSAGE SEND
    def send_message(self,message):
        if len(message) == 0:
            raise SmarterErrorOld("Cannot send an empty message")
    
        try:
            self.socket.send(message)
        except socket.error, msg:
            raise SmarterErrorOld("Could not send message")

        self.sendBytesCount += len(message)
    
        id = Smarter.raw_to_number(message[0])
        self.sendCount += 1
        if id in self.commandCount:
            self.commandCount[id] += 1
        else:
            self.commandCount[id] = 1

        self.sendMessage = message
        if self.dump:
            self.print_message_send(message)




    # MESSAGE SEND PROTOCOL

    def send_command(self,id,arguments=""):
        x = Smarter.message_connection(id)
        if len(x) != 0:
            # that whole fast thing should be fixed.
            if x[0] != Smarter.ResponseCommandStatus:
                self.fast = False
        else:
            self.fast = False
        self.send(Smarter.number_to_raw(id) + arguments + Smarter.number_to_raw(Smarter.MessageTail))


    def send(self,message):
        if not self.connected:
            raise SmarterErrorOld("Could not write message not connected")
        
        try:
            self.writeLock.acquire()
        except Exception:
            raise SmarterErrorOld("Could not write message")

        try:
            self.socketLock.acquire()
        except Exception:
            raise SmarterErrorOld("Could not write message")

        if self.connected:
            try:
                self.send_message(message)
            except Exception:
                self.socketLock.release()
                self.writeLock.release()
                self.disconnect()
                raise SmarterErrorOld("Could not send message")
            
            self.socketLock.release()
        
            if self.shout:
                self.writeLock.release()
                return

            try:
                self.read()
            except Exception:
                self.disconnect()
                print(traceback.format_exc())
                raise SmarterErrorOld("Could not write message (no response)")
            
            data = Smarter.raw_to_number(self.readMessage[0])
            
            while (data == Smarter.ResponseKettleStatus) or (data == Smarter.ResponseCoffeeStatus):
                try:
                    self.read()
                except Exception:
                    self.writeLock.release()
                    self.disconnect()
                    raise SmarterErrorOld("Could not write message (no response)")
                
                data = Smarter.raw_to_number(self.readMessage[0])
             
            self.responseMessage = self.readMessage

            if self.fast:
                self.writeLock.release()
                return
            
            # Smarter.message_connection(raw_to_number(self.readMessage[0])[0]
            try:
                self.read()
            except Exception:
                self.disconnect()
                self.writeLock.release()
                raise SmarterErrorOld("Could not write message (no response)")
            

            data = Smarter.raw_to_number(self.readMessage[0])
            while (data != Smarter.ResponseKettleStatus) and (data != Smarter.ResponseCoffeeStatus):
                try:
                    self.read()
                except Exception:
                    self.disconnect()
                    self.writeLock.release()
                    raise SmarterErrorOld("Could not write message (no response)")
                data = Smarter.raw_to_number(self.readMessage[0])

        else:
            self.writeLock.release()
            raise SmarterErrorOld("Could not read message disconnected")
        self.writeLock.release()
         
    @threadsafe_function
    def connect(self):
        if self.dump:
            print "[" + self.host +  ":" + '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + "] Connecting device"
        self.init()
        self.write_stats()
        
        if self.host == "":
            self.host = Smarter.DirectHost

        if self.host == Smarter.DirectHost:
            if platform.system() == "Darwin" or platform.system() == "Linux":
                # yeah, it only accept one wifi...

                # loop over interfaces.. interfaces()
                from wireless import Wireless
                wireless = Wireless()
                wirelessname = wireless.current()
                if wirelessname is not None:
                    if (wirelessname[0:14] == Smarter.DeviceStringCoffee or wirelessname[0:11] == Smarter.DeviceStringKettle) and self.host == Smarter.DirectHost:
                        self.isDirect = True
                    else:
                        self.isDirect = False
                else:
                    self.isDirect = False
            elif platform.system() == "Windows":
                self.isDirect = False
                # Netsh WLAN show interfaces grep it contains "iKettle 2.0" or "Smarter...
            else:
                self.isDirect = False
        else:
            self.isDirect = False
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(12)
            self.socket.connect((self.host, self.port))
            self.connected = True
            self.sessionCount = 1
        except socket.error, msg:
            s = traceback.format_exc()
            logging.debug(s)
            logging(msg)
            logging.error("[" + self.host + "] Could not connect to + " + self.host)
            raise SmarterErrorOld("Could not connect to + " + self.host)


        if not self.fast:
            import threading
            try:
                self.monitor = threading.Thread(target=self.monitor_device)
                self.monitor.start()
            except Exception, e:
                s = traceback.format_exc()
                logging.debug(s)
                loggins.debug(e)
                logging.error("[" + self.host + "] Could not start monitor")
                raise SmarterErrorOld("Could not start monitor")


    @threadsafe_function
    def write_stats(self):
        
        
        
        section = "stats"
        if self.isKettle:
            section += ".kettle"
        elif self.isCoffee:
            section += ".coffee"
        else:
            return
        config = SafeConfigParser()
        
        
        if not os.path.exists(self.settingsPath):
                os.makedirs(self.settingsPath)
        config.read(self.settingsPath+self.host+'.conf')
        
        try:
            config.add_section(section)
        except Exception:
            pass

        try:
            self.totalSendCount = int(config.get(section, 'send')) + self.sendCount - self.deltaSendCount
            self.deltaSendCount += self.sendCount - self.deltaSendCount
            config.set(section, 'send', str(self.totalSendCount))
        except Exception:
            config.set(section, 'send', str(self.sendCount))
        
        try:
            self.totalReadCount = int(config.get(section, 'read')) + self.readCount - self.deltaReadCount
            self.deltaReadCount += self.readCount - self.deltaReadCount
            config.set(section, 'read', str(self.totalReadCount))
        except Exception:
            config.set(section, 'read', str(self.readCount))

        try:
            self.totalReadBytesCount = int(config.get(section, 'readbytes')) + self.readBytesCount - self.deltaReadBytesCount
            self.deltaReadBytesCount += self.readBytesCount - self.deltaReadBytesCount
            config.set(section, 'readbytes', str(self.totalReadBytesCount))
        except Exception:
            config.set(section, 'readbytes', str(self.readBytesCount))

        try:
            self.totalSendBytesCount = int(config.get(section, 'sendbytes')) + self.sendBytesCount - self.deltaSendBytesCount
            self.deltaSendBytesCount += self.sendBytesCount - self.deltaSendBytesCount
            config.set(section, 'sendbytes', str(self.totalSendBytesCount))
        except Exception:
            config.set(section, 'sendbytes', str(self.sendBytesCount))



        try:
            self.totalCountHeater = int(config.get(section, 'heater')) + self.countHeater - self.deltaCountHeater
            self.deltaCountHeater += self.countHeater - self.deltaCountHeater
            config.set(section, 'heater', str(self.totalCountHeater))
        except Exception:
            config.set(section, 'heater', str(self.countHeater))


        if self.isKettle:
            try:
                self.totalCountKettleRemoved = int(config.get(section, 'kettleremoved')) + self.countKettleRemoved - self.deltaCountKettleRemoved
                self.deltaCountKettleRemoved += self.countKettleRemoved - self.deltaCountKettleRemoved
                config.set(section, 'kettleremoved', str(self.totalCountKettleRemoved))
            except Exception:
                config.set(section, 'kettleremoved', str(self.countKettleRemoved))

            try:
                self.totalCountKeepWarm = int(config.get(section, 'keepwarm')) + self.countKeepWarm - self.deltaCountKeepWarm
                self.deltaCountKeepWarm += self.countKeepWarm - self.deltaCountKeepWarm
                config.set(section, 'keepwarm', str(self.totalCountKeepWarm))
            except Exception:
                config.set(section, 'keepwarm', str(self.countKeepWarm))
                
                
        if self.isCoffee:
            try:
                self.totalCountCarafeRemoved = int(config.get(section, 'caraferemoved')) + self.countCarafeRemoved - self.deltaCountCarafeRemoved
                self.deltaCountCarafeRemoved += self.countCarafeRemoved - self.deltaCountCarafeRemoved
                config.set(section, 'caraferemoved', str(self.totalCountCarafeRemoved))
            except Exception:
                config.set(section, 'caraferemoved', str(self.countCarafeRemoved))

            try:
                self.totalCountGrinderOn = int(config.get(section, 'grinder')) + self.countGrinderOn - self.deltaCountGrinderOn
                self.deltaCountGrinderOn += self.countGrinderOn - self.deltaCountGrinderOn
                config.set(section, 'grinder', str(self.totalCountGrinderOn))
            except Exception:
                config.set(section, 'grinder', str(self.countGrinderOn))

            try:
                self.totalCountHotPlateOn = int(config.get(section, 'hotplate')) + self.countHotPlateOn - self.deltaCountHotPlateOn
                self.deltaCountHotPlateOn += self.countHotPlateOn - self.deltaCountHotPlateOn
                config.set(section, 'hotplate', str(self.totalCountHotPlateOn))
            except Exception:
                config.set(section, 'hotplate', str(self.countHotPlateOn))

        try:
            self.totalSessionCount = int(config.get(section, 'sessions')) + self.sessionCount - self.deltaSessionCount
            self.deltaSessionCount += self.sessionCount - self.deltaSessionCount
            config.set(section, 'sessions', str(self.totalSessionCount))
        except Exception:
            config.set(section, 'sessions', str(self.sessionCount))

        
        with open(self.settingsPath+self.host+'.conf', 'w') as f:
            config.write(f)

        
        if self.dump:
            self.print_stats()



    @threadsafe_function
    def disconnect(self):
 
        self.run = False
        
        if self.connected:
            
            self.write_stats()
        
            if self.dump:
                x = self.device
                if x == "Unknown": x = "device"
                print "[" + self.host +  ":" + '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + "] Disconnecting " + x
        
            self.connected = False
            try:
                if self.monitor:
                    if self.writeLock.locked():
                        self.writeLock.release()
                    if self.socketLock.locked():
                        self.socketLock.release()
            except Exception:
                raise SmarterError(SmarterClientFailedStopThread,"Could not disconnect from " + self.host)

            self.monitor = None
            try:
                if self.socket:
                    self.socket.close()
                    self.socket = None
            # FIX: Also except thread exceptions..
            except socket.error, msg:
                self.socker = None
                raise SmarterError(SmarterClientFailedStop,"Could not disconnect from " + self.host + " (" + msg[1] + ")")


    def find_devices(self):
        devices = []
        try:
            cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            command = Smarter.number_to_raw(Smarter.CommandDeviceInfo) + Smarter.number_to_raw(Smarter.MessageTail)
            #command = '\x64\x7e'
  
            cs.sendto(command, ('255.255.255.255', self.port))
            cs.settimeout(4)

            # support up to 100 devices
            for i in range (0,100):
                message, server = cs.recvfrom(4)
                # '0x64 type version 0x7e
                if Smarter.raw_to_number(message[0]) == Smarter.ResponseDeviceInfo and Smarter.raw_to_number(message[3]) == Smarter.MessageTail:
                    devices.append((server[0],Smarter.raw_to_number(message[1]),Smarter.raw_to_number(message[2])))
        except Exception:
            pass
        finally:
            cs.close()
        return devices
 
 
    #------------------------------------------------------
    # MESSAGE RESPONSE DECODERS
    #------------------------------------------------------


    def decode_ResponseKettleSettings(self,message):
        #self.switch_kettle_device()
        self.defaultKeepWarmTime  = Smarter.raw_to_number(message[2])
        self.defaultTemperature   = Smarter.raw_to_temperature(message[1])
        self.defaultFormulaTemperature = Smarter.raw_to_number(message[3])


    def decode_ResponseCoffeeSettings(self,message):
        #self.switch_coffee_device()
        self.defaultCups          = Smarter.raw_to_cups(message[1])
        self.defaultStrength      = Smarter.raw_to_strength(message[2])
        self.defaultGrind         = Smarter.raw_to_bool(message[3])
        self.defaultHotPlate      = Smarter.raw_to_hotplate(message[4])


    def switch_kettle_device(self):
        if not self.isKettle:
            self.isKettle = True
            self.isCoffee = False
            self.write_stats()
            self.deviceId = Smarter.DeviceKettle
            self.device = Smarter.device_to_string(Smarter.DeviceKettle)


    def switch_coffee_device(self):
        if not self.isCoffee:
            self.isKettle = False
            self.isCoffee = True
            self.write_stats()
            self.deviceId = Smarter.DeviceCoffee
            self.device = Smarter.device_to_string(Smarter.DeviceCoffee)

    def decode_ResponseKettleStatus(self,message):
        #self.switch_kettle_device()
        self.statusMessage       = message

        self.kettleStatus        = Smarter.raw_to_number(message[1])
            
        if self.kettleStatus == Smarter.KettleHeating:
            if not self.heaterOn:
                heaterOn = True
            if self.keepWarmOn == True:
                self.keepWarmOn = False
                self.countKeepWarm += 1
        elif self.kettleStatus == Smarter.KettleKeepWarm:
            if not self.keepWarmOn:
                self.keepWarmOn = True
            if self.heaterOn == True:
                self.heaterOn = False
                self.countHeater += 1
        else:
            if self.keepWarmOn == True:
                self.keepWarmOn = False
                self.countKeepWarm += 1
            if self.heaterOn == True:
                self.heaterOn = False
                self.countHeater+= 1

        self.temperature            = Smarter.raw_to_temperature(message[2])
        self.waterSensor            = Smarter.raw_to_watersensor(message[3],message[4])
        
        if self.onBase != Smarter.is_on_base(message[2]):
            if self.onBase:
                self.countKettleRemoved += 1
            self.onBase = Smarter.is_on_base(message[2])
            
        self.unknown            = Smarter.raw_to_number(message[5])



    def decode_ResponseCoffeeStatus(self,message):
        #self.switch_coffee_device()
        
        def is_set(x, n):
            return x & 2**n != 0
        
        self.statusMessage       = message
        self.coffeeStatus        = Smarter.raw_to_number(message[1])
        
        if self.carafe != is_set(self.coffeeStatus,0):
            if not self.carafe:
                 self.countCarafeRemoved += 1
            self.carafe = is_set(self.coffeeStatus,0)
        
        if self.heaterOn != is_set(self.coffeeStatus,4):
            if not self.heaterOn:
                self.countHeater += 1
            else:
                # what happens when it fails?? or stopped
                countCupsBrew += cupsBrew
            self.heaterOn = is_set(self.coffeeStatus,4)

        if self.hotPlateOn != is_set(self.coffeeStatus,6):
            if not self.hotPlateOn:
                self.countHotPlateOn += 1
            self.hotPlateOn = is_set(self.coffeeStatus,6)
        
        if self.grinderOn != is_set(self.coffeeStatus,3):
            if not self.grinderOn:
                self.countGrinderOn += 1
            self.grinderOn = is_set(self.coffeeStatus,3)
            
        
    
        self.ready               = is_set(self.coffeeStatus,2)
        self.grind               = is_set(self.coffeeStatus,1)
        self.working             = is_set(self.coffeeStatus,5)
        self.timerEvent          = is_set(self.coffeeStatus,7)
        self.waterLevel          = Smarter.raw_to_waterlevel(message[2])
        self.waterEnough         = Smarter.raw_to_waterlevel_bit(message[2])
        self.strength            = Smarter.raw_to_strength(message[4])
        self.cups                = Smarter.raw_to_cups(message[5])
        self.cupsBrew            = Smarter.raw_to_cups_brew(message[5])
        self.unknown             = Smarter.raw_to_number(message[3])


    def decode_ResponseDeviceInfo(self,message):
        self.isCoffee = False
        self.isKettle = False
        
        self.deviceId = Smarter.raw_to_number(message[1])
        self.version = Smarter.raw_to_number(message[2])

        if self.deviceId == Smarter.DeviceKettle:
            self.isKettle = True
            self.device = Smarter.device_to_string(self.deviceId)
        
        if self.deviceId == Smarter.DeviceCoffee:
            self.isCoffee = True
            self.device = Smarter.device_to_string(self.deviceId)


    def decode_ResponseBase(self,message):
        #self.switch_kettle_device()
        self.waterSensorBase = Smarter.raw_to_watersensor(message[1],message[2])


    def decode_ResponseCarafe(self,message):
        #self.switch_coffee_device()
        self.carafeMode = Smarter.raw_to_bool(message[1])


    def decode_ResponseSingleCupMode(self,message):
        #self.switch_coffee_device()
        self.singlecup  = Smarter.raw_to_bool(message[1])


    def decode_ResponseCommandStatus(self,message):
        self.commandStatus = Smarter.raw_to_number(message[1])


    def decode_ResponseWifiFirmware(self,message):
        s = ""
        for i in range(1,len(message)-1):
            x = str(message[i])
            if x in string.printable:
                s += x
        self.WifiFirmware = s


    def decode_ResponseTimers(self,message):
        #self.switch_coffee_device()
        pass


    def decode_ResponseWirelessNetworks(self,message):
        a = ""
        w = []
        db = False
        for i in range(1,len(message)-1):
            x = str(message[i])
            if x == ',':
               db = True
               d = ""
               continue
            elif x == '}':
               db = False
               w += [(a,int(d))]
               a = ""
               continue
            elif not db and x in string.printable:
                a += x
            elif db and x in string.printable:
                d += x
        from operator import itemgetter
    
        # most powerfull wifi on top
        self.Wifi = sorted(w,key=itemgetter(1),reverse=True)


    def decode_ResponseCoffeeHistory(self,message):
        #self.switch_coffee_device()
        counter = Smarter.raw_to_number(message[1])
        if counter > 0:
            for i in range(0,counter):
                self.historySuccess = Smarter.raw_to_bool(message[i*32+13])
        else:
            pass
  
  
    def decode_ResponseKettleHistory(self,message):
        #self.switch_kettle_device()
        
        counter = Smarter.raw_to_number(message[1])
        if counter > 0:
            for i in range(0,counter):
                # read 32 bytes payload
                # queue!!!!
                self.historyTemperature = Smarter.raw_to_temperature(message[i*32+1+2])
                self.historyKeepWarmTime = Smarter.raw_to_keepwarm(message[i*32+2+2])
                self.historyFormulaTemperature = Smarter.raw_to_temperature(message[i*32+3+2])
                self.historyHours   = Smarter.raw_to_temperature(message[i*32+6+2])
                self.historyMinutes = Smarter.raw_to_temperature(message[i*32+7+2])
                self.historyDay     = Smarter.raw_to_temperature(message[i*32+8+2])
                self.historyMonth   = Smarter.raw_to_temperature(message[i*32+9+2])
                self.historyYear    = Smarter.raw_to_temperature(message[i*32+10+2])+1980
                
    
                # CHECK THIS
                
                #print str(self.historyHours) + ":" + str(self.historyMinutes)
                #print str(self.historyDay) + "-" + str(self.historyMonth) + "-" + str(self.historyYear)
                self.historySuccess = Smarter.raw_to_bool(message[i*32+13])
        else:
            self.historyTemperature = 0
            self.historyFormulaTemperature = 0
            self.historySuccess = False
            self.historyKeepWarmTime = 0



    #------------------------------------------------------
    # COMMANDS: iKettle 2.0 & Smarter Coffee 
    #------------------------------------------------------


    def device_raw(self,code):
        dump = self.dump
        self.dump = True
        self.send(Smarter.codes_to_message(code))
        self.dump = dump
        

    def device_info(self):
        self.send_command(Smarter.CommandDeviceInfo)


    def device_check(self):
            if not self.isKettle and not self.isCoffee:
                self.fast = False
                self.device_info()


    def device_store_settings(self,v1,v2,v3,v4):
        self.device_check()
        if self.isKettle:   self.kettle_store_settings(Smarter.string_to_temperature(v1),Smarter.string_to_keepwarm(v2),Smarter.string_to_bool(v3),Smarter.string_to_temperature(v4))
        elif self.isCoffee:
            try:
                b = Smarter.string_to_grind(v3)
            except Exception:
                b = Smarter.string_to_bool(v3)
            self.coffee_store_settings(Smarter.string_to_cups(v1),Smarter.string_to_hotplate(v2),b,Smarter.string_to_strength(v4))


    def device_settings(self):
        self.device_check()
        if self.isKettle:   self.kettle_settings()
        elif self.isCoffee: self.coffee_settings()


    def device_history(self):
        self.device_check()
        if   self.isKettle: self.kettle_history()
        elif self.isCoffee: self.coffee_history()


    def device_stop(self):
        self.device_check()
        if self.isKettle:   self.kettle_stop()
        elif self.isCoffee: self.coffee_stop()


    def device_start(self):
        self.device_check()
        if self.isKettle:   self.kettle_heat_settings()
        elif self.isCoffee: self.coffee_brew_settings()


    def device_default(self):
        self.device_check()
        if self.isKettle:   self.kettle_store_settings()
        elif self.isCoffee: self.coffee_store_settings()


    def device_reset(self):
        self.send_command(Smarter.CommandResetSettings)
        defaultFormulaTemperature = 0
        defaultFormula = 0
        defaultKeepWarmTime = 0
        defaultTemperature = 100
   
     
    def device_update(self):
        self.send_command(Smarter.CommandUpdate)


    def device_time(self,second = 0,minute = 0,hour = 12,unknown = 0,day = 17, month=1, century = 20,year = 16):
        self.send_command(Smarter.CommandDeviceTime,Smarter.number_to_raw(second) + Smarter.number_to_raw(minute) + Smarter.number_to_raw(hour) + Smarter.number_to_raw(unknown) + Smarter.number_to_raw(day) + Smarter.number_to_raw(month) + Smarter.number_to_raw(century) + Smarter.number_to_raw(year))



    #------------------------------------------------------
    # COMMANDS: Wifi
    #------------------------------------------------------


    def wifi_firmware(self):
        self.send_command(Smarter.CommandWifiFirmware)


    def wifi_scan(self):
        self.send_command(Smarter.CommandWifiScan)


    def wifi_leave(self):
        self.send_command(Smarter.CommandWifiLeave)


    def wifi_connect(self):
        self.send_command(Smarter.CommandWifiJoin)


    def wifi_join(self,network,password=""):
        self.fast = False
        self.send_command(Smarter.CommandWifiNetwork,Smarter.text_to_raw(network))
        self.send_command(Smarter.CommandWifiPassword,Smarter.text_to_raw(password))
        self.send_command(Smarter.CommandWifiJoin)


    #------------------------------------------------------
    # COMMANDS: iKettle 2.0
    #------------------------------------------------------

 
    def kettle_store_settings(self, temperature = 100, timer = 0, formulaOn = False, formulaTemperature = 75):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandKettleStoreSettings, Smarter.keepwarm_to_raw(timer) + Smarter.temperature_to_raw(temperature) + Smarter.bool_to_raw(formulaOn) + Smarter.temperature_to_raw(formulaTemperature))
            if self.commandStatus == Smarter.StatusSucces:
                self.defaultKeepWarmTime        = timer
                self.defaultFormula             = formulaOn
                self.defaultFormulaTemperature  = formulaTemperature
                self.defaultTemperature         = temperature
            else:
               SmarterErrorOld(KettleFailedStoreSettings,"Could not store kettle machine settings")
        else:
            raise SmarterErrorOld(KettleNoMachineStoreSettings,"You need a Kettle machine to store settings")


    def kettle_settings(self):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandKettleSettings)
        else:
            raise SmarterErrorOld(KettleNoMachineSettings,"You need a Kettle machine to get its settings")


    def kettle_heat(self,temperature=100,keepwarm=0):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandHeat,Smarter.temperature_to_raw(temperature)+Smarter.keepwarm_to_raw(keepwarm))
        else:
            raise SmarterError(KettleNoMachineHeat,"You need a kettle to heat it")


    def kettle_heat_default(self):
        self.kettle_heat(self.defaultTemperature,self.defaultKeepWarmTime)


    def kettle_heat_settings(self):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandHeatDefault)
        else:
            raise SmarterError(KettleNoMachineHeat,"You need a kettle to heat it")


    def kettle_formula_heat(self, formulaTemperature = 75, keepwarm = 0):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandHeatFormula,Smarter.temperature_to_raw(formulaTemperature)+Smarter.keepwarm_to_raw(keepwarm))
        else:
            raise SmarterError(KettleNoMachineHeatFormula,"You need a kettle to heat in formula mode")


    def kettle_stop(self):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandKettleStop)
        else:
            raise SmarterError(KettleNoMachineStop,"You need a kettle to stop heating")


    def kettle_history(self):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandKettleHistory)
        else:
            raise SmarterError(KettleNoMachineHistory,"You need a kettle machine to get its history")



    #------------------------------------------------------
    # COMMANDS: Kettle Calibrate
    #------------------------------------------------------


    def kettle_calibrate(self):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandCalibrate)
        else:
            raise SmarterErrorOld(KettleNoMachineSettings,"You need a Kettle to calibrate")


    def kettle_calibrate_base(self):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandBase)
        else:
            raise SmarterErrorOld(KettleNoMachineSettings,"You need a Kettle to get its calibration base value")


    def kettle_calibrate_store_base(self,base = 1000):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandStoreBase,Smarter.watersensor_to_raw(base))
            self.waterSensorBase = base
        else:
            raise SmarterErrorOld(KettleNoMachineSettings,"You need a Kettle to set its calibration base value")



    #------------------------------------------------------
    # COMMANDS: Smarter Coffee 
    #------------------------------------------------------


    def coffee_settings(self):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandCoffeeSettings)
        else:
            raise SmarterError(CoffeeNoMachineSettings,"You need a coffee machine to get its settings")


    def coffee_history(self):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandCoffeeHistory)
        else:
            raise SmarterError(CoffeeNoMachineHistory,"You need a coffee machine to get its history")


    def coffee_stop(self):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandCoffeeStop)
        else:
            raise SmarterError(CoffeeNoMachineStop,"You need a coffee machine to stop brewing coffee")


    def coffee_single_cup_mode(self):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandSingleCupMode)
        else:
            raise SmarterError(CoffeeNoMachineSingleCupMode,"You need a coffee machine to get its single cup mode status")


    def coffee_single_cup_mode_on(self):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandSetSingleCupMode,Smarter.bool_to_raw(True))
        else:
            raise SmarterError(CoffeeNoMachineSingleCupMode,"You need a coffee machine to set single cup mode on")


    def coffee_single_cup_mode_off(self):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandSetSingleCupMode,Smarter.bool_to_raw(False))
        else:
            raise SmarterError(CoffeeNoMachineSingleCupMode,"You need a coffee machine to set single cup mode off")


    def coffee_carafe(self):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandCarafe)
        else:
            raise SmarterError(CoffeeNoMachineCarafe,"You need a coffee machine to get its carafe required status")


    def coffee_carafe_on(self):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandSetCarafe,Smarter.bool_to_raw(False))
        else:
            raise SmarterError(CoffeeNoMachineCarafe,"You need a coffee machine to set carafe required on")


    def coffee_carafe_off(self):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandSetCarafe,Smarter.bool_to_raw(True))
        else:
            raise SmarterError(CoffeeNoMachineCarafe,"You need a coffee machine to set carafe required off")


    def coffee_store_settings(self, cups = 1, hotplate = 0, grind = True, strength = 1):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandCoffeeStoreSettings,Smarter.strength_to_raw(strength)+Smarter.cups_to_raw(cups)+Smarter.bool_to_raw(grind)+Smarter.hotplate_to_raw(hotplate))

            if self.commandStatus == Smarter.StatusSucces:
                self.defaultCups = cups
                self.defaultStrength = strength
                self.defaultGrind = grind
                self.defaultHotPlate = hotplate
            else:
                raise SmarterError(CoffeeFailedStoreSettings,"Could not store coffee machine settings")

        else:
            raise SmarterError(CoffeeNoMachineStoreSettings,"You need a coffee machine to store settings")
    

    def coffee_brew_default(self):
        self.brew(self.defaultCups,self.defaultStrength,self.defaultHotPlate,self.defaultGrind)


    def coffee_brew_settings(self):
        #  cups strength hotplate grind
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandBrewDefault)
        else:
            raise SmarterError(CoffeeNoMachineBrew,"You need a coffee machine to brew coffee")


    def coffee_brew(self, cups = 1, hotplate = 0, grind = True, strength = 1):
        #  cups strength hotplate grind
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandBrew,Smarter.cups_to_raw(cups)+Smarter.strength_to_raw(strength)+Smarter.hotplate_to_raw(hotplate)+Smarter.bool_to_raw(grind))
        else:
            raise SmarterError(CoffeeNoMachineBrew,"You need a coffee machine to brew coffee")


    def coffee_descaling(self):
        if self.fast or self.isCoffee:
            if self.waterLevel == Smarter.CoffeeWaterFull:
                try:
                    self.coffee_brew(12,0,False,Smarter.CoffeeWeak)
                except:
                    raise SmarterError(CoffeeNoMachineBrew,"Descaling failed")
            raise SmarterError(CoffeeNoMachineBrew,"Not enough water, please fill to full")
        raise SmarterError(CoffeeNoMachineBrew,"You need a coffee machine to descale it")
    
    
    
    def coffee_hotplate_off(self):
        if self.fast or self.isCoffee == True:
            self.send_command(Smarter.CommandHotplateOff)
        else:
            raise SmarterError(CoffeeNoMachineHotplateOff,"You need a coffee machine to turn off the hotplate")
 

    def coffee_hotplate_on(self, timer=0):
        if self.fast or self.isCoffee == True:
            if timer == 0:
                self.send_command(Smarter.CommandHotplateOff)
            else:
                self.send_command(Smarter.CommandHotplateOn,Smarter.hotplate_to_raw(timer))
            self.hotPlate = timer
        else:
            raise SmarterError(CoffeeNoMachineHotplateOn,"You need a coffee machine to turn on the hotplate")


    def coffee_grinder_toggle(self):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandGrinder)
        
        else:
            raise SmarterError(CoffeeNoMachineGrinder,"You need a coffee machine to toggle the grinder")


    def coffee_filter(self):
        if self.isCoffee and self.grind:
            self.send_command(Smarter.CommandGrinder)
        else:
            raise SmarterError(CoffeeNoMachineGrinder,"You need a coffee machine to use the filter")


    def coffee_timers(self):
        if self.isCoffee and self.grind:
            self.send_command(Smarter.CommandTimers)
        else:
            raise SmarterError(CoffeeNoMachineGrinder,"You need a coffee machine to use timers")


    def coffee_timer_disable(self,index=0):
        if self.isCoffee and self.grind:
            pass #self.send_command(Smarter.CommandDisableTimer)
        else:
            raise SmarterError(CoffeeNoMachineGrinder,"You need a coffee machine to use timers")


    def coffee_timer_store(self,index=0,time=None):
        if self.isCoffee and self.grind:
            pass #self.send_command(Smarter.CommandStoreTimer)
        else:
            raise SmarterError(CoffeeNoMachineGrinder,"You need a coffee machine to use timers")


    def coffee_beans(self):
        if self.isCoffee and not self.grind:
            self.send_command(Smarter.CommandGrinder)
        else:
            raise SmarterError(CoffeeNoMachineGrinder,"You need a coffee machine to grind beans")


    def coffee_cups(self,cups=1):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandCups,Smarter.cups_to_raw(cups))
            self.cups = cups
        else:
            raise SmarterError(CoffeeNoMachineCups,"You need a coffee machine to select the number of cups to brew")


    def coffee_strength(self,strength="medium"):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandStrength ,Smarter.strength_to_raw(Smarter.string_to_strength(strength)))
            self.strength = strength
        else:
            raise SmarterError(CoffeeNoMachineStrength,"You need a coffee machine to select the coffee strength")



    #------------------------------------------------------
    # STRING/PRINT SMARTER INFO
    #------------------------------------------------------


    def print_info(self):
        print Smarter.device_info(self.deviceId,self.version)


    def print_singlecupmode(self):
        if self.singlecup:
            print "Single cup mode"
        else:
            print "Carafe mode"


    def print_carafe(self):
        if self.carafeMode:
            print "Can brew without carafe"
        else:
            print "Carafe needed for brewing"


    def print_watersensor_base(self):
        print "Watersensor calibration base value: " + str(self.waterSensorBase)


    def print_wireless_networks(self):
        print
        print "         Signal   Wireless Network"
        for i in range(0,len(self.Wifi)):
            
            quality = Smarter.dbm_to_quality(self.Wifi[i][1])
            
            s = ""
            for x in range(quality / 10,10):
                s += " "
            for x in range(0,quality / 10):
                s += "█"

            print "     " + s + "   " + self.Wifi[i][0]
        print


    def print_wifi_firmware(self):
        print
        print self.WifiFirmware
        print
    
    
    def print_settings(self):
        if self.isKettle:
            self.print_kettle_settings()
        elif self.isCoffee:
            self.print_coffee_settings()
            
            
    def print_coffee_settings(self):
        print Smarter.string_coffee_settings(self.defaultCups, self.defaultStrength, self.defaultGrind, self.defaultHotPlate)


    def print_kettle_settings(self):
        print Smarter.string_kettle_settings(self.defaultTemperature, self.defaultFormula, self.defaultFormulaTemperature, self.defaultKeepWarmTime)


    def print_timers(self):
        # fix this
        print "Not yet implemented"


    def print_coffee_history(self):
        # fix this
        if not self.historySuccess:
            print "No history available"
            return
        print "Not yet implemented"


    def print_history(self):
        if self.isKettle:
            self.print_kettle_history()
        elif self.isCoffee:
            self.print_coffee_history()


    def print_kettle_history(self):
        # fix this
        if not self.historySuccess:
            print "No history available"
            return
        print "Not yet implemented"


    def print_short_kettle_status(self):
        if self.onBase:
            print Smarter.status_kettle_description(self.kettleStatus) + " on base: temperature " + Smarter.temperature_to_string(self.temperature) + ", watersensor " + str(self.waterSensor)
        else:
            print Smarter.status_kettle_description(self.kettleStatus) + " off base"


    def print_short_status(self):
        if self.isKettle:
            self.print_short_kettle_status()
        elif self.isCoffee:
            self.print_short_coffee_status()


    def print_kettle_status(self):
        if self.onBase:
            print "Status           " + Smarter.status_kettle_description(self.kettleStatus)
            print "Temperature      " + Smarter.temperature_to_string(self.temperature)
            print "Water sensor     " + str(self.waterSensor) + " (calibration base " + str(self.waterSensorBase) + ")"
        else:
            print "Status           off base"
        print "Default heating  " + Smarter.string_kettle_settings(self.defaultTemperature,self.defaultFormula, self.defaultFormulaTemperature,self.defaultKeepWarmTime)


    def string_coffee_bits(self):
        s = ""
        if not self.carafeMode:
            s += ", carafe required"
        if self.singlecup:
            s += ", single cup mode"
        else:
            s += ", carafe mode"
        if not self.waterEnough:
            s += ", not enough water to brew"
        if self.timerEvent:
            s += ", timer triggered"
        return s


    def print_short_coffee_status(self):
        print Smarter.string_coffee_status(self.ready, self.cupsBrew, self.working, self.heaterOn, self.hotPlateOn, self.carafe, self.grinderOn) + ", water " + Smarter.waterlevel(self.waterLevel) + ", setting: " + Smarter.string_coffee_settings(self.cups, self.strength, self.grind, self.hotPlate) + self.string_coffee_bits()


    def print_coffee_status(self):
        print "Status           " + Smarter.string_coffee_status(self.ready, self.cupsBrew, self.working, self.heaterOn, self.hotPlateOn, self.carafe, self.grinderOn) + self.string_coffee_bits()
        print "Water level      " + Smarter.waterlevel(self.waterLevel)
        print "Setting          " + Smarter.string_coffee_settings(self.cups, self.strength, self.grind, self.hotPlate)
        print "Default brewing  " + Smarter.string_coffee_settings(self.defaultCups, self.defaultStrength, self.defaultGrind, self.defaultHotPlate)


    def print_status(self):
        print
        if self.isKettle:
            self.print_kettle_status()
        elif self.isCoffee:
            self.print_coffee_status()
        print


    def string_connect_status(self):
        if self.connected:
            s = ""
            if self.isDirect:
                s = " directly"
            return "Connected" + s + " to [" + self.host + "] " + Smarter.device_info(self.deviceId,self.version)
        return "Not connected"


    def print_connect_status(self):
        print self.string_connect_status()
    

    def print_devices_found(self,devices):
        for i in range(0,len(devices)):
            print "[" + devices[i][0] +  ":" + '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + "] Found " + Smarter.device_info(devices[i][1],devices[i][2])
        if len(devices) == 0:
            print "No coffee machine or kettle found"

    def print_stats(self):
        print
        print "  Stats "+ self.host
        print "  ______"+ "_"*len(self.host)
        print
        print
        print "  " + str(self.totalSendCount).rjust(9, ' ')   + "  Commands ("  + Smarter.bytes_to_human(self.totalSendBytesCount) + ")"
        print "  " + str(self.totalReadCount).rjust(9, ' ')   + "  Responses (" + Smarter.bytes_to_human(self.totalReadBytesCount) + ")"
        if self.totalSessionCount != 0:
            print "  " + str(self.totalSessionCount).rjust(9, ' ') + "  " + "Sessions"
        print
        print
        if self.isCoffee:
            print "  " + str(self.totalCountCarafeRemoved).rjust(9, ' ') + "  Carafe removed"
            print "  " + str(self.totalCountCupsBrew).rjust(9, ' ') + "  Cups brew"
            print "  " + str(self.totalCountHeater).rjust(9, ' ') + "  Heater on"
            print "  " + str(self.totalCountHotPlateOn).rjust(9, ' ') + "  Hotplate on"
            print "  " + str(self.totalCountGrinderOn).rjust(9, ' ') + "  Grinder on"
        elif self.isKettle:
            print "  " + str(self.totalCountKettleRemoved).rjust(9, ' ') + "  Kettle removed"
            print "  " + str(self.totalCountHeater).rjust(9, ' ') + "  Heater on"
            print "  " + str(self.totalCountKeepWarm).rjust(9, ' ') + "  Kept warm"
        print
        print
        if self.sendCount != 0 or self.readCount != 0:
            print "  Current session"
            print
        #    print "  " + str(self.sessionCount).rjust(10, ' ') + "  Connected"
            print "  " + str(self.sendCount).rjust(9, ' ')   + "  Commands ("  + Smarter.bytes_to_human(self.sendBytesCount) + ")"
            print "  " + str(self.readCount).rjust(9, ' ')   + "  Responses (" + Smarter.bytes_to_human(self.readBytesCount) + ")"
            print
            
            for id in sorted(self.commandCount):
                print "  " + str(self.commandCount[id]).rjust(9, ' ') + "  [" + Smarter.number_to_code(id) + "] " + Smarter.message_description(id)
            print
            
            for id in sorted(self.responseCount):
                print "  " + str(self.responseCount[id]).rjust(9, ' ') + "  [" + Smarter.number_to_code(id) + "] "  + Smarter.message_description(id)
            print
            if self.isCoffee:
                print "  " + str(self.countCarafeRemoved).rjust(9, ' ') + "  Carafe removed"
                print "  " + str(self.countCupsBrew).rjust(9, ' ') + "  Cups brew"
                print "  " + str(self.countHeater).rjust(9, ' ') + "  Heater on"
                print "  " + str(self.countHotPlateOn).rjust(9, ' ') + "  Hotplate on"
                print "  " + str(self.countGrinderOn).rjust(9, ' ') + "  Grinder on"
            elif self.isKettle:
                print "  " + str(self.countKettleRemoved).rjust(9, ' ') + "  Kettle removed"
                print "  " + str(self.countHeater).rjust(9, ' ') + "  Heater on"
                print "  " + str(self.countKeepWarm).rjust(9, ' ') + "  Kept warm"
            print
                

    def print_message_send(self,message):
        print "[" + self.host +  ":" + '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + "] Message Send     [" + Smarter.message_description(Smarter.raw_to_number(message[0])) + "] [" + Smarter.message_to_codes(message) + "]"


    def print_message_read(self,message):
        id = Smarter.raw_to_number(message[0])
        print "[" + self.host +  ":" + '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + "] Message Received [" + Smarter.message_description(id) + "] [" + Smarter.message_to_codes(message) + "]"
        if   id == Smarter.ResponseCommandStatus:   print "Command replied: " + Smarter.status_command(self.commandStatus)
        elif id == Smarter.ResponseWirelessNetworks: self.print_wireless_networks()
        elif id == Smarter.ResponseWifiFirmware:    self.print_wifi_firmware()
        elif id == Smarter.ResponseKettleHistory:   self.print_kettle_history()
        elif id == Smarter.ResponseCoffeeHistory:   self.print_coffee_history()
        elif id == Smarter.ResponseKettleSettings:  self.print_kettle_settings()
        elif id == Smarter.ResponseCoffeeSettings:  self.print_coffee_settings()
        elif id == Smarter.ResponseCarafe:          self.print_carafe()
        elif id == Smarter.ResponseSingleCupMode:   self.print_singlecupmode()
        elif id == Smarter.ResponseDeviceInfo:      self.print_info()
        elif id == Smarter.ResponseBase:            self.print_watersensor_base()
        elif id == Smarter.ResponseKettleStatus:    self.print_short_kettle_status()
        elif id == Smarter.ResponseCoffeeStatus:    self.print_short_coffee_status()
        elif id == Smarter.ResponseTimers:          self.print_timers()
        else:                                       print "Unknown Reply Message"

