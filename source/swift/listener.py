from ctypes import CDLL, CFUNCTYPE, POINTER, c_int, byref

def ls(f):
    native_lib = CDLL('./libTheme')

    class Trigger:
        def configure(self, f):
            print('Configured')
            self.f = f

        def fire(self, theme):
            self.f(theme)

    tr = Trigger()

    def callback(number):
        theme = "Light" if number[0] == 0 else "Dark"
        #print('python: the number is ', number[0])
        #print('python: the theme is ', theme)
        print(theme)
        tr.fire(theme)

    SWIFT_CALLBACK = CFUNCTYPE(None, POINTER(c_int))
    swift_callback = SWIFT_CALLBACK(callback)

    native_lib.set_callback(byref(swift_callback))

    tr.configure(f)
    print('aaa')
    native_lib.start()
    print('bbb')
