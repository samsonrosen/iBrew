#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import platform
import signal

import rumps

import logging
import logging.handlers

from iBrewFolders import AppFolders
from iBrewWeb import *

#------------------------------------------------------
# iBrew
#
# Taskbar Launcher (MacOS & Windows)
#
# https://github.com/Tristan79/iBrew
#
# Copyright © 2016 Tristan (@monkeycat.nl)
#
# Intermezzo
#------------------------------------------------------

class Launcher():    
    def signal_handler(self, signal, frame):
        print "Caught Ctrl-C.  exiting."
        if self.web:
            self.web.kill()
        sys.exit(-1)
    
    def __init__(self):
        self.ui = None

    def exit(self):
        sys.exit()
        os.exit()

    def run(self):
        
        try:
            self.web.run(2080,True)
        except Exception, e:
            logging.debug(e)
            logging.info("iBrew: Failed to run Web Interface & REST API on port 2080")
            self.web.kill()
            if self.ui:
                self.ui.quit_application()
            print "I never ever had problems not exiting before, fucking python... why not exit?"
            self.exit()
            
        logging.info("iBrew: Starting Web Interface & REST API on port 2080")
    
    def go(self):
        #if platform.system() != "Darwin":
        #    print "iBrew: MacOS Only"
        #    return
        
        AppFolders.makeFolders()
        
        if platform.system() == "Darwin" or platform.system() == "Linux":
            if getattr(sys, 'frozen', None):
                try:
                    # do not touch if its not a symlink...
                    if os.path.islink("/usr/local/bin/ibrew"):
                        os.remove("/usr/local/bin/ibrew")
                        os.symlink(AppFolders.appBase()+"/iBrewConsole","/usr/local/bin/ibrew")
                except Exception:
                    pass
   
        logger = logging.getLogger()    
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        log_file = os.path.join(AppFolders.logs(), "iBrewWeb.log")
        
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
    
        self.web = iBrewWeb()

        #signal.signal(signal.SIGINT, self.signal_handler)
        #import threading
        self.t = threading.Thread(target=self.run)
        self.t.start()
        logging.info("GUI Started")
        try:
            if platform.system() == "Darwin":
                from iBrewMac import MacGui
                self.ui = MacGui(self.web)
                self.ui.run()
            elif platform.system() == "Windows":
                from iBrewWin import WinGui
                self.ui = WinGui(self.web)
                self.ui.run()
            else:
                print "MacOS & Windows only"
        except Exception:
            if self.ui:
                self.ui.quit_application()
            self.web.kill()

Launcher().go()

