import threading

from ctypes import CDLL, CFUNCTYPE, POINTER, c_int, byref

def listener(f):
    native_lib = CDLL('./libTheme')

    def callback(number):
        theme = "Light" if number[0] == 0 else "Dark"
        #print('python: the number is ', number[0])
        #print('python: the theme is ', theme)
        f(theme)

    SWIFT_CALLBACK = CFUNCTYPE(None, POINTER(c_int))
    swift_callback = SWIFT_CALLBACK(callback)

    native_lib.set_callback(byref(swift_callback))
    native_lib.start()

    print('aaaa') # this is never printed
    # while True:
    #     pass

listener(print)

# t = threading.Thread(target=listener, args=(print, ))
# t.start()
# t.join()
