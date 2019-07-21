import threading

class Interval:
    created = []
    def __init__(self, function, interval, id):
        self.id = id
        self.function = function
        self.interval = interval        
        self.running = self.id in self.created
        self.created.append(self.id)

    def func(self):
        # do something here ...
        if not self.f_stop.is_set():
            # call f() again in 60 seconds
            self.function()
            threading.Timer(self.interval, self.func).start()

    def start(self):
        if not self.running:
            self.running = True
            self.f_stop = threading.Event()
            # start calling f now and every 60 sec thereafter
            self.func()

    def stop(self):
        if self.running:
            self.running = False
            # stop the thread when needed
            self.f_stop.set()