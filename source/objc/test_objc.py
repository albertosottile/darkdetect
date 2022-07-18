import asyncio
import threading

import ctypes

objc = ctypes.cdll.LoadLibrary('./libObserver.dylib')

void_p = ctypes.c_void_p
ull = ctypes.c_uint64

objc.objc_getClass.restype = void_p
objc.sel_registerName.restype = void_p

MSGPROTOTYPE = ctypes.CFUNCTYPE(void_p, void_p, void_p, void_p)
msg = MSGPROTOTYPE(('objc_msgSend', objc), ((1 ,'', None), (1, '', None), (1, '', None)))

def _utf8(s):
    if not isinstance(s, bytes):
        s = s.encode('utf8')
    return s

def n(name):
    return objc.sel_registerName(_utf8(name))

def C(classname):
    return objc.objc_getClass(_utf8(classname))

def run():
    event_loop = asyncio.new_event_loop()

    NSAutoreleasePool = C('NSAutoreleasePool')
    pool = msg(NSAutoreleasePool, n('alloc'))
    pool = msg(pool, n('init'))

    #Observer *observer = [[Observer alloc] init];
    Observer = C('Observer')
    observer = msg(Observer, n('alloc'))
    observer = msg(observer, n('init'))

    try:
        observer = msg(observer, n('run'))
        event_loop.run_forever()
    finally:
        msg(pool, n('release'))

#run()

t = threading.Thread(target=run)
t.start()
t.join()
