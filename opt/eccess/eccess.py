"""A tool written in Python and Elementary to provide a GUI for configuring Unix users and groups"""

import elementary
import evas

#Import our internal parts
from optionsWindow import *
from UserManager import *
from TimeManager import *
from TaskManager import *
from ScreenSetup import *

class Eccess(object):
    def __init__( self ):
        self.mainWindow = elementary.StandardWindow("eCcess", "eCcess - System Tool")
        self.mainWindow.callback_delete_request_add(lambda o: elementary.exit())
        self.nf = elementary.Naviframe(self.mainWindow)
        self.nf.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        self.nf.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        #self.scroller = elementary.Scroller(self.mainWindow)
        #self.scroller.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_FILL)
        #self.scroller.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        #self.scroller.content_set(self.nf)
        #self.scroller.policy_set(0, 1)
        self.nf.show()
        self.mainWindow.resize_object_add(self.nf)
        #self.scroller.show()

    def launch( self, launchto=False ):
        self.mainWindow.resize(800, 400)
        self.mainWindow.show()
        self.options_spawn()
        if launchto == "users":
            self.users_groups_spawn()
        elif launchto == "time":
            self.time_date_spawn()
        elif launchto == "taskmanager":
            self.task_manager_spawn()

    def options_spawn( self, bt=False ):
        self.nf.item_simple_push(optionsWindow(self))

    def users_groups_spawn( self, bt=False ):
        print "Users and groups CB"
        self.nf.item_simple_push(UserManager(self))

    def time_date_spawn( self, bt=False ):
        print "Times and date CB"
        self.nf.item_simple_push(TimeManager(self))

    def task_manager_spawn( self, bt=False ):
        print "Task manager CB"
        self.nf.item_simple_push(TaskManager(self))

    def screen_setup_spawn( self, bt=False ):
        print "Screen setup CB"
        self.nf.item_simple_push(ScreenSetup(self))

if __name__ == "__main__":
    elementary.init()
    GUI = Eccess()
    if len(sys.argv) == 1:
        GUI.launch()
    else:
        GUI.launch(sys.argv[1])
    elementary.run()    
    elementary.shutdown()
