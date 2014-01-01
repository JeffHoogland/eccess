import os
import sys
import elementary
import ecore
import evas
import time
import dateutil.tz as dtz
import pytz
import datetime as dt
import collections
import esudo


def getTimeZones():
    result=collections.defaultdict(list)
    for name in pytz.common_timezones:
        timezone=dtz.gettz(name)
        now=dt.datetime.now(timezone)
        offset=now.strftime('%z')
        abbrev=now.strftime('%Z')
        result[offset].append(name)
        result[abbrev].append(name)    
    return result

def searchList(text, lst):
    for item in lst:
        if text.lower() in item.lower()[:len(text)]:
            return lst.index(item)
    return 0

class TimeManager(elementary.Box):
    def __init__(self, parent):
        elementary.Box.__init__(self, parent.mainWindow)
        self.win = win = parent.mainWindow
        self.rent = parent
        self.timezones = getTimeZones()
        self.zones = []
        self.zoneitems = False

        cframe = elementary.Frame(win)
        cframe.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        cframe.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        #cframe.size_hint_align = (-1.0, 0.0)
        cframe.text = "Current Time"
        cframe.show()

        clock = elementary.Clock(win)
        clock.show_seconds_set(True)
        clock.show_am_pm_set(True)
        clock.show()

        cframe.content = clock

        bt = elementary.Button(win)
        bt.text_set("Edit")
        bt.callback_clicked_add(self.edit_time)
        bt.show()

        clockbox = elementary.Box(win)
        clockbox.horizontal = True
        clockbox.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        clockbox.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        clockbox.pack_end(cframe)
        clockbox.pack_end(bt)
        clockbox.show()

        self.tzframe = tzframe = elementary.Frame(win)
        tzframe.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        tzframe.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        tzframe.text = "Current Timezone"
        tzframe.show()

        self.zone = zone = elementary.Label(win)
        zone.text = "<b>%s</b>"%time.tzname[0]
        zone.show()

        tzframe.content = zone

        bt = elementary.Button(win)
        bt.text_set("Edit")
        bt.callback_clicked_add(self.edit_timezone)
        bt.show()

        tzbox = elementary.Box(win)
        tzbox.horizontal = True
        tzbox.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        tzbox.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        tzbox.pack_end(tzframe)
        tzbox.pack_end(bt)
        tzbox.show()

        inet = elementary.Button(win)
        inet.text = "Sync Time from Internet"
        inet.callback_clicked_add(self.time_from_internet)
        inet.show()        

        bck = elementary.Button(win)
        bck.text = "Back"
        bck.callback_clicked_add(lambda x: parent.nf.item_pop())
        bck.show()

        bbox = elementary.Box(win)
        bbox.horizontal = True
        bbox.pack_end(inet)
        bbox.pack_end(bck)
        bbox.show()

        self.pack_end(clockbox)
        self.pack_end(tzbox)
        self.pack_end(bbox)

    def time_from_internet( self, bt ):
        self.run_command(False, False, 'ntpdate pool.ntp.org')

    def edit_time( self, bt ):
        print "In the edit time call back"
        clock = elementary.Clock(self.win)
        clock.show_seconds_set(True)
        clock.show_am_pm_set(True)
        clock.edit_set(True)
        clock.show()

        bbox = elementary.Box(self.win)
        bbox.horizontal = True

        chng = elementary.Button(self.win)
        chng.text = "Change"
        chng.callback_clicked_add(lambda x: self.rent.nf.item_pop())
        chng.callback_clicked_add(self.change_time, clock)
        chng.show()

        bck = elementary.Button(self.win)
        bck.text = "Cancel"
        bck.callback_clicked_add(lambda x: self.rent.nf.item_pop())
        bck.show()
        bbox.pack_end(chng)
        bbox.pack_end(bck)
        bbox.show()

        box = elementary.Box(self.win)
        box.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        box.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        box.pack_end(clock)
        box.pack_end(bbox)
        box.show()

        self.rent.nf.item_simple_push(box)

    def change_time( self, bt, clock):
        print "In the change time function"
        times = list(clock.time_get())
        for x in times:
            if x < 10:
                times[times.index(x)] = "0%s"%x
        self.run_command(False, False, 'changetime.sh %s %s %s'%(times[0], times[1], times[2]))

    def edit_timezone( self, bt):
        print "In the edit time zone call back"

        zonelist = elementary.List(self.win)
        zonelist.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        zonelist.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        self.zones = []
        for tz in self.timezones:
            for each in self.timezones[tz]:
                if each not in self.zones:
                    self.zones.append(each)
        self.zones.sort()
        for zone in self.zones:
            zonelist.item_append(zone)
        zonelist.show()
        self.zoneitems = zonelist.items_get()

        sframe = elementary.Frame(self.win)
        sframe.text = "Search"
        sframe.size_hint_weight = (1.0, 0.0)
        sframe.size_hint_align = (-1.0, 0.0)
        search = elementary.Entry(self.win)
        search.single_line = True
        search.size_hint_weight = (1.0, 0.0)
        search.size_hint_align = (-1.0, 0.0)
        search.callback_changed_add(self.search_change)
        sframe.content = search
        search.show()
        sframe.show()

        bbox = elementary.Box(self.win)
        bbox.horizontal = True

        chng = elementary.Button(self.win)
        chng.text = "Change"
        chng.callback_clicked_add(lambda x: self.rent.nf.item_pop())
        chng.callback_clicked_add(self.change_timezone, zonelist)
        chng.show()

        bck = elementary.Button(self.win)
        bck.text = "Cancel"
        bck.callback_clicked_add(lambda x: self.rent.nf.item_pop())
        bck.show()
        bbox.pack_end(chng)
        bbox.pack_end(bck)
        bbox.show()

        box = elementary.Box(self.win)
        box.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        box.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        box.pack_end(zonelist)
        box.pack_end(sframe)
        box.pack_end(bbox)
        box.show()

        self.rent.nf.item_simple_push(box)
        search.focus = True

    def search_change( self, entry ):
        print entry.text
        zeindex = searchList(entry.text, self.zones)
        self.zoneitems[zeindex].selected_set(True)
        self.zoneitems[zeindex].bring_in()
        print self.zones[zeindex]

    def change_timezone( self, bt, zones ):
        print "Changing time zone to %s"%zones.selected_item_get().text
        self.run_command(False, False, 'cp -f /usr/share/zoneinfo/%s /etc/localtime'%zones.selected_item_get().text)
        self.zone.text = zones.selected_item_get().text

    def run_command(self, bnt, window, command):
        if window:
            window.hide()
        cmd = esudo.eSudo(command, self.win)
