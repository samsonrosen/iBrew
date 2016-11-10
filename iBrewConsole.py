# -*- coding: utf-8 -*-

import sys
import time
import datetime
import logging

import locale
import platform
import codecs

import logging.handlers

from smarter.SmarterInterface import *
from smarter.SmarterProtocol import *

from iBrewWeb import *
from iBrewJokes import *
from iBrewFolders import AppFolders

import re
import random

import traceback

#------------------------------------------------------
# iBrew
#
# Console Interface to iKettle 2.0 & Smarter Coffee Devices
#
# https://github.com/Tristan79/iBrew
#
# Copyright © 2016 Tristan (@monkeycat.nl)
#
# Kettle Rattle (rev 6)
#------------------------------------------------------



#------------------------------------------------------
# iBrew VERSION INFORMATION
#------------------------------------------------------


iBrewApp          = "iBrew: iKettle 2.0 & Smarter Coffee Interface"
iBrewInfo         = "iBrew: Brewing on the 7th day © 2016 Tristan (@monkeycat.nl)"
iBrewContribute   = "Please contribute any discoveries on https://github.com/Tristan79/iBrew/issues"

class iBrewConsole:

    #------------------------------------------------------
    # iBrew MONITOR
    #------------------------------------------------------
    # assume we're connected to a client! we're printing
    # every message received. you can stop the monitor by
    # pressing ctrl-c, the only messages we expect to
    # receive is a response message 14 (status device),
    # if there are any other messages we print them too!
    
    def monitor(self):
        print "iBrew: Press ctrl-c to stop"
        
        
        dump = self.client.dump
        self.client.dump_status = True
        self.client.dump = True
        
        while True:
            try:
                x = raw_input("")
            except KeyboardInterrupt:
                self.quit = True
                break
            except Exception, e:
                self.quit = True
                logging.debug(traceback.format_exc())
                logging.debug(str(e))
                break
        self.client.dump = dump
        self.client.dump_status = False
        print



    #------------------------------------------------------
    # iBrew WEB
    #------------------------------------------------------

    # assume we're connected to a client
    # you can stop the web server by pressing ctrl-c
    def web(self,port=Smarter.Port-1):
        
        webs = None
        try:
            if self.haveHost:
                self.web = iBrewWeb()
                self.web.run(port,self.client.dump,self.client.host)
            else:
                self.web = iBrewWeb()
                self.web.run(port,self.client.dump)
        except Exception, e:
            logging.debug(e)
            logging.info("iBrew: Failed to run Web Interface & REST API on port " + str(port))
            return
        logging.info("iBrew: Starting Web Interface & REST API on port " + str(port) + ". Press ctrl-c to stop")
        self.monitor()
        self.web.kill()
        logging.info("iBrew: Stopped Web Interface & REST API on port " + str(port))
 

    #------------------------------------------------------
    # iBrew SWEEP
    #------------------------------------------------------

    # assume we're connected to a client
    # you can stop the sweep by pressing ctrl-c
    def sweep(self,start=1):
        if int(start) <= 0 or start > 256:
            print 'iBrew: sweep start out of range [00..ff]'
            return

        dump = self.client.dump
        self.client.dump = True
        self.client.dump_status = False
        
        print
        print "DO NOT DO THIS IF YOU DO NOT KNOW WHAT YOU ARE DOING"
        print
        print "IT CAN RENDER THE " + Smarter.device_to_string(self.client.deviceId) + " COMPLETELY USELESS"
        print
        print "Are you really, really sure?"
        try:
            i = raw_input("Please enter YES if you are: ")
            if i != "YES":
                return
        except Exception:
            return
        print "iBrew: Press ctrl-c to stop"
 

        for id in range(int(start),256):
            try:
                # known command/message?
                known = False
                if self.client.isKettle:
                    known = Smarter.message_kettle(id)
                if self.client.isCoffee:
                    known = Smarter.message_coffee(id)
                # know command for other device except itself?
                if not known:
                
                    # add zero here...
                    print "iBrew: Probing command: " + Smarter.number_to_code(id)

                    # button pressed quit...
                    self.client.device_raw(Smarter.number_to_code(id))

                    # check if got also a ???status message... FIX
                    if self.client.commandStatus != Smarter.StatusInvalid:
                        print "iBrew: New command found: " + Smarter.number_to_code(id)
                    self.client.dump = False
                    self.client.device_stop()
                    self.client.dump = True
            except Exception:
                # was it ctrl-c or error???
                break;
        self.client.dump = dump



    #------------------------------------------------------
    # iBrew Console MAIN LOOP
    #------------------------------------------------------

    def is_valid_ipv4_address(self,address):
        try:
            socket.inet_pton(socket.AF_INET, address)
        except AttributeError:  # no inet_pton here, sorry
            try:
                socket.inet_aton(address)
            except socket.error:
                return False
            return address.count('.') == 3
        except socket.error:  # not a valid address
            return False
        return True


    def is_valid_ipv6_address(self,address):
        try:
            socket.inet_pton(socket.AF_INET6, address)
        except socket.error:  # not a valid address
            return False
        return True
        

    def check_license(self):
        self.username = "WebServer"
        
        if not os.path.isfile(AppFolders.settings() + '/.ibrew'):
            self.username = "NOT ACCEPTED"
            self.app_info()
            print
            print "PLEASE READ THE FOLLOWING VERY CAREFULLY"
            print
            print
            print "LICENSE " + iBrewApp
            print
            print Smarter.license()
            print
            print
            print "WARNING: YOU COULD BRICK YOUR DEVICE, USE AT YOUR OWN RISK"
            print
            print "NOTE: THIS IS OFFLINE! NO INFORMATION WILL BE SHARED WITH ANYONE!"
            print
            print
            print "LICENSING AGREEMENT"
            try:
                self.username = raw_input("Please enter your full name: ").strip()
                c = 0
                while not (' ' in self.username):
                    c += 1
                    if c > 2:
                        print "Forgot your full name?"
                        return False
                    print "That is not your full name!"
                    self.username = raw_input("Please enter your full name: ").strip()
                c = 0
                email = raw_input(self.username + ", please enter your email address: ").strip()
                while (not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email)):
                    c += 1
                    if c > 2:
                        print "Forgot your email address?"
                        return False
                    print "Invalid email"
                    email = raw_input(self.username + ", please enter your email: ").strip()
                c = 0
                accept = raw_input("You accept the license? Please answer with YES or NO followed by pressing the ENTER key: ").strip()
                while (accept.upper() != "YES"):
                    if accept.upper() == "NO":
                        return False
                    c += 1
                    if c > 2:
                        print "You decided to not to agree!"
                        return False
                    email = raw_input("Please answer with YES or NO followed by pressing the ENTER key: ").strip()
            except Exception:
                print "You decided to not to agree!"
                return False
            print "Thank you, "+ self.username +" for accepting!"
            print
        
            config = SafeConfigParser()
            config.read(AppFolders.settings() + '/.ibrew')
        
            try:
                config.add_section('license')
            except Exception:
                pass

            config.set('license', 'accepted', 'true')
            config.set('license', 'name', self.username)
            config.set('license', 'email', email)
            with open(AppFolders.settings() + '/.ibrew', 'w') as f:
                config.write(f)
        else:
            config = SafeConfigParser()
            config.read(AppFolders.settings() + '/.ibrew')
            try:
                self.username =  config.get('license','name')
            except Exception:
                self.username = "NOT ACCEPTED"
        return True
        
    
    def execute(self,line):
    
        try:
            numarg = 0
            if len(line) == 0:
                if self.console:
                    if self.client.connected:
                        self.client.print_short_status()
                    else: print "iBrew: Not connected"
                    return
                else:
                    argument = line
                    command = "help"
            else:
                command = line[0].lower()
                numarg = len(line) - 1
                arguments = line[1:]


            if command == "exit" or command == "quit":
                self.client.run = False
                self.quit = True
                return


            if command != "help" and command != "?" and command != "message" and command != "usage" and command != "commands" and command != "joke" and command != "license" and command != "protocol" and command != "structure" and command != "groups" and command != "group" and command != "notes" and command != "examples" and command != "messages":
                if not self.check_license():
                    return
            
            if command == "dump":
                if numarg == 0 and not self.console:
                    print "iBrew: Do I look like a civet cat to you?"
                    return
                else:
                    if self.client.dump and numarg == 0:
                        self.client.dump = False
                        if self.console:
                            print "iBrew: Dump raw messages disabled"
                    else:
                        self.client.dump = True
                        if self.console:
                            print "iBrew: Dump raw messages enabled"
                    
                    if numarg > 0:
                        command = arguments[0].lower()
                        arguments = arguments[1:]
                        numarg -= 1
                    else:
                        return

            if command == "shout":
                if self.console or numarg == 0:
                    print "iBrew: Can't hear you. Drinking tea at a dinner on the other side of the universe!"
                    return
                if numarg > 0:
                    command = arguments[0].lower()
                    arguments = arguments[1:]
                    numarg -= 1
                if not self.console:
                    self.client.shout      = True
                    self.client.isKettle   = True
                    self.client.isCoffee   = True
                else:
                    print "iBrew: \'shout\' not available in the console"


            if command == "coffee":
                if numarg == 0:
                    print "iBrew: Nah, I want hot chocolade!"
                    return
                if numarg > 0:
                    command = arguments[0].lower()
                    arguments = arguments[1:]
                    numarg -= 1
                #if not self.console:
                self.client.isCoffee   = True
                #else:
                #    print "iBrew: \'coffee\' not available in the console"


            if command == "kettle":
                if numarg == 0:
                
                    sim = ""
                    blubtext = "*blub*"
                    borreltext = "*borrel*"
                    for i in range(1,random.randint(0,42*42)):
                        if random.randint(0,1) == 0:
                            if random.randint(0,4) == 0:
                                sim += " ".rjust(random.randint(0,4)," ") + blubtext.upper()
                            else:
                                sim += " ".rjust(random.randint(0,4)," ") + blubtext

                        else:
                            if random.randint(0,5) == 0:
                                sim += " ".rjust(random.randint(0,4)," ") + borreltext.upper()
                            else:
                                sim += " ".rjust(random.randint(0,4)," ") + borreltext
                    print "iBrew: Starting simulation of boiling water!\n\n" + sim
                    return
                
                if numarg > 0:
                    command = arguments[0].lower()
                    arguments = arguments[1:]
                    numarg -= 1
                #if not self.console:
                self.client.isKettle   = True
                #else:
                #    print "iBrew: \'kettle\' not available in the console"


            if command == "slow":
                if self.console or numarg == 0:
                    print "iBrew: As you command, but it can take a while!"
                    return
                if numarg > 0:
                    command = arguments[0].lower()
                    arguments = arguments[1:]
                    numarg -= 1
                if not self.console:
                    self.client.fast   = False
                else:
                    print "iBrew: \'kettle\' not available in the console"



            if command == "fahrenheid":
                if numarg == 0 and not self.console:
                    print "iBrew: Kelvin, stop that!"
                    return
                else:
                    Smarter.fahrenheid = True
                    if numarg > 0:
                        command = arguments[0].lower()
                        arguments = arguments[1:]
                        numarg -= 1
                    if self.console:
                        print "iBrew: Temperature in fahrenheid"
                        return


            if command == "celsius":
                if numarg == 0 and not self.console:
                    print "iBrew: But i'm freezing and so confused. Please turn me on!"
                    return
                else:
                    Smarter.fahrenheid = False
                    if numarg > 0:
                        command = arguments[0].lower()
                        arguments = arguments[1:]
                        numarg -= 1
                    if self.console:
                        print "iBrew: Temperature in celsius"
                        return

            self.haveHost = False
            
            if numarg > 0:
                if self.is_valid_ipv4_address(arguments[numarg-1]) or self.is_valid_ipv6_address(arguments[numarg-1]):
                    self.client.host = arguments[numarg-1]
                    self.haveHost = True
                    numarg -= 1
                    arguments = arguments[0:numarg]
                    self.client.disconnect()
                    # still wong...
              
            if command == "console" or command == "connect":
                self.client.disconnect()
                
            if command == "disconnect":
                self.client.disconnect()
                return

            if command == "connect" or command == "console" or ((command == "relay" or command == "sweep" or command == "monitor" or command == "web") and not self.console):
                self.app_info()
                self.joke()


            if command == "monitor":
                self.client.fast = False

            if (command == "relay" and not self.console) or ((not self.client.connected or self.haveHost) and command != "help" and command != "?" and command != "list" and command != "message" and command != "usage" and command != "commands" and command != "web" and command != "joke" and command != "license" and command != "protocol" and command != "structure" and command != "notes" and command != "groups" and command != "group" and command != "examples" and command != "messages"):


                if not self.haveHost and command != "relay":
                    devices = self.client.find_devices()
                    if self.client.dump:
                        self.client.print_devices_found(devices)
            
                    if len(devices) == 1:
                        self.client.host = devices[0][0]

                if command == "console" or command == "connect" or command == "relay":
                    self.client.dump_status = False
                    self.client.fast = False
                    self.client.shout = False
                

                try:
                    if not self.client.dump:
                        print
                        print "  Starting please wait..."
                        print
                    if not (self.console and command == "relay"):
                        self.client.connect()
                    
                    
                except Exception, e:
                    logging.debug(e)
                    logging.info("iBrew: Could not connect to [" + self.client.host + "]")
                    if command != "console" and command != "connect" and command != "relay":
                        return
                
                if command == "console" or command == "connect" or command == "relay":
                    self.console = True
                    if numarg == 1:
                        self.client.block(arguments[0])
                    if self.client.dump:
                        self.client.print_rules()
                
            if command == "status":
                self.client.fast = False
                try:
                    self.client.device_all_settings()
                except Exception, e:
                    logging.debug(str(e))
                    logging.debug(traceback.format_exc())
                    print "iBrew: Could not init values"
                    return



            if command == "connect" or command == "console" or ((command == "relay" or command == "sweep" or command == "monitor") and not self.console):
 
                try:
                    self.client.device_all_settings()
                except Exception, e:
                    logging.debug(str(e))
                    logging.debug(traceback.format_exc())
                    print "iBrew: Could not init values"
                    return
                self.client.print_connect_status()
                self.client.print_status()
                
            if command == "console" or command == "connect" or (command == "relay" and not self.console):
                self.intro()
            
            if command == "console" or command == "connect":
                return


            
            if command == "help" or command == "?":
                                            self.usage()
                                            self.commands()
            elif command == "shortstatus":  self.client.print_short_status()
            elif command == "usage":        self.usage()
            elif command == "rules":
                                            if numarg >= 1:
                                                self.client.print_rules()
                                            else:
                                                self.client.print_rules_short()
            elif command == "unblock":      self.client.unblock(arguments[0])
            elif command == "block":        self.client.block(arguments[0])
            elif command == "relay":
                                            if numarg >= 1:
                                                if self.console:
                                                    self.client.relay_stop()
                                                else:
                                                    print "iBrew: If you spin something around and around real fast, it looks like its standing still..."
                                            self.client.relay_start()
                                            return
            
            elif command == "commands":     self.commands()
            elif command == "protocol":     print Smarter.protocol()
            elif command == "structure":    print Smarter.structure()
            elif command == "notes":        print Smarter.notes()
            elif command == "license":
                                            if self.console and numarg == 1 and arguments[0] == "disagree":
                                                os.remove(AppFolders.settings() + '/.ibrew')
                                            else:
                                                print Smarter.license()
            elif command == "examples":     self.examples()
            elif command == "groups":       print Smarter.groups()
            elif command == "messages":
                                            if numarg >= 1 or not self.console:
                                                print Smarter.messages()
                                            else:
                                                print Smarter.messages(self.client.isCoffee,self.client.isKettle)
            elif command == "message":
                                            if numarg >= 1:
                                                print Smarter.message(Smarter.code_to_number(arguments[0]))
                                            else:
                                                print Smarter.message_all()
            elif command == "group":
                                            if numarg >= 1:
                                                s = None
                                                try:
                                                    s = Smarter.group(Smarter.string_to_group(arguments[0]))
                                                except SmarterError:
                                                    print "iBrew: Group not available"
                                                else:
                                                    print s
                                            else:
                                                print Smarter.groups_all()
            elif command == "list":         self.client.print_devices_found(self.client.find_devices())
            elif command == "joke" or command == "quote":
                                            print
                                            self.joke()
                                            print
            elif command == "stats":        self.client.print_stats()
            elif command == "web":
                                            if not self.console:
                                                if numarg == 0:
                                                    self.web()
                                                else:
                                                    self.web(int(arguments[0]))
                                            else:
                                                print "iBrew: Not in console"

            # Kettle
            elif not self.client.connected: return
            elif command == "heat":
                                            if numarg >= 2:
                                                self.client.kettle_heat(Smarter.string_to_temperature(arguments[0]),Smarter.string_to_keepwarm(arguments[1]))
                                            elif numarg == 1:
                                                self.client.kettle_heat(Smarter.string_to_temperature(arguments[0]))
                                            else:
                                                self.client.kettle_heat_default()
                                    
            elif command == "tea":
                                            if numarg == 1:
                                                if arguments[0] == "white":
                                                    self.client.kettle_heat_white_tea()
                                                if arguments[0] == "black":
                                                    self.client.kettle_heat_black_tea()
                                                if arguments[0] == "green":
                                                    self.client.kettle_heat_green_tea()
                                                if arguments[0] == "oelong":
                                                    self.client.kettle_heat_oelong_tea()
                                                
            elif command == "boil":         self.client.kettle_boil()

            elif command == "formula":
                                            if numarg >= 2:
                                                self.client.kettle_formula_heat(Smarter.string_to_temperature(arguments[0]),Smarter.string_to_keepwarm(arguments[1]))
                                            elif numarg == 1:
                                                self.client.kettle_formula_heat(Smarter.string_to_temperature(arguments[0]),self.client.defaultKeepWarmTime)
                                            else:
                                                self.client.kettle_formula_heat_default(self.client.defaultFormulaTemperature,self.client.defaultKeepWarmTime)

            elif command == "default":      self.client.device_restore_default()
            elif command == "calibrate":
                                            if self.client.onBase:
                                                print "Please remove kettle for accurate calibration"
                                            self.client.kettle_calibrate()
            elif command == "base":
                                            if numarg == 0:
                                                self.client.kettle_calibrate_base()
                                                if not self.client.dump: self.client.print_watersensor_base()
                                            if numarg >= 1:
                                                self.client.kettle_calibrate_store_base(Smarter.string_to_watersensor(arguments[0]))
                                                if not self.client.dump: self.client.print_watersensor_base()

            # WiFi
            elif command == "firmware":
                                            self.client.wifi_firmware()
                                            if not self.client.dump: self.client.print_wifi_firmware()
            elif command == "direct":        self.client.wifi_direct()
            elif command == "scan":
                                            self.client.wifi_scan()
                                            if not self.client.dump: self.client.print_wireless_networks()
            elif command == "join":
                                            if numarg >= 1:
                                                password = ""
                                                network = arguments[0]
                                                if numarg >= 2:
                                                    password = arguments[1]
                                                self.client.wifi_join(network,password)
                                            else:
                                                print "iBrew: Need at least a wireless network name"
            elif command == "rejoin":
                                            if self.client.isDirect:
                                                print "iBrew: Can not rejoin if connected directly"
                                            else:
                                                self.client.wifi_rejoin()

            # Coffee
            elif command == "hotplate":
                                            if numarg >= 1:
                                                if arguments[0].lower() == "off":
                                                      self.client.coffee_hotplate_off()
                                                elif arguments[0].lower() == "on":
                                                    if numarg >= 2:
                                                            self.client.coffee_hotplate_on(Smarter.string_to_hotplate(arguments[1]))
                                                    else:
                                                        self.client.coffee_hotplate_on()
                                                else:
                                                    print "iBrew: hotplate missing [on/off] got " + arguments[0]
                                            else:
                                                print "iBrew: hotplate missing [on/off]"
            elif command == "carafe":
                                            if numarg >= 1:
                                                if arguments[0].lower() == "off":
                                                    self.client.coffee_carafe_required_off()
                                                elif arguments[0].lower() == "on":
                                                    self.client.coffee_carafe_required_on()
                                            else:
                                                self.client.coffee_carafe_required()
            elif command == "timers":        self.client.coffee_timers()
            elif command == "timer":
                                            if numarg >= 2:
                                                if arguments[0].lower() == "delete":
                                                    self.client.coffee_timer_disable(Smarter.string_to_number(arguments[1]))
                                                else:
                                                    self.client.coffee_timer_store(Smarter.string_to_number(arguments[1]))
 
                                                print "iBrew: Not yet implemented"
                                            else:
                                                print "iBrew: timer needs index (time or delete)"
            elif command == "mode":
                                            if numarg >= 1:
                                                if arguments[0].lower() == "carafe":
                                                    self.client.coffee_carafe_mode()
                                                elif arguments[0].lower() == "cup":
                                                    self.client.coffee_cup_mode()
                                            else:
                                                self.client.coffee_mode()
            elif command == "beans":
                                            if self.client.grind:
                                                print "iBrew: Beans already selected"
                                            else:
                                                self.client.coffee_beans()
                                                print "iBrew: Beans used"
            elif command == "filter" or command == "pregrind":
                                            if not self.client.grind:
                                                print "iBrew: Filter already selected"
                                            else:
                                                self.client.coffee_filter()
                                                print "iBrew: Filter used"
            elif command == "descaling":
                                            try:
                                                self.client.coffee_descaling()
                                            except Exception:
                                                # no water...?
                                                print "iBrew: Descaling failed"
            elif command == "brew":
                                            if numarg == 0:
                                                self.client.coffee_brew_settings()
                                            elif numarg == 1 and arguments[0].lower() == "default":
                                                self.client.coffee_brew_default()
                                            elif numarg == 1:
                                                self.client.coffee_brew(Smarter.string_to_cups(arguments[0]),self.client.hotPlate,self.client.grind,self.client.strength)
                                            elif numarg == 2:
                                                self.client.coffee_brew(Smarter.string_to_cups(arguments[0]),Smarter.string_to_hotplate(arguments[1]),self.client.grind,self.client.strength)
                                            elif numarg == 3:
                                                self.client.coffee_brew(Smarter.string_to_cups(arguments[0]),Smarter.string_to_hotplate(arguments[1]),Smarter.string_to_grind(arguments[2]),self.client.strength)
                                            elif numarg >= 4:
                                                self.client.coffee_brew(Smarter.string_to_cups(arguments[0]),Smarter.string_to_hotplate(arguments[1]),Smarter.string_to_grind(arguments[2]),Smarter.string_to_strength(arguments[3]))
            elif command == "strength":
                                            if numarg == 0:
                                                print "iBrew: specify strength [weak,medium,strong]"
                                            elif numarg >= 1:
                                                self.client.coffee_strength(Smarter.string_to_strength(arguments[0]))
            elif command == "weak":         self.client.coffee_weak()
            elif command == "medium":       self.client.coffee_medium()
            elif command == "strong":       self.client.coffee_strong()
            elif command == "cups":
                                            if numarg == 0:
                                                print "iBrew: specify cups [1..12]"
                                            elif numarg >= 1:
                                                self.client.coffee_cups(Smarter.string_to_cups(arguments[0]))

              # Console Commands
            elif command == "monitor":      self.monitor()
            elif command == "sweep":
                                            if numarg >= 1:
                                                 self.sweep(Smarter.code_to_number(arguments[0]))
                                            else:
                                                self.sweep()
            elif command == "settings":     # FAST fix need device... could default...
                                            if numarg == 0:
                                                self.client.device_settings()
                                                if not self.client.dump: self.client.print_settings()
                                            elif numarg == 0: print "iBrew: Could not store coffee settings, missing all arguments"
                                            elif numarg == 1 and self.client.isCoffee: print "iBrew: Could not store coffee settings, missing cups"
                                            elif numarg == 2 and self.client.isCoffee: print "iBrew: Could not store coffee settings, missing grinder"
                                            elif numarg == 3 and self.client.isCoffee: print "iBrew: Could not store coffee settings, missing hotplate"
                                            elif numarg == 1 and self.client.isKettle: print "iBrew: Could not store kettle settings, missing temperature"
                                            elif numarg == 2 and self.client.isKettle: print "iBrew: Could not store kettle settings, missing formula mode"
                                            elif numarg == 3 and self.client.isKettle: print "iBrew: Could not store kettle settings, missing formula temperature"
                                            elif numarg >= 4:
                                                self.client.device_store_settings(arguments[0],arguments[1],arguments[2],arguments[3])
                                                if not self.client.dump: self.client.print_settings()
            elif command == "stop" or command == "off":
                                            #if numarg == 0:
                                            self.client.device_stop()
                                            #else:
                                            #    if arguments[0].lower() == "kettle":
                                            #        self.client.kettle_stop()
                                            #    elif arguments[0].lower() == "coffee":
                                            #        self.client.coffee_stop()
                                            #    else:
                                            #        self.client.device_stop()
                                        
            elif command == "on" or command == "start":
                                            #if numarg == 0:
                                            self.client.device_start()
                                            #else:
                                            #    if arguments[0].lower() == "kettle":
                                            #        self.client.kettle_heat()
                                            #    elif arguments[0].lower() == "coffee":
                                            #        self.client.coffee_brew_settings()
                                            #    else:
                                            #        self.client.device_start()
                                                    

            elif command == "reset":        self.client.device_reset()
            elif command == "info":
                                            self.client.device_info()
                                            if not self.client.dump: self.client.print_info_device()
            elif command == "history":
                                            self.client.device_history()
                                            if not self.client.dump: self.client.print_history()
            elif command == "time":
                                            print "not yet implemented"
                                            self.client.device_time()
            
            elif command == "status":       self.client.print_status()
            else:
                                            try:
                                                self.client.device_raw(command+''.join(arguments))
                                            except Exception:
                                                print "iBrew: Sending raw command message failed"
        except Exception,e:
            if not self.console:
                self.quit = True
            print str(e)
            print(traceback.format_exc())
            print "iBrew: Command Failed"
            
       
    def run(self,arguments):
        AppFolders.makeFolders()

        #Configure logging
        # root level        
        logger = logging.getLogger()    
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        log_file = os.path.join(AppFolders.logs(), "iBrewConsole.log")
        
        fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=1048576, backupCount=4, encoding="UTF8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
        # By default only do info level to console
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)
        sh.setFormatter(formatter)
        logger.addHandler(sh)


        sh.setLevel(logging.DEBUG)
        
        self.console = False
        self.quit = True
        self.client = SmarterClient()
        
        self.client.settingsPath = AppFolders.settings() + "/"
        self.client.fast = True
        try:
            self.execute(arguments)
        except Exception:
            self.console = False
    
        if self.console:
            self.quit = False
            
        while not self.quit:
            try:
                cursor = self.client.host + ":" + self.client.device + "$"
                self.execute(raw_input(cursor).strip().split())
            except KeyboardInterrupt:
                self.quit = True
            except Exception, e:
                self.quit = True
                logging.debug(traceback.format_exc())
                logging.debug(str(e))
        self.client.disconnect()
     
                     
#------------------------------------------------------
# iBrew Console PRINT
#------------------------------------------------------

    def app_info(self):
        print iBrewApp
        print iBrewInfo
        if self.username != "NOT ACCEPTED":
            print "iBrew: LICENSING AGREEMENT accepted by LICENSEE " + self.username
        print
        print iBrewContribute
        print

    def intro(self):
        print
        print "For list of commands type: help and press enter"
        print "Press enter for status update and press ctrl-c to quit"
        print

    def joke(self):
        joke = iBrewJokes().joke()
        if self.client is not None:
            if self.client.isCoffee:
                joke = iBrewJokes().coffee()
            elif self.client.isKettle:
                joke = iBrewJokes().kettle()
        print "\n      \'" + joke[0] + "\'\n                  -- " + joke[1] + "\n"


    def usage(self):
        print
        print "  iBrew Web Server"
        print
        print "  Usage: ibrew (energy) (dump) (fahrenheid) web (port) (rules) (modifiers) (host)"
        print
        print "    energy                 energy saver (stats not possible)"
        print "    dump                   dump message enabled"
        print "    fahrenheid             use fahrenheid"
        print "    web                    start web interface & rest api"
        print "    port                   optional port number, default 2082"
        print "    rules                  blocking rules"
        print "    modifiers              patches"
        print "    host                   host address of device (format: ip4, ip6, fqdn)"
        print
        print
        print "  iBrew Command Line"
        print
        print "  Usage: ibrew (energy) (dump) (shout|slow) (coffee|kettle) (fahrenheid) [command] (host)"
        print
        print "    dump                   dump message enabled"
        print "    energy                 NOT IMPLEMENTED energy saver (stats not possible)"
        print "    shout                  sends commands and quits not waiting for a reply"
        print "    slow                   fully inits everything before action"
        print "    coffee                 assumes coffee machine"
        print "    kettle                 assumes kettle"
        print "    fahrenheid             PARTLY WORKING use fahrenheid"
        print "    command                action to take!"
        print "    host                   host address of device (format: ip4, ip6, fqdn)"
        print
        print "  If you do not supply a host, it will try to connect to the first detected device"
        print "  Thus if you have more then one device supply a host (if its not in direct mode)"
        print

    def commands(self):
        print
        print "  iKettle 2.0 & Smarter Coffee  Commands"
        print "    default                set default settings"
        print "    info                   device info"
        print "    list                   list detected devices"
        print "    reset                  reset device to default"
        print "    shortstatus            show status"
        print "    start                  start the device"
        print "    status                 show full status"
        print "    settings               show user settings"
        print "    stop                   stop the appliance"
        print
        print "  iKettle 2.0 Commands"
        print "    base                   show watersensor base value"
        print "    base [base]            store watersensor base value"
        print "    boil                   heat till 100°C (coffee level)"
        print "    calibrate              calibrates watersensor"
        print "    celsius                use celsius °C [console only]"
        print "    fahrenheid             use fahrenheid °F [console only]"
        print "    formula (temperature (keepwarm))] heat kettle in formula mode"
        print "    heat (temperature)(keepwarm))    heat kettle"
        print "    settings [temperature] [keepwarm] [formula] [formulatemperature] store kettle user settings"
        print "    tea [white,green,black,oelong] warms water for tea"
        print
        print "  Smarter Coffee  Commands"
        print "    beans                  use beans for coffee"
        print "    brew (cups (hotplate (grind (strength)))) brew coffee"
        print "    brew default           brew coffee with default settings"
        print "    carafe                 returns if carafe is required"
        print "    carafe [state]         set carafe is required [on or off]"
        print "    cups [number]          set number of cups [1..12]"
        print "    descaling              descale coffee machine"
        print "    filter                 use pregrind beans in filter for coffee"
        print "    hotplate off           turn hotplate off"
        
        # VERAMDER DEZE FIX (ON MAG WEG)
        print "    hotplate on (minutes)  turn hotplate on (time in minutes)"
        print "    mode                   return which mode: cup or carafe mode"
        print "    mode [mode]            set mode: [cup] or [carafe] mode"
        print "    pregrind               use pregrind beans in filter for coffee"
        print "    (strength) [strength]  set strength coffee [weak, medium or strong]"
        print "    settings [cups] [hotplate] [grind] [strength] store user settings"
        print
        print "  Wireless Network Commands"
        print "    direct                 enable direct mode access"
        print "    join [net] [pass]      connect to wireless network"
        print "    rejoin                 rejoins current wireless network [not in direct mode]"
        print "    scan                   scan wireless networks"
        print
        print "  Smarter Network Commands [console only]"
        print "    connect (host) (rules&modifiers) connect to device"
        print "    block [rules]          block messages with groups or ids"
        print "    disconnect             disconnect connected device"
        print "    unblock [rules]        unblock messages groups or ids"
        print "    relay (port)           start relay device"
        print "    relay stop             stop relay device"
        print "    rules (full)           show blocking rules"
        print "    stats                  show traffic statistics"
        print
        print "  Block Rules"
        print "    Consists of rules, in: is for outgoing connection to the device, out: is for incomming connection from relay client."
        print
        print "    [in:|out:]rule(,[in:|out:]rule)*"
        print
        print "    rule:"
        print "      message id"
        print "      group name"
        print
        print "  Debug Commands"
        print "    time [time]            set the device time"
        print "    firmware               show firmware Wifi"
        print "    history                action history"
        print "    [hexdata]              send raw data to device (e.g. \'64 7e\')"
        print "    dump                   toggle \'dump raw messages\'"
        print "    monitor                monitor incomming traffic"
        print "    modify (modifiers)     patch or unpatch messages"
        print "    sweep (id)             [developer only] try (all or start with id) unknown command codes"
        print
        
        
        print "  NOT IMPLEMENTED Modifiers Rules"
        print "    [in:|out:]var=(value)(,[in:|out:]var=(value))*"
        print
        print "    VAR           VALUE"
        print "    version       [00..FF]               override device firmware version"
        print "    heater        disable                coffee machine or kettle heater disabled"
        print
        print "    base          [00..4000]             override default calibration base"
        print "    formula       [0..100]               override default formula temperature"
        print "    temperature   [0..100]               override default temperature"
        print "    keepwarm      off or [5..?]          override default keepwarm time"
        print "    formula       disable/enabled        override formula mode"
        print
        print "    carafe        optional or required   override carafe detection"
        print "    cups          [1..12]                override default number of cups"
        print "    grind         beans or filter        override default grind"
        print "    hotplate      off or [5..?]          override default hotplate time"
        print "    mode          carafe or cup          override mode"
        print "    strength      weak, medium or strong override default strength"
        print "    water                                correct cups according to water level"
        print "    limit         [1..12]                limit the number of cups to be selected"
        print "    grinder       disable                force use of filter"
        print "    hotplate      disable                coffee machine hotplate disabled"
        print "    child         lock                   kettle can not heat above 45 degrees"
        print
        print "    if no value it clears the patch"
        print
        print "  NOT IMPLEMENTED Debug Coffee Timer"
        print "    timer [index] (erase|[time]) set/erase timer"
        print "    timers                 show timers"
        print
        
        print "  Help Commands"
        print "    examples               show examples of commands"
        print "    groups                 show all groups"
        print "    group                  show messages in group"
        print "    messages               show all known protocol messages"
        print "    message [id]           show protocol message detail of message [id]"
        print "    notes                  show developer notes on the devices"
        print "    protocol               show all protocol information available"
        print "    structure              show protocol structure information"
        print
        print "  iBrew Commands"
        print "    console (rules) (modifiers) start console [command line only]"
        print "    joke                   show joke"
        print "    license                show license"
        print "    license disagree       stop using license [command line only]"
        print "    quit                   quit console [console only]"
        print


    def examples(self):
        print
        print "  Example command line:"
        print "    ibrew shout 21 30 05 7e  Send kettle raw heat without waiting for reply"
        print "    ibrew weak 10.0.0.1      Set coffee strength to weak"
        print "    ibrew strength weak      Set coffee strength to weak but do not toggle filter/beans"
        print "    ibrew dump coffee relay out:coffee Simulates coffee machine messages"
        print
        print "  Example console:"
        print "    off                      Stop heating/brewing"
        print "    messages                 Show all protocol messages"
        print "    message 3e               Show protocol message 3a, turn hotplate on"
        print "    167E                     Send kettle raw stop"
        print "    21 30 05 7e              Send kettle raw heat"
        print "    weak                     Set coffee strength to weak"
        print "    strength weak            Set coffee strength to weak but do not toggle filter/beans"
        print "    cups 3                   Set number of cups to brew"
        print "    mode cup                 Set cup mode"
        print "    block in:wifi,in:02          Block wifi and [" + Smarter.message_description(02) + "] command to device"
        print "    patch relay out:version=12] Patches [" + Smarter.message_description(Smarter.ResponseDeviceInfo) + "] Argument version to clients"
        print "    brew 4 10 beans strong   Brew 4 cups of strong coffee using the beans keeping the hotplate on for 10 minutes"
        print "    join MyWifi p@ssw0rd     Joins MyWifi wireless network using p@ssw0rd as credential"
        print "    settings 100 20 True 75  Set default user settings for the kettle to..."
        print

