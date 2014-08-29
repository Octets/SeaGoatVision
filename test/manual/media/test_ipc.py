#!/usb/bin/env python2
import zmq
import time
import numpy as np

context = zmq.Context()

publisher = context.socket(zmq.PUB)
publisher.bind("ipc:///tmp/seagoatvision_media.ipc")

for j in range(10):
    for i in range(255):
        width = 100
        message = np.ones((width, width), dtype=np.uint8) * (i + 1)
        m_width = width >> 8
        property = bytearray(chr(m_width)) + bytearray(chr(width))
        array_message = property + message.tostring()
        publisher.send(array_message)
        time.sleep(0.02)
