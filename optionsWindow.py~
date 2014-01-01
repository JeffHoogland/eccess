import elementary
import evas

class optionsWindow(elementary.Box):
    def __init__( self, parent ):
        elementary.Box.__init__(self, parent.mainWindow)
        self.win = parent.mainWindow
        self.horizontal = True

        b1 = elementary.Box(self.win)
        b1.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        b1.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        b1.show()

        bt = elementary.Label(parent.mainWindow)
        bt.text_set("<div align='center'><b>Select an Option:</b></div>")
        bt.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        bt.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        b1.pack_end(bt)
        bt.show()

        bt = elementary.Button(parent.mainWindow)
        bt.text_set("About eCcess")
        bt.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        bt.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        bt.callback_clicked_add(self.about)
        b1.pack_end(bt)
        bt.show()

        b2 = elementary.Box(self.win)
        b2.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        b2.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        b2.show()

        bt = elementary.Button(parent.mainWindow)
        bt.text_set("Users and Groups")
        bt.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        bt.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        bt.callback_clicked_add(parent.users_groups_spawn)
        b2.pack_end(bt)
        bt.show()

        bt = elementary.Button(parent.mainWindow)
        bt.text_set("Time and Date")
        bt.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        bt.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        bt.callback_clicked_add(parent.time_date_spawn)
        b2.pack_end(bt)
        bt.show()

        bt = elementary.Button(parent.mainWindow)
        bt.text_set("Task Manager")
        bt.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        bt.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        bt.callback_clicked_add(parent.task_manager_spawn)
        #b2.pack_end(bt)
        #bt.show()

        bt = elementary.Button(parent.mainWindow)
        bt.text_set("Screen Resolution")
        bt.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        bt.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        bt.callback_clicked_add(parent.screen_setup_spawn)
        #self.pack(bt, 1, 3, 1, 1)
        #bt.show()

        self.pack_end(b1)
        self.pack_end(b2)

    def about( self, bt ):
        popup = elementary.Popup(self.win)
        popup.text = "Written in Elementary and Python - " \
                        "By: Jeff Hoogland - " \
                        "Special thanks to: Stephen Houston and Kai Huuhko"
        popup.part_text_set("title,text", "About")
        bt = elementary.Button(self.win)
        bt.text = "OK"
        bt.callback_clicked_add(lambda x: popup.hide())
        popup.part_content_set("button1", bt)
        popup.show()
