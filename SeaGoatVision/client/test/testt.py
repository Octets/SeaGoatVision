import cv2
import pylab

blue, green, red = cv2.split(cv2.imread('/home/benoit/testtt/test.png'))

f = file('/home/benoit/testtt/test.png.mapping', 'r')
s = f.read()
f.close()
mapping = pylab.np.fromstring(s, bool).reshape(480, 640)
#mapping = np.invert(mapping)

b = blue[mapping].flatten()
g = green[mapping].flatten()
r = red[mapping].flatten()

x = pylab.arange(1, b.size + 1)
print b.size
print x.size

pylab.plot(x, b, 'b.', label='Blue channel')
#plot(x, g, 'g.', label='Green channel')
#plot(x, r, 'r.', label='Red channel')
pylab.show()