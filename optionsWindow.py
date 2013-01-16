import elementary
import evas

class optionsWindow(elementary.Table):
    def __init__( self, parent ):
        elementary.Table.__init__(self, parent.mainWindow)

        bt = elementary.Label(parent.mainWindow)
        bt.text_set("<div align='center'><b>Select an Option:</b></div>")
        bt.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        bt.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        self.pack(bt, 0, 0, 1, 1)
        bt.show()

        bt = elementary.Button(parent.mainWindow)
        bt.text_set("Users and Groups")
        bt.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        bt.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        bt.callback_clicked_add(parent.users_groups_spawn)
        self.pack(bt, 1, 0, 1, 1)
        bt.show()

        bt = elementary.Button(parent.mainWindow)
        bt.text_set("Time and Date")
        bt.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        bt.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        bt.callback_clicked_add(parent.time_date_spawn)
        self.pack(bt, 1, 1, 1, 1)
        bt.show()
