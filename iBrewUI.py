#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import platform
import signal

import logging
import logging.handlers

from iBrewFolders import AppFolders
#why was it console and it worked?
from iBrewWeb import *

class Launcher():    
    def signal_handler(self, signal, frame):
        print "Caught Ctrl-C.  exiting."
        if self.apiServer:
            self.web.kill()
        sys.exit()
    
    def run(self):
        
        try:
            self.web.run(2080,True)
        except Exception, e:
            logging.debug(e)
            logging.info("iBrew: Failed to run Web Interface & REST API on port 2080")
            return
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
                except:
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

        signal.signal(signal.SIGINT, self.signal_handler)
        import threading
        t = threading.Thread(target=self.run)
        t.start()
        logging.info("GUI Started")
        if platform.system() == "Darwin":
            from iBrewWin import MacGui
            MacGui(self.web).run()
        elif platform.system() == "Windows":
            from iBrewWin import WinGui
            WinGui(self.web).run()
        else:
            print "MacOS & Windows only"

Launcher().go()

