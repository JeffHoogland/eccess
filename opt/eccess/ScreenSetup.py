import elementary
import evas
import ecore

class ScreenSetup(elementary.Box):
    def __init__(self, parent):
        elementary.Box.__init__(self, parent.mainWindow)
        self.win = win = parent.mainWindow
        self.rent = parent
        
        lst = elementary.List(win)
        lst.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        lst.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)

        lst.show()

        bck = elementary.Button(win)
        bck.text = "Back"
        bck.callback_clicked_add(lambda x: parent.nf.item_pop())
        bck.show()

        bbox = elementary.Box(win)
        bbox.horizontal = True
        bbox.pack_end(bck)
        bbox.show()

        self.pack_end(lst)
        self.pack_end(bbox)
