import os
import sys
import elementary
import ecore
import evas
import pwd
import grp


def getGroups(user=False):
    grouplist = []
    if not user:
        for group in grp.getgrall():
            grouplist.append(group[0])
    else:
        for group in grp.getgrall():
            if user in group[3]:
                grouplist.append(group[0])
    return grouplist

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
        cp.item_append("Group Membership", None, self.usergroups, genlist.data)
        cp.item_append("Delete", None, self.userdel, genlist.data)
        pos = self.win.evas.pointer_canvas_xy_get()
        cp.pos = pos
        cp.show()

    def group_activated(self, item, genlist, data):
        cp = elementary.Ctxpopup(self.win)
        cp.item_append("Delete", None, self.groupdel, genlist.data)
        pos = self.win.evas.pointer_canvas_xy_get()
        cp.pos = pos
        cp.show()

    def add_group(self, btn=False, data=False):
        lbl1 = elementary.Frame(self.win)
        lbl1.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        lbl1.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        lbl1.text = "Group Name:"
        lbl1.show()

        entry1 = elementary.Entry(self.win)
        entry1.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        entry1.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        entry1.single_line = True
        entry1.show()
        lbl1.content = entry1

        ok = elementary.Button(self.win)
        ok.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        ok.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        ok.text = "Create Group"
        ok.callback_pressed_add(self.create_group, entry1)
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
        #box.pack_end(lbl2)
        #box.pack_end(lbl3)
        box.pack_end(bbox)
        box.show()

        self.rent.nf.item_simple_push(box)

    def create_group(self, bnt, groupname):
        print "%s"%(groupname.text)
        self.run_command(False, False, "gksudo 'groupadd %s'"%groupname.text)
        self.rent.nf.item_pop()

    def add_user(self, btn=False, data=False):
        lbl1 = elementary.Frame(self.win)
        lbl1.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        lbl1.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        lbl1.text = "Username:"
        lbl1.show()

        lbl2 = elementary.Frame(self.win)
        lbl2.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        lbl2.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        lbl2.text = "Password:"
        lbl2.show()

        lbl3 = elementary.Frame(self.win)
        lbl3.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        lbl3.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        lbl3.text = "Confirm Password:"
        lbl3.show()

        entry1 = elementary.Entry(self.win)
        entry1.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        entry1.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        entry1.single_line = True
        entry1.show()
        lbl1.content = entry1

        entry2 = elementary.Entry(self.win)
        entry2.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        entry2.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        entry2.single_line = True
        entry2.password = True
        entry2.show()
        lbl2.content = entry2

        entry3 = elementary.Entry(self.win)
        entry3.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        entry3.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        entry3.single_line = True
        entry3.password = True
        entry3.show()
        lbl3.content = entry3

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
        box.pack_end(lbl2)
        box.pack_end(lbl3)
        box.pack_end(bbox)
        box.show()

        self.rent.nf.item_simple_push(box)

    def create_user(self, bnt, username, passwd1, passwd2):
        print "%s %s %s"%(username.text, passwd1.text, passwd2.text)
        self.rent.nf.item_pop()
        if passwd1.text == passwd2.text:
            self.run_command(False, False, "gksudo 'useradd %s -m -p %s'"%(username.text, passwd1.text))
        else:
            self.popup_message("The entered passwords do not match. Please try again.", "Password Mismatch", self.add_user)

    def flip_page(self, btn, data):
        self.go(elementary.ELM_FLIP_CUBE_RIGHT)

    def usermod(self, l, i, user):
        cp = i.widget_get()
        cp.dismiss()
        self.users.item_simple_push(UserForm(self, user))

    def usergroups(self, l, i, user):
        cp = i.widget_get()
        cp.dismiss()
        print "%s"%user
        self.users.item_simple_push(GroupsForm(self, user))

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
        popup = elementary.Popup(self.win)
        popup.text = message
        popup.part_text_set("title,text", title)
        bt = elementary.Button(self.win)
        bt.text = "OK"
        if callback:
            bt.callback_clicked_add(callback, popup)
        bt.callback_clicked_add(lambda x: popup.hide())
        popup.part_content_set("button1", bt)
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

    def groupdel(self, l, i, group):
        cp = i.widget_get()
        cp.dismiss()
        print group[0]
        self.confirm("Are you sure you want to delete the group '%s'"%group[0], "gksudo 'groupdel %s'"%group[0])

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

class GroupsForm(elementary.Box):
    def __init__(self, parent, user):
        elementary.Box.__init__(self, parent.win)
        self.rent = parent
        self.username = user[0]

        groups = getGroups()
        self.usergroups = usergroups = getGroups(user[0])
        
        label = elementary.Label(parent.win)
        label.text = "%s Groups:"%user[0]

        itc = elementary.GengridItemClass(item_style="default",
                                       content_get_func=self.check_return)

        gg = elementary.Gengrid(parent.win)
        gg.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        gg.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        gg.horizontal_set(False)
        gg.bounce_set(False, True)
        gg.item_size_set(140, 40)
        gg.align_set(0.5, 0.0)
        gg.show()
        gg.select_mode_set(elementary.ELM_OBJECT_SELECT_MODE_NONE)

        for group in groups:
            gg.item_append(itc, [group, usergroups], None)

        sc = elementary.Button(parent.win)
        sc.text = "Save Changes"
        sc.callback_clicked_add(self.save_changes, gg)
        sc.show()

        ngrp = elementary.Button(parent.win)
        ngrp.text = "New Group"
        ngrp.callback_clicked_add(lambda x: parent.add_group())
        ngrp.show()

        btn = elementary.Button(parent.win)
        btn.text = "Back"
        btn.callback_clicked_add(lambda x: parent.users.item_pop())
        btn.show()

        bbox = elementary.Box(parent.win)
        bbox.horizontal = True
        bbox.pack_end(sc)
        bbox.pack_end(ngrp)
        bbox.pack_end(btn)
        bbox.show()

        label.show()
        self.pack_end(label)
        self.pack_end(gg)
        self.pack_end(bbox)

    def check_sel( self, ck):
        if ck.state_get():
            self.usergroups.append(ck.text)
        else:
            self.usergroups.remove(ck.text)
        print ck.text
        print ck.state_get()
        print self.usergroups

    def save_changes( self, bt, gengrid ):
        grps = ""
        for group in self.usergroups:
            if self.usergroups.index(group) == 0:
                grps = "%s"%group
            else:
                grps = "%s,%s"%(grps, group)
        print grps
        self.rent.run_command(False, False, "gksudo 'usermod -G %s %s'"%(grps, self.username))
        self.rent.users.item_pop()

    def check_return( self, obj, part, data ):
        if part == "elm.swallow.icon":
            ck = elementary.Check(obj)
            ck.text_set(data[0])
            ck.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
            ck.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
            ck.callback_changed_add(self.check_sel)
            if data[0] in data[1]:
                ck.state_set(True)
            return ck
        return None

    def group_toggle( self, chk ):
        print chk.text

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
            self.main.popup_message("The entered passwords do not match. Please try again.", "Password Mismatch")

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
        bbtn.callback_clicked_add(parent.add_group, self)
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
