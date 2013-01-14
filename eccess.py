"""A tool written in Python and Elementary to provide a GUI for configuring Unix users and groups"""

import os
import sys
import elementary
import edje
import ecore
import evas
import emotion
import time
import pwd
import grp
import dateutil.tz as dtz
import pytz
import datetime as dt
import collections

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

class Eccess:

    def __init__( self ):
        self.mainWindow = elementary.StandardWindow("mainwindow", "eCcess - System Tool")
        box = elementary.Box(self.mainWindow)
        box.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        box.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        self.nf = elementary.Naviframe(self.mainWindow)
        self.nf.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        self.nf.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        self.scroller = elementary.Scroller(self.mainWindow)
        self.scroller.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        self.scroller.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        box.pack_end(self.scroller)
        box.show()
        self.mainWindow.resize_object_add(box)
        self.scroller.content_set(self.nf)
        self.scroller.policy_set(0, 1)
        self.scroller.show()
        self.nf.show()

    def users_groups( self, bt ):
        print "Users and groups CB"
        self.nf.item_simple_push(UserManager(self))

    def time_date( self, bt ):
        print "Times and date CB"
        self.nf.item_simple_push(TimeManager(self))

    def launch( self, obj ):
        if obj is None:
            self.mainWindow.callback_delete_request_add(lambda o: elementary.exit())

        tb = elementary.Table(self.mainWindow)
        self.nf.item_simple_push(tb)
        #tb.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        tb.show()

        bt = elementary.Label(self.mainWindow)
        bt.text_set("<div align='center'><b>Select an Option:</b></div>")
        bt.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        bt.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        tb.pack(bt, 0, 0, 1, 1)
        bt.show()

        bt = elementary.Button(self.mainWindow)
        bt.text_set("Users and Groups")
        bt.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        bt.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        bt.callback_clicked_add(self.users_groups)
        tb.pack(bt, 1, 0, 1, 1)
        bt.show()

        bt = elementary.Button(self.mainWindow)
        bt.text_set("Time and Date")
        bt.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        bt.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        bt.callback_clicked_add(self.time_date)
        tb.pack(bt, 1, 1, 1, 1)
        bt.show()

        self.mainWindow.resize(800, 300)
        self.mainWindow.show()

class TimeManager(elementary.Box):
    def __init__(self, parent):
        elementary.Box.__init__(self, parent.mainWindow)
        self.win = win = parent.mainWindow
        self.rent = parent
        self.timezones = getTimeZones()

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
        #bt.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        #bt.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
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
        #bt.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        #bt.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        bt.callback_clicked_add(self.edit_timezone)
        bt.show()

        tzbox = elementary.Box(win)
        tzbox.horizontal = True
        tzbox.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        tzbox.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        tzbox.pack_end(tzframe)
        tzbox.pack_end(bt)
        tzbox.show()

        bck = elementary.Button(win)
        bck.text = "Back"
        bck.callback_clicked_add(lambda x: parent.nf.item_pop())
        bck.show()

        self.pack_end(clockbox)
        self.pack_end(tzbox)
        self.pack_end(bck)
        self.show()

    def edit_time( self, bt ):
        print "In the edit time call back"

    def edit_timezone( self, bt):
        print "In the edit time zone call back"

        zonelist = elementary.List(self.win)
        zonelist.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        zonelist.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        tmplist = []
        for tz in self.timezones:
            for each in self.timezones[tz]:
                if each not in tmplist:
                    tmplist.append(each)
        tmplist.sort()
        for zone in tmplist:
            zonelist.item_append(zone)
        zonelist.show()

        bbox = elementary.Box(self.win)
        bbox.horizontal = True
        #bbox.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        #bbox.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)

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
        box.pack_end(bbox)
        box.show()

        self.rent.nf.item_simple_push(box)

    def change_timezone( self, bt, zones ):
        print "Changing time zone to %s"%zones.selected_item_get().text
        self.run_command(False, False, "gksudo 'sudo cp -f /usr/share/zoneinfo/%s /etc/localtime'"%zones.selected_item_get().text)
        self.zone.text = zones.selected_item_get().text

    def run_command(self, bnt, window, command):
        if window:
            window.hide()
        cmd = ecore.Exe(command)
        #cmd.on_del_event_add(self.refreshInterface)

class UserListClass(elementary.GenlistItemClass):
    def text_get(self, genlist, part, data):
        return data.pw_name

class GroupListClass(elementary.GenlistItemClass):
    def text_get(self, genlist, part, data):
        return data.gr_name

class UserManager(elementary.Flip):
    def __init__(self, parent):
        elementary.Flip.__init__(self, parent.mainWindow)

        self.rent = parent
        self.win = parent.mainWindow
        self.userlist = pwd.getpwall()
        self.grouplist = grp.getgrall()

        ulist = self.ulist = elementary.Genlist(self.win)
        glist = self.glist = elementary.Genlist(self.win)

        users = self.users = Users(self)
        groups = self.groups = Groups(self)

        self.part_content_set("front", users)
        self.part_content_set("back", groups)
        self.show()

        self.populate_users()
        self.populate_groups()

    def populate_users(self, *args):
        self.ulist.clear()
        for entry in self.userlist:
            if not self.show_system_users.state:
                if entry.pw_uid >= 1000 and entry.pw_uid < 65534:
                    self.ulist.item_append(UserListClass(), entry, None, 0, None)
            else:
                self.ulist.item_append(UserListClass(), entry, None, 0, None)

    def populate_groups(self, *args):
        self.glist.clear()
        for entry in self.grouplist:
            self.glist.item_append(GroupListClass(), entry, None, 0, None)

    def user_activated(self, item, genlist, data):
        cp = elementary.Ctxpopup(self.win)
        cp.item_append("Information", None, self.usermod, genlist.data)
        cp.item_append("Change Password", None, self.passwordchange, genlist.data)
        cp.item_append("Delete", None, self.userdel, genlist.data)
        pos = self.win.evas.pointer_canvas_xy_get()
        cp.pos = pos
        cp.show()

    def group_activated(self, item, genlist, data):
        cp = elementary.Ctxpopup(self.win)
        cp.item_append("Information", None, self.groupmod, genlist.data)
        cp.item_append("Delete", None, self.groupdel, genlist.data)
        pos = self.win.evas.pointer_canvas_xy_get()
        cp.pos = pos
        cp.show()

    def add(self, btn, data):
        print(btn, data)

    def add_user(self, btn=False, data=False):
        self.win.title = "eCcess - Create User"
        
        lbl1 = elementary.Label(self.win)
        lbl1.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        lbl1.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        lbl1.text = "Username:"
        lbl1.show()

        lbl2 = elementary.Label(self.win)
        lbl2.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        lbl2.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        lbl2.text = "Password:"
        lbl2.show()

        lbl3 = elementary.Label(self.win)
        lbl3.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        lbl3.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        lbl3.text = "Confirm Password:"
        lbl3.show()

        entry1 = elementary.Entry(self.win)
        entry1.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        entry1.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        entry1.single_line = True
        entry1.show()

        entry2 = elementary.Entry(self.win)
        entry2.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        entry2.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        entry2.single_line = True
        entry2.password = True
        entry2.show()

        entry3 = elementary.Entry(self.win)
        entry3.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        entry3.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        entry3.single_line = True
        entry3.password = True
        entry3.show()

        ok = elementary.Button(self.win)
        ok.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        ok.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        ok.text = "Create User"
        ok.callback_pressed_add(self.create_user, entry1, entry2, entry3)
        ok.show()

        nvm = elementary.Button(self.win)
        nvm.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        nvm.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        nvm.text = "Cancel"
        nvm.callback_pressed_add(lambda x: self.rent.nf.item_pop())
        nvm.show()

        bbox = elementary.Box(self.win)
        bbox.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        bbox.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        bbox.horizontal = True
        bbox.pack_end(ok)
        bbox.pack_end(nvm)
        bbox.show()

        box = elementary.Box(self.win)
        box.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        box.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        box.pack_end(lbl1)
        box.pack_end(entry1)
        box.pack_end(lbl2)
        box.pack_end(entry2)
        box.pack_end(lbl3)
        box.pack_end(entry3)
        box.pack_end(bbox)
        box.show()

        self.rent.nf.item_simple_push(box)

    def create_user(self, bnt, username, passwd1, passwd2):
        print "%s %s %s"%(username.text, passwd1.text, passwd2.text)
        self.rent.nf.item_pop()
        if passwd1.text == passwd2.text:
            self.run_command(False, False, "gksudo 'useradd %s -m -p %s'"%(username.text, passwd1.text))
        else:
            self.popup_message("The entered passwords do not match. Please try again.", "eCcess - Password Mismatch", self.add_user)

    def flip_page(self, btn, data):
        self.go(elementary.ELM_FLIP_CUBE_RIGHT)

    def usermod(self, l, i, user):
        cp = i.widget_get()
        cp.dismiss()
        self.users.item_simple_push(UserForm(self, user))

    def passwordchange(self, l, i, user):
        cp = i.widget_get()
        cp.dismiss()
        self.users.item_simple_push(PasswordForm(self, user))

    def userdel(self, l, i, user):
        cp = i.widget_get()
        cp.dismiss()
        print user[0]
        self.confirm("Are you sure you want to delete the user '%s'"%user[0], "gksudo 'userdel %s'"%user[0])

    def popup_message(self, message, title, callback=False):
        popup = elementary.StandardWindow("popup", "%s"%title)

        lbl = elementary.Label(popup)
        lbl.text = message
        lbl.show()

        grps = elementary.Button(popup)
        grps.text = "OK"
        if callback:
            grps.callback_clicked_add(callback)
        grps.callback_pressed_add(self.close, popup)
        grps.show()

        box = elementary.Box(popup)
        box.pack_end(lbl)
        box.pack_end(grps)
        box.show()

        popup.resize_object_add(box)
        popup.show()

    def confirm(self, message, command):
        popup = elementary.StandardWindow("popup", "eCcess - Please Confirm")

        lbl = elementary.Label(popup)
        lbl.text = message
        lbl.show()

        bbtn = elementary.Button(popup)
        bbtn.text = "Cancel"
        bbtn.callback_clicked_add(self.close, popup)
        bbtn.show()

        grps = elementary.Button(popup)
        grps.text = "Yes"
        grps.callback_clicked_add(self.run_command, popup, command)
        grps.show()

        bbox = elementary.Box(popup)
        bbox.horizontal = True
        bbox.pack_end(bbtn)
        bbox.pack_end(grps)
        bbox.show()

        box = elementary.Box(popup)
        box.pack_end(lbl)
        box.pack_end(bbox)
        box.show()

        popup.resize_object_add(box)
        popup.show()

    def close(self, bnt, window):
        window.hide()

    def run_command(self, bnt, window, command):
        if window:
            window.hide()
        cmd = ecore.Exe(command)
        cmd.on_del_event_add(self.refreshInterface)

    def refreshInterface( self , event=False, cmd=False):
        self.userlist = pwd.getpwall()
        self.grouplist = grp.getgrall()
        self.populate_users()
        self.populate_groups()

    def groupmod(self, l, i, group):
        cp = i.widget_get()
        cp.dismiss()
        self.users.item_simple_push(UserForm(self, group))

    def groupdel(self, l, i, group):
        cp = i.widget_get()
        cp.dismiss()

    def toggle_system_users(self, check):
        self.populate_users()

class Users(elementary.Naviframe):
    def __init__(self, parent):
        elementary.Naviframe.__init__(self, parent.win)

        lbl = elementary.Label(parent.win)
        lbl.text = "Users"
        lbl.show()

        ulist = parent.ulist
        ulist.callback_activated_add(parent.user_activated, self)
        ulist.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        ulist.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        ulist.show()

        bbtn = elementary.Button(parent.win)
        bbtn.text = "Add User"
        bbtn.callback_clicked_add(parent.add_user, self)
        bbtn.show()

        grps = elementary.Button(parent.win)
        grps.text = "Groups"
        grps.callback_clicked_add(parent.flip_page, self)
        grps.show()

        bck = elementary.Button(parent.win)
        bck.text = "Back"
        bck.callback_clicked_add(lambda x: parent.rent.nf.item_pop())
        bck.show()

        sep = elementary.Separator(parent.win)
        sep.show()

        chk = parent.show_system_users = elementary.Check(parent.win)
        chk.callback_changed_add(parent.toggle_system_users)
        chk.text = "Show system users"
        chk.show()

        bbox = elementary.Box(parent.win)
        bbox.horizontal = True
        bbox.pack_end(bbtn)
        bbox.pack_end(grps)
        bbox.pack_end(bck)
        bbox.pack_end(sep)
        bbox.pack_end(chk)
        bbox.show()

        box = elementary.Box(parent.win)
        box.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        box.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        box.pack_end(lbl)
        box.pack_end(ulist)
        box.pack_end(bbox)
        box.show()

        self.item_simple_push(box)
        self.show()

class UserForm(elementary.Box):
    def __init__(self, parent, user):
        elementary.Box.__init__(self, parent.win)
        #self.parent = parent
        entries = {}
        ids = {}

        for text, data in (("Username", user.pw_name), ("User ID", user.pw_uid), ("Group ID", user.pw_gid), ("Real name", user.pw_gecos.strip(",,,")), ("Home directory", user.pw_dir), ("Shell", user.pw_shell)):
            f = elementary.Frame(parent.win)
            f.size_hint_align = (-1.0, 0.0)
            f.text = text
            entries[text] = e = elementary.Label(parent.win)
            e.text = str(data)
            e.show()
            f.content = e
            f.show()
            self.pack_end(f)

        btn = elementary.Button(parent.win)
        btn.text = "Back"
        btn.callback_clicked_add(lambda x: parent.users.item_pop())
        btn.show()
        self.pack_end(btn)

class PasswordForm(elementary.Box):
    def __init__(self, parent, user):
        elementary.Box.__init__(self, parent.win)
        self.main = parent
        entries = {}
        ids = {}

        for text, data in (("Username", user.pw_name), ("Password", ""), ("Confirm Password", "")):
            f = elementary.Frame(parent.win)
            f.size_hint_align = (-1.0, 0.0)
            f.text = text
            if not data:
                entries[text] = e = elementary.Entry(parent.win)
                e.single_line = True
                e.password = True
            else:
                entries[text] = e = elementary.Label(parent.win)
            e.text = str(data)
            e.show()
            f.content = e
            f.show()
            self.pack_end(f)

        btn = elementary.Button(parent.win)
        btn.text = "Cancel"
        btn.callback_clicked_add(lambda x: parent.users.item_pop())
        btn.show()

        bbtn = elementary.Button(parent.win)
        bbtn.text = "Change"
        bbtn.callback_clicked_add(lambda x: parent.users.item_pop())
        bbtn.callback_clicked_add(self.changePassword, entries)
        bbtn.show()

        bbox = elementary.Box(parent.win)
        bbox.horizontal = True
        bbox.pack_end(bbtn)
        bbox.pack_end(btn)
        bbox.show()

        self.pack_end(bbox)

    def changePassword(self, bnt, entries):
        for e in entries:
            print e
            print entries[e].text
        if entries["Password"].text == entries["Confirm Password"].text:
            self.main.run_command(False, False, "gksudo 'changepass.sh %s %s'"%(entries["Username"].text, entries["Password"].text))
        else:
            self.main.popup_message("The entered passwords do not match. Please try again.", "eCcess - Password Mismatch")

class Groups(elementary.Naviframe):
    def __init__(self, parent):
        elementary.Naviframe.__init__(self, parent.win)

        lbl = elementary.Label(parent.win)
        lbl.text = "Groups"
        lbl.show()

        glist = parent.glist
        glist.callback_activated_add(parent.group_activated, self)
        glist.size_hint_weight = (1.0, 1.0)
        glist.size_hint_align = (-1.0, -1.0)
        glist.show()

        bbtn = elementary.Button(parent.win)
        bbtn.text = "Add Group"
        bbtn.callback_clicked_add(parent.add, self)
        bbtn.show()

        grps = elementary.Button(parent.win)
        grps.text = "Users"
        grps.callback_clicked_add(parent.flip_page, self)
        grps.show()

        bck = elementary.Button(parent.win)
        bck.text = "Back"
        bck.callback_clicked_add(lambda x: parent.rent.nf.item_pop())
        bck.show()

        bbox = elementary.Box(parent.win)
        bbox.horizontal = True
        bbox.pack_end(bbtn)
        bbox.pack_end(grps)
        bbox.pack_end(bck)
        bbox.show()

        box = elementary.Box(parent.win)
        box.pack_end(lbl)
        box.pack_end(glist)
        box.pack_end(bbox)
        box.show()

        self.size_hint_weight = (1.0, 1.0)
        self.size_hint_align = (-1.0, -1.0)
        self.item_simple_push(box)
        self.show()

if __name__ == "__main__":
    elementary.init()

    GUI = Eccess()
    GUI.launch(None)
    elementary.run()    
    elementary.shutdown()
