import threading

import ctypes
loop = ctypes.cdll.LoadLibrary('./loop')
loop.run.argtypes = None
loop.run.restype = ctypes.c_void_p

#loop.run() #this works

t = threading.Thread(target=loop.run, args=())
t.start()
t.join()
