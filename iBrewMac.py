# -*- coding: utf8 -*-

import rumps

#from PyObjCTools import AppHelper

import webbrowser

rumps.debug_mode(False)  # turn on command line logging information for development - default is off

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

