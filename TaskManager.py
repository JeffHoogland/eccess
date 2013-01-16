import elementary
import evas
import ecore
import psutil

class TaskManager(elementary.Box):
    def __init__(self, parent):
        elementary.Box.__init__(self, parent.mainWindow)
        self.win = win = parent.mainWindow
        self.rent = parent
        
        lbl = elementary.Label(self.win)
        lbl.text = "Running Processes:"
        lbl.show()

        itc = elementary.GenlistItemClass(item_style="default",
                                       content_get_func=self.process_return)

        self.gl = gl = elementary.Genlist(self.win)
        gl.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        gl.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        gl.bounce_set(False, True)
        gl.show()

        self.processes = {}
        tmp = psutil.get_process_list()
        for p in tmp:
            #print p
            if "kworker" not in p.name and "getty" not in p.name and "watchdog" not in p.name and p.pid > 100:
                gl.item_append(itc, p, None)

        bck = elementary.Button(win)
        bck.text = "Back"
        bck.callback_clicked_add(lambda x: parent.nf.item_pop())
        bck.show()

        bbox = elementary.Box(win)
        bbox.horizontal = True
        bbox.pack_end(bck)
        bbox.show()

        self.pack_end(lbl)
        self.pack_end(gl)
        self.pack_end(bbox)

    def process_return( self, obj, part, data ):
        print data.name
        print data.pid
        if part == "elm.swallow.icon":
            box = elementary.Box(self.win)
            box.horizontal = True
            
            pid = elementary.Label(self.win)
            pid.text = str(data.pid)
            pid.show()

            sep = elementary.Separator(self.win)
            sep.show()

            pname = elementary.Label(self.win)
            pname.text = data.name
            pname.show()

            box.pack_end(pid)
            box.pack_end(sep)
            box.pack_end(pname)

            return box
        return None
