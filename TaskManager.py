import elementary
import evas
import ecore
import psutil
import os
import getpass
import sortedlist as sl

EXPAND_BOTH = evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND
FILL_BOTH = evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL

class TaskManager(elementary.Box):
    def __init__(self, parent):
        elementary.Box.__init__(self, parent.mainWindow)
        self.win = win = parent.mainWindow
        self.rent = parent
        self.appstokill = []
        self.process = {}
        
        self.loop = ecore.timer_add(0.5, self.update)
        
        lbl = elementary.Label(self.win)
        lbl.text = "Running Processes:"
        lbl.show()

        scr = elementary.Scroller(self.win)
        scr.size_hint_weight = EXPAND_BOTH
        scr.size_hint_align = FILL_BOTH

        titles = [("PID", True), ("User", True), ("CPU", True), ("Memory", True), ("Process Name", True), ("", False)]

        self.slist = slist = sl.SortedList(self, titles=titles,   size_hint_weight=EXPAND_BOTH,
            size_hint_align=FILL_BOTH, homogeneous=True)
        scr.content = slist
        scr.show()

        slist.show()

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
        self.pack_end(scr)
        self.pack_end(bbox)

    def update(self):
        self.processes_build()
        for p in self.process:
            self.process[p].update()
        self.slist.update()
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
        self.slist.row_unpack(self.process[pid], True)
        self.process.pop(pid, None)
    
    def processes_build( self, cmd=False, arg=False ):
        #print "cmd %s , arg %s"%(cmd, arg)

        tmp = psutil.get_process_list()
        currentpids = []
        pidstoremove = []
        for p in tmp:
            if p.username == getpass.getuser():
                currentpids.append(p.pid)
                if p.pid not in self.process:
                    cess = Process(self, p)
                    self.process[p.pid] = cess
                    self.slist.row_pack(cess, sort=False)
        for pid in self.process:
            if pid not in currentpids:
                self.slist.row_unpack(self.process[pid], True)
                pidstoremove.append(pid)
        for pid in pidstoremove:
            self.process.pop(pid, None)

class Process(list):
    def __init__(self, parent, data):
        self.win = parent.win
        self.dt = data

        pd = str(data.pid)
        #while len(pd) < 8:
        #    pd = " %s"%pd

        pid = elementary.Check(self.win)
        pid.text = pd
        pid.callback_changed_add(parent.check_sel)
        pid.show()

        pname = elementary.Label(self.win)
        pname.text = data.name[0:25]
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

        bt = elementary.Button(self.win)
        bt.text = "Kill Process"
        bt.callback_pressed_add(parent.kill_process, data.pid)
        bt.show()

        self.append(pid)
        self.append(user)
        self.append(cpu)
        self.append(mem)
        self.append(pname)
        self.append(bt)

    def update(self):
        #print str(self.dt.get_cpu_percent(interval=0))
        self.cpu.text = str(self.dt.get_cpu_percent(interval=0))
        #print self.dt.get_memory_percent()
        self.mem.text = "%.2f"%self.dt.get_memory_percent()
