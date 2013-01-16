import elementary
import evas
import ecore
import psutil

class TaskManager(elementary.Box):
    def __init__(self, parent):
        elementary.Box.__init__(self, parent.mainWindow)
        self.win = win = parent.mainWindow
        self.rent = parent
        
        idlst = elementary.List(win)
        idlst.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        idlst.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)

        nlst = elementary.List(win)
        nlst.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        nlst.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)

        self.processes = {}
        tmp = psutil.get_process_list()
        for p in tmp:
            print p
            if "kworker" not in p.name and "watchdog" not in p.name and p.pid > 100:
                idlst.item_append("%s"%p.pid)
                nlst.item_append("%s"%p.name)

        idlst.show()
        nlst.show()

        lbox = elementary.Box(win)
        lbox.horizontal = True
        lbox.pack_end(idlst)
        lbox.pack_end(nlst)
        lbox.show()

        bck = elementary.Button(win)
        bck.text = "Back"
        bck.callback_clicked_add(lambda x: parent.nf.item_pop())
        bck.show()

        bbox = elementary.Box(win)
        bbox.horizontal = True
        bbox.pack_end(bck)
        bbox.show()

        self.pack_end(idlst)
        self.pack_end(nlst)
        self.pack_end(bbox)
