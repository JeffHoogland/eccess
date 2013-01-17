import elementary
import evas
import ecore
import psutil
import os

class TaskManager(elementary.Box):
    def __init__(self, parent):
        elementary.Box.__init__(self, parent.mainWindow)
        self.win = win = parent.mainWindow
        self.rent = parent
        self.appstokill = []
        self.processes = []
        
        lbl = elementary.Label(self.win)
        lbl.text = "Running Processes:"
        lbl.show()

        self.gl = gl = elementary.Genlist(self.win)
        gl.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        gl.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        gl.bounce_set(False, True)
        gl.select_mode_set(elementary.ELM_OBJECT_SELECT_MODE_NONE)
        gl.show()

        self.processes_build()

        kills = elementary.Button(self.win)
        kills.text = "Kill Selected Applications"
        kills.callback_clicked_add(self.kill_selected)
        kills.show()

        sep = elementary.Separator(self.win)
        sep.show()

        bck = elementary.Button(win)
        bck.text = "Back"
        bck.callback_clicked_add(lambda x: parent.nf.item_pop())
        bck.show()

        bbox = elementary.Box(win)
        bbox.horizontal = True
        bbox.pack_end(kills)
        bbox.pack_end(sep)
        bbox.pack_end(bck)
        bbox.show()

        self.pack_end(lbl)
        self.pack_end(gl)
        self.pack_end(bbox)

    def run_command(self, bnt, window, command):
        if window:
            window.hide()
        cmd = ecore.Exe(command)
        cmd.on_del_event_add(self.processes_build)

    def kill_selected( self, bt ):
        for pid in self.appstokill:
            self.kill_process(False, pid)

    def check_sel( self, ck ):
        if ck.state_get():
            self.appstokill.append(ck.text)
        else:
            self.appstokill.remove(ck.text)
        #print self.appstokill

    def kill_process( self, bt, pid ):
        self.run_command(False, False, "kill -9 %s"%pid)
    
    def processes_build( self, cmd=False, arg=False ):
        #print "cmd %s , arg %s"%(cmd, arg)
        self.gl.clear()
        self.processes = []

        itc = elementary.GenlistItemClass(item_style="default",
                                       content_get_func=self.process_return)

        tmp = psutil.get_process_list()
        for p in tmp:
            if os.getpgid(p.pid) > 1 and "getty" not in p.name:
                self.gl.item_append(itc, p, None)
                self.processes.append(p)

    def process_return( self, obj, part, data ):
        #print data.name
        #print data.pid
        #print "Name: %s , Group: %s"%(data.name, os.getpgid(data.pid))
        if part == "elm.swallow.icon":
            box = elementary.Box(self.win)
            box.horizontal = True
            
            pid = elementary.Check(self.win)
            pid.text = str(data.pid)
            pid.callback_changed_add(self.check_sel)
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
        elif part == "elm.swallow.end":
            bt = elementary.Button(self.win)
            bt.text = "Kill Process"
            bt.callback_pressed_add(self.kill_process, data.pid)
            return bt
        return None
