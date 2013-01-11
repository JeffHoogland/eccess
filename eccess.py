"""A tool written in Python and Elementary to provide a GUI for configuring Unix users and groups"""

import os
import elementary
import edje
import ecore
import evas
import emotion
import time
import pwd
import grp

class Eccess:

    def __init__( self ):
        self.mainWindow = elementary.StandardWindow("mainwindow", "eCcess - System Tool")

    def users_groups( self, bt ):
        print "Users and groups CB"
        UserManager()

    def launch( self, obj ):
        if obj is None:
            self.mainWindow.callback_delete_request_add(lambda o: elementary.exit())
        
        bg = elementary.Background(self.mainWindow)
        self.mainWindow.resize_object_add(bg)
        bg.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        bg.show()

        #nf = elementary.Naviframe(self.mainWindow)
        #nf.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        #self.mainWindow.resize_object_add(nf)

        tb = elementary.Table(self.mainWindow)
        #nf.item_simple_push(tb)
        tb.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        self.mainWindow.resize_object_add(tb)
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

        self.mainWindow.resize(800, 300)
        self.mainWindow.show()

class UserListClass(elementary.GenlistItemClass):
    def text_get(self, genlist, part, data):
        return data.pw_name

class GroupListClass(elementary.GenlistItemClass):
    def text_get(self, genlist, part, data):
        return data.gr_name

class UserManager(object):
    def __init__(self):
        self.userlist = pwd.getpwall()
        self.grouplist = grp.getgrall()

        win = self.win = elementary.StandardWindow("usermanager", "eCcess - Users and Groups")
        win.callback_delete_request_add(self.quit)

        ulist = self.ulist = elementary.Genlist(win)
        glist = self.glist = elementary.Genlist(win)

        flip = self.flip = elementary.Flip(win)
        flip.interaction = elementary.ELM_FLIP_INTERACTION_ROTATE
        flip.interaction_direction_enabled_set(elementary.ELM_FLIP_DIRECTION_LEFT, True)
        flip.interaction_direction_hitsize_set(elementary.ELM_FLIP_DIRECTION_LEFT, 0.1)
        flip.size_hint_weight = (1.0, 1.0)
        win.resize_object_add(flip)

        users = self.users = Users(self)
        groups = self.groups = Groups(self)

        flip.part_content_set("front", users)
        flip.part_content_set("back", groups)
        flip.show()

        self.populate_users()
        self.populate_groups()

        win.resize(400,465)
        win.show()

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
        usermk = elementary.StandardWindow("usermaker", "eCcess - Create User")

        bg = elementary.Background(usermk)
        usermk.resize_object_add(bg)
        bg.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        bg.show()

        lbl1 = elementary.Label(usermk)
        lbl1.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        lbl1.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        lbl1.text = "Username:"
        lbl1.show()

        lbl2 = elementary.Label(usermk)
        lbl2.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        lbl2.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        lbl2.text = "Password:"
        lbl2.show()

        lbl3 = elementary.Label(usermk)
        lbl3.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        lbl3.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        lbl3.text = "Confirm Password:"
        lbl3.show()

        entry1 = elementary.Entry(usermk)
        entry1.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        entry1.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        entry1.show()

        entry2 = elementary.Entry(usermk)
        entry2.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        entry2.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        entry2.password = True
        entry2.show()

        entry3 = elementary.Entry(usermk)
        entry3.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        entry3.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        entry3.password = True
        entry3.show()

        ok = elementary.Button(usermk)
        ok.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        ok.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        ok.text = "Create User"
        ok.callback_pressed_add(self.create_user, entry1, entry2, entry3)
        ok.callback_pressed_add(self.close, usermk)
        ok.show()

        nvm = elementary.Button(usermk)
        nvm.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        nvm.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        nvm.text = "Cancel"
        nvm.callback_pressed_add(self.close, usermk)
        nvm.show()

        bbox = elementary.Box(usermk)
        bbox.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        bbox.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        bbox.horizontal = True
        bbox.pack_end(ok)
        bbox.pack_end(nvm)
        bbox.show()

        box = elementary.Box(usermk)
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

        usermk.resize_object_add(box)
        usermk.resize(350, 300)
        usermk.show()

    def create_user(self, bnt, username, passwd1, passwd2):
        print "%s %s %s"%(username.text, passwd1.text, passwd2.text)
        if passwd1.text == passwd2.text:
            self.run_command(False, False, "gksudo 'useradd %s -m -p %s'"%(username.text, passwd1.text))
        else:
            self.popup_message("The entered passwords do not match. Please try again.", "eCcess - Password Mismatch", self.add_user)

    def flip_page(self, btn, data):
        self.flip.go(elementary.ELM_FLIP_CUBE_RIGHT)

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

    def quit(self, *args):
        self.win.hide()

class Users(elementary.Naviframe):
    def __init__(self, parent):
        elementary.Naviframe.__init__(self, parent.win)

        lbl = elementary.Label(parent.win)
        lbl.text = "Users"
        lbl.show()

        ulist = parent.ulist
        ulist.callback_activated_add(parent.user_activated, self)
        ulist.size_hint_weight = (1.0, 1.0)
        ulist.size_hint_align = (-1.0, -1.0)
        ulist.show()

        bbtn = elementary.Button(parent.win)
        bbtn.text = "Add User"
        bbtn.callback_clicked_add(parent.add_user, self)
        bbtn.show()

        grps = elementary.Button(parent.win)
        grps.text = "Groups"
        grps.callback_clicked_add(parent.flip_page, self)
        grps.show()

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
        bbox.pack_end(sep)
        bbox.pack_end(chk)
        bbox.show()

        box = elementary.Box(parent.win)
        box.pack_end(lbl)
        box.pack_end(ulist)
        box.pack_end(bbox)
        box.show()

        self.size_hint_weight = (1.0, 1.0)
        self.size_hint_align = (-1.0, -1.0)
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
        btn.text = "Close"
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

        bbox = elementary.Box(parent.win)
        bbox.horizontal = True
        bbox.pack_end(bbtn)
        bbox.pack_end(grps)
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
