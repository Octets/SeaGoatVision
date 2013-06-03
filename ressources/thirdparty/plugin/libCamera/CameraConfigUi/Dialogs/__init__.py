import os

for f in os.listdir(os.path.dirname(__file__)):
    filename, _ = os.path.splitext(f)
    code = 'from %(module)s import *' % {'module' : filename} 
    exec code
