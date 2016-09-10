#!/usr/bin/env python

import sys
import platform
import signal

import rumps
import logging
import logging.handlers
import time
from PyObjCTools import AppHelper
import webbrowser
import os
import sys
from iBrewFolders import AppFolders

rumps.debug_mode(True)  # turn on command line logging information for development - default is off

class MacGui(rumps.App):
    def __init__(self, apiServer):
        super(MacGui, self).__init__("iBrew", icon=AppFolders.appBase() + "/web/static/icons/logo.png", quit_button=None)
        self.apiServer = apiServer
        self.menu = [
            'iBrew Web Interface',
            None
        ]         

    @rumps.clicked("iBrew Web Interface")
    def web(self, sender):
        webbrowser.open("http://localhost:{0}".format(2080), new=0)

    @rumps.clicked("Quit")
    def quit(self, sender):
        if self.apiServer:
            self.apiServer.kill()
        #AppHelper.stopEventLoop()
        rumps.quit_application()
        sys.exit()
    
    @rumps.notifications
    def notifications(self, notification):  # function that reacts to incoming notification dicts
        print notification
    
    def onebitcallback(self, sender):  # functions don't have to be decorated to serve as callbacks for buttons
        print 4848484            # this function is specified as a callback when creating a MenuItem below


from iBrewConsole import *

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
        if platform.system() != "Darwin":
            print "iBrew: MacOS Only"
            return
        
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
            MacGui(self.web).run()
        else:
            print "MacOS Only"

Launcher().go()

