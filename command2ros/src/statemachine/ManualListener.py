class ManualListener(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()