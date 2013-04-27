from camera import Camera
from camera import PixelFormat
from camera import AcquisitionMode
from camera import ConfigFileIndex
from camera import ExposureMode
import time
import unittest

class TestCamera(unittest.TestCase):
	def setUp(self):
		self.cam = Camera()
		self.cam.initialize()
		time.sleep(500)
		self.cam.start()
	
	def tearDown(self):
		self.cam.stop()
		self.cam.uninitialize()	
		
	def testPixelFormat(self):
		self.cam.setPixelFormat(PixelFormat.Mono8)
		pf = self.cam.getPixelFormat()
		self.assertEqual(pf,"Mono8")
		
		self.cam.setPixelFormat(PixelFormat.Bayer8)
		pf = self.cam.getPixelFormat()
		self.assertEqual(pf,"Bayer8")
		
		self.cam.setPixelFormat(PixelFormat.Bayer16)
		pf = self.cam.getPixelFormat()
		self.assertEqual(pf,"Bayer16")
		
		self.cam.setPixelFormat(PixelFormat.Rgb24)
		pf = self.cam.getPixelFormat()
		self.assertEqual(pf,"Rgb24")
		
		self.cam.setPixelFormat(PixelFormat.Bgr24)
		pf = self.cam.getPixelFormat()
		self.assertEqual(pf,"Bgr24")
		
		self.cam.setPixelFormat(PixelFormat.Rgba32)
		pf = self.cam.getPixelFormat()
		self.assertEqual(pf,"Rgba32")
		
		self.cam.setPixelFormat(PixelFormat.Bgra32)
		pf = self.cam.getPixelFormat()
		self.assertEqual(pf,"Bgra32")		
		
	def testAcquisitionMode(self):
		self.cam.setAcquisitionMode(AcquisitionMode.Continuous)
		am = self.cam.getAcquisitionMode()
		self.assertEqual(am,"Continuous")
		
		self.cam.setAcquisitionMode(AcquisitionMode.SingleFrame)
		am = self.cam.getAcquisitionMode()
		self.assertEqual(am,"SingleFrame")
		
		self.cam.setAcquisitionMode(AcquisitionMode.MultiFrame)
		am = self.cam.getAcquisitionMode()
		self.assertEqual(am,"MultiFrame")
		
		self.cam.setAcquisitionMode(AcquisitionMode.Recorder)
		am = self.cam.getAcquisitionMode()
		self.assertEqual(am,"Recorder")
		
	def testConfigFileIndex(self):
		self.cam.setConfigFileIndex(ConfigFileIndex.Factory)
		cfi = self.cam.getConfigFileIndex()
		self.assertEqual(cfi,"Factory")
		
		self.cam.setConfigFileIndex(ConfigFileIndex.Index1)
		cfi = self.cam.getConfigFileIndex()
		self.assertEqual(cfi,"1")
		
		
		self.cam.setConfigFileIndex(ConfigFileIndex.Index2)
		cfi = self.cam.getConfigFileIndex()
		self.assertEqual(cfi,"2")
		
		self.cam.setConfigFileIndex(ConfigFileIndex.Index3)
		cfi = self.cam.getConfigFileIndex()
		self.assertEqual(cfi,"3")
		
		self.cam.setConfigFileIndex(ConfigFileIndex.Index4)
		cfi = self.cam.getConfigFileIndex()
		self.assertEqual(cfi,"4")
		
		self.cam.setConfigFileIndex(ConfigFileIndex.Index5)
		cfi = self.cam.getConfigFileIndex()
		self.assertEqual(cfi,"5")
		
	def testGetTotalBytesPerFrame(self):
		tbbf = self.cam.getTotalBytesPerFrame()
		self.assertIsInstance(tbbf,int)
		
	def testHeight(self):
		self.cam.setHeight(300)
		h = self.cam.getHeight()
		self.assertEqual(h,300)
		
	def testWidth(self):
		self.cam.setWidth(400)
		w = self.cam.getWidth()
		self.assertEqual(w,400)
		
	def testRegionX(self):
		self.cam.setRegionX(150)
		rx = self.cam.getRegionX()
		self.assertEqual(rx,150)
		
	def testRegionY(self):
		self.cam.setRegionY(200)
		ry = self.cam.getRegionY()
		self.assertEqual(ry,200)
		
	def testGamma(self):
		self.cam.setGamma(0)
		g = self.cam.getGamma()
		self.assertEqual(g,0)
	
	def testExposureMode(self):
		self.cam.setExposureMode(ExposureMode.Manual)
		em = self.cam.getExposureMode()
		self.assertEqual(em,"Manual")
		
		self.cam.setExposureMode(ExposureMode.Auto)
		em = self.cam.getExposureMode()
		self.assertEqual(em,"Auto")
		
		self.cam.setExposureMode(ExposureMode.AutoOnce)
		em = self.cam.getExposureMode()
		self.assertEqual(em,"AutoOnce")
		
		self.cam.setExposureMode(ExposureMode.External)
		em = self.cam.getExposureMode()
		self.assertEqual(em,"External")
		
		
	
if __name__ == "__main__":
	unittest.main() 
