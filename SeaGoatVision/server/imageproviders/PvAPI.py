import ctypes

try:
    lib = ctypes.cdll.LoadLibrary('libPvAPI.so')
except:
    lib = ctypes.cdll.LoadLibrary('lib', 'x86' 'libPvAPI.so')
    
#Error codes, returned by most functions:
class tPvErr:
    ePvErrSuccess       = 0        # No error
    ePvErrCameraFault   = 1        # Unexpected camera fault
    ePvErrInternalFault = 2        # Unexpected fault in PvApi or driver
    ePvErrBadHandle     = 3        # Camera handle is invalid
    ePvErrBadParameter  = 4        # Bad parameter to API call
    ePvErrBadSequence   = 5        # Sequence of API calls is incorrect
    ePvErrNotFound      = 6        # Camera or attribute not found
    ePvErrAccessDenied  = 7        # Camera cannot be opened in the specified mode
    ePvErrUnplugged     = 8        # Camera was unplugged
    ePvErrInvalidSetup  = 9        # Setup is invalid (an attribute is invalid)
    ePvErrResources     = 10       # System/network resources or memory not available
    ePvErrBandwidth     = 11       # 1394 bandwidth not available
    ePvErrQueueFull     = 12       # Too many frames on queue
    ePvErrBufferTooSmall= 13       # Frame buffer is too small
    ePvErrCancelled     = 14       # Frame cancelled by user
    ePvErrDataLost      = 15       # The data for the frame was lost
    ePvErrDataMissing   = 16       # Some data in the frame is missing
    ePvErrTimeout       = 17       # Timeout during wait
    ePvErrOutOfRange    = 18       # Attribute value is out of the expected range
    ePvErrWrongType     = 19       # Attribute is not this type (wrong access function) 
    ePvErrForbidden     = 20       # Attribute write forbidden at this time
    ePvErrUnavailable   = 21       # Attribute is not available at this time
    ePvErrFirewall      = 22       # A firewall is blocking the traffic (Windows only)
    __ePvErr_force_32   = 0xFFFFFFFF

# Camera information type (extended)
class tPvCameraInfoEx(ctypes.Structure): pass
tPvCameraInfoEx._fields_ = [
    ('StructVer', ctypes.c_ulong),          # Version of this structure
    ('UniqueId', ctypes.c_ulong),           # Unique value for each camera
    ('CameraName', ctypes.c_char * 32),     # People-friendly camera name (usually part name)
    ('ModelName', ctypes.c_char * 32),      # Name of camera part
    ('PartNumber', ctypes.c_char * 32),     # Manufacturer's part number
    ('SerialNumber', ctypes.c_char * 32),   # Camera's serial number
    ('FirmwareVersion', ctypes.c_char * 32),# Camera's firmware version
    ('PermittedAccess', ctypes.c_ulong),    # A combination of tPvAccessFlags
    ('InterfaceId', ctypes.c_ulong),        # Unique value for each interface or bus
    ('InterfaceType', ctypes.c_ulong)]      # Interface type; see tPvInterface

class tPvInterface:
    ePvInterfaceFirewire    = 1
    ePvInterfaceEthernet    = 2
    __ePvInterface_force_32 = 0xFFFFFFFF

class tPvCameraInfo(ctypes.Structure): pass
tPvCameraInfo._fields_ = [
      ('UniqueId', ctypes.c_ulong),         # Unique value for each camera
      ('SerialString', ctypes.c_char * 32), # Camera's serial number
      ('PartNumber', ctypes.c_ulong),       # Camera part number
      ('PartVersion', ctypes.c_ulong),      # Camera part version
      ('PermittedAccess', ctypes.c_ulong),  # A combination of tPvAccessFlags
      ('InterfaceId', ctypes.c_ulong),      # Unique value for each interface or bus
      ('InterfaceType', ctypes.c_byte),     # Interface type; see tPvInterface
      ('DisplayName', ctypes.c_char * 16),  # People-friendly camera name
      ('_reserved', ctypes.c_ulong * 4)]    # Always zero

def PvInitialize():
    return lib.PvInitialize()

def PvInitializeSync():
    import time
    status = PvInitialize()
    while PvCameraCount() == 0:
        time.sleep(0.250)
    return status

def PvUnInitialize():
    return lib.PvUnInitialize()

def PvCameraListEx():
    camlist = (tPvCameraInfoEx * 10)()
    return lib.PvCameraListEx(camlist, 10, None, 
                              ctypes.sizeof(tPvCameraInfoEx)), camlist
    
def PvCameraCount():
    return lib.PvCameraCount()

def PvCameraList():
    camlist = (tPvCameraInfo * 10)()
    return lib.PvCameraList(camlist, 10, None), camlist

if __name__ == '__main__':
    assert PvInitializeSync() == tPvErr.ePvErrSuccess

    count, cams = PvCameraList()
    for i in xrange(0, count):
        cam = cams[0]
        print cam.UniqueId
    assert PvUnInitialize() == tPvErr.ePvErrSuccess
