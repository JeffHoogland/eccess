import elementary
import evas
import ecore
import psutil
import os
import getpass

def sortedDictValues(adict):
    items = adict.items()
    items.sort()
    return [value for key, value in items]

class TaskManager(elementary.Box):
    def __init__(self, parent):
        elementary.Box.__init__(self, parent.mainWindow)
        self.win = win = parent.mainWindow
        self.sortmethod = "pid"
        self.rent = parent
        self.appstokill = []
        self.processid = {}
        self.processname = {}
        
        self.loop = ecore.timer_add(0.5, self.update)
        
        lbl = elementary.Label(self.win)
        lbl.text = "Running Processes:"
        lbl.show()

        tbox = elementary.Box(self.win)
        tbox.horizontal = True
        tbox.size_hint_align_set(0.0, 0.5)
        tbox.show()

        pid = elementary.Button(self.win)
        pid.text = "PID"
        pid.callback_clicked_add(self.sort_by, "pid")
        pid.show()

        sep = elementary.Separator(self.win)
        sep.show()
        sep2 = elementary.Separator(self.win)
        sep2.show()
        sep3 = elementary.Separator(self.win)
        sep3.show()
        sep4 = elementary.Separator(self.win)
        sep4.show()

        pname = elementary.Button(self.win)
        pname.text = "Process Name"
        pname.callback_clicked_add(self.sort_by, "name")
        pname.show()

        user = elementary.Button(self.win)
        user.text = "User"
        user.show()

        cpu = elementary.Button(self.win)
        cpu.text = "CPU"
        cpu.show()

        mem = elementary.Button(self.win)
        mem.text = "Mem"
        mem.show()

        tbox.pack_end(pid)
        tbox.pack_end(sep)
        tbox.pack_end(user)
        tbox.pack_end(sep2)
        tbox.pack_end(cpu)
        tbox.pack_end(sep3)
        tbox.pack_end(mem)
        tbox.pack_end(sep4)
        tbox.pack_end(pname)

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
        self.pack_end(tbox)
        self.pack_end(gl)
        self.pack_end(bbox)

    def sort_by(self, bt, method):
        self.sortmethod = method
        self.processes_build()

    def update(self):
        for p in self.processid:
            for i in self.gl.realized_items_get():
                if p == i.data.pid:
                    self.processid[p].update()
        return 1

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
        itc = elementary.GenlistItemClass(item_style="default",
                                       content_get_func=self.process_return)

        tmp = psutil.get_process_list()
        if self.sortmethod == "pid":
            for p in tmp:
                if p.username == getpass.getuser():
                    self.gl.item_append(itc, p, None)
        elif self.sortmethod == "name":
            #write some code to build the list based on process name
            sdv = sortedDictValues(self.processname)
            for v in sdv:
                self.gl.item_append(itc, v.dt, None)

    def process_return( self, obj, part, data ):
        if part == "elm.swallow.icon":
            p = Process(self, data)
            self.processid[data.pid] = p
            self.processname[data.name] = p
            return p
        elif part == "elm.swallow.end":
            bt = elementary.Button(self.win)
            bt.text = "Kill Process"
            bt.callback_pressed_add(self.kill_process, data.pid)
            return bt
        return None

class Process(elementary.Box):
    def __init__(self, parent, data):
        elementary.Box.__init__(self, parent.win)
        self.win = parent.win
        self.dt = data

        self.horizontal = True
        
        pd = str(data.pid)
        #while len(pd) < 8:
        #    pd = " %s"%pd

        pid = elementary.Check(self.win)
        pid.text = pd
        pid.callback_changed_add(parent.check_sel)
        pid.show()

        sep = elementary.Separator(self.win)
        sep.show()
        sep2 = elementary.Separator(self.win)
        sep2.show()
        sep3 = elementary.Separator(self.win)
        sep3.show()
        sep4 = elementary.Separator(self.win)
        sep4.show()

        pname = elementary.Label(self.win)
        pname.text = data.name
        pname.show()

        user = elementary.Label(self.win)
        user.text = data.username
        user.show()

        self.cpu = cpu = elementary.Label(self.win)
        cpu.text = str(data.get_cpu_percent(interval=0))
        cpu.show()

        self.mem = mem = elementary.Label(self.win)
        mem.text = "%.2f"%data.get_memory_percent()
        mem.show()

        self.pack_end(pid)
        self.pack_end(sep)
        self.pack_end(user)
        self.pack_end(sep2)
        self.pack_end(cpu)
        self.pack_end(sep3)
        self.pack_end(mem)
        self.pack_end(sep4)
        self.pack_end(pname)
        self.show()

    def update(self):
        #print str(self.dt.get_cpu_percent(interval=0))
        self.cpu.text = str(self.dt.get_cpu_percent(interval=0))
        #print self.dt.get_memory_percent()
        self.mem.text = "%.2f"%self.dt.get_memory_percent()
