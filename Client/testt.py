import cv2
from pylab import *

blue, green, red = cv2.split(cv2.imread('/home/benoit/testtt/test.png'))

f = file('/home/benoit/testtt/test.png.map', 'r')
s = f.read()
f.close()
map = fromstring(s, bool).reshape(480, 640)
#map = np.invert(map)

b = blue[map].flatten()
g = green[map].flatten()
r = red[map].flatten()

bx = 
x = arange(1, b.size + 1)
print b.size
print x.size

plot(x, b, 'b.', label='Blue channel')
#plot(x, g, 'g.', label='Green channel')
#plot(x, r, 'r.', label='Red channel')
show()