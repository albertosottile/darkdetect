import threading
import multiprocessing as mp

import listener

if __name__ == '__main__':
    t = threading.Thread(target=listener.ls, args=(print, ))
    t.start()
    t.join()

# if __name__ == '__main__':
#     p = mp.Process(target=listener.ls, args=(print,))
#     p.start()
#     p.join()
