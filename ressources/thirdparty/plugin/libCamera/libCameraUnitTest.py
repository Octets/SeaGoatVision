from camera import Camera
from camera import PixelFormat
from camera import AcquisitionMode
from camera import ConfigFileIndex
from camera import ExposureMode
from camera import ExposureAutoMode
from camera import ExposureAutoAlgMode
from camera import GainMode
from camera import GainAutoMode
from camera import WhitebalMode
from camera import WhitebalAutoMode

import time
import unittest

class TestCamera(unittest.TestCase):
	def setUp(self):
		self.cam = Camera()
		self.cam.initialize()
		time.sleep(1000)
		#self.cam.start()
	
	def tearDown(self):
		#self.cam.stop()
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
		
	#Tests for ROI methods
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
	#End Tests for ROI methods
		
	def testGamma(self):
		with self.assertRaises(RuntimeError):
			self.cam.setGamma(0)
			
		self.cam.setGamma(0.45)
		g = self.cam.getGamma()
		self.assertTrue(0.449 < g and g < 0.451)
		
		self.cam.setGamma(0.5)
		g = self.cam.getGamma()
		self.assertTrue(0.499 < g and g < 0.501)
		
		self.cam.setGamma(0.7)
		g = self.cam.getGamma()
		self.assertTrue(0.699 < g and g < 0.701)
		
		self.cam.setGamma(1)
		g = self.cam.getGamma()
		self.assertTrue(0.999 < g and g < 1.001)
	
	#Tests for Exposure methods
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
	
	def testExposureValue(self):
		with self.assertRaises(RuntimeError):
			self.cam.setExposureValue(1000)
		
		self.cam.setExposureMode(ExposureMode.Manual)
		
		with self.assertRaises(RuntimeError):
			self.cam.setExposureValue(20)
			
		self.cam.setExposureValue(1000)
		value = self.cam.getExposureValue()
		self.assertEqual(value,1000)
		
	
	def testExposureAutoMode(self):
		with self.assertRaises(RuntimeError):
			self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoAdjustTol,-1)
			
		with self.assertRaises(RuntimeError):
			self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoAdjustTol,51)
			
		self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoAdjustTol,10)
		eaat = self.cam.getExposureAutoMode(ExposureAutoMode.ExposureAutoAdjustTol)
		self.assertEqual(eaat,10)
		
		with self.assertRaises(RuntimeError):
			self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoMin,44)
		
		self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoMin,50)
		eamin = self.cam.getExposureAutoMode(ExposureAutoMode.ExposureAutoMin)
		self.assertEqual(eamin,50)
		
		with self.assertRaises(RuntimeError):
			self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoMax,44)
		
		self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoMax,100)
		eamax = self.cam.getExposureAutoMode(ExposureAutoMode.ExposureAutoMax)
		self.assertEqual(eamax,100)
		
		with self.assertRaises(RuntimeError):
			self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoRate,-1)
		with self.assertRaises(RuntimeError):
			self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoRate,101)
			
		self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoRate,40)
		ear = self.cam.getExposureAutoMode(ExposureAutoMode.ExposureAutoRate)
		self.assertEqual(ear,40)
		
		with self.assertRaises(RuntimeError):
			self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoOutliers,-1)
		
		with self.assertRaises(RuntimeError):
			self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoOutliers,10001)
		
		self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoOutliers,50)
		eao = self.cam.getExposureAutoMode(ExposureAutoMode.ExposureAutoOutliers)
		self.assertEqual(eao,50)
		
		with self.assertRaises(RuntimeError):
			self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoTarget,-1)
		with self.assertRaises(RuntimeError):
			self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoTarget,101)
		
		self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoTarget,60)
		eat = self.cam.getExposureAutoMode(ExposureAutoMode.ExposureAutoTarget)
		self.assertEqual(eat,60)
		
		with self.assertRaises(RuntimeError):
			self.cam.setExposureAutoMode(ExposureAutoMode.ExposureAutoAlg,20)
		
		with self.assertRaises(RuntimeError):
			self.cam.getExposureAutoMode(ExposureAutoMode.ExposureAutoAlg)
	
	
	def testExposureAutoAlgMode(self):
		self.cam.setExposureAutoAlgMode(ExposureAutoAlgMode.FitRange)
		eaam = self.cam.getExposureAutoAlgMode()		
		self.assertEqual(eaam,"FitRange")
		
		self.cam.setExposureAutoAlgMode(ExposureAutoAlgMode.Mean)
		eaam = self.cam.getExposureAutoAlgMode()		
		self.assertEqual(eaam,"Mean")
		
	
	#End tests for Exposure methods
	#Tests for Gain methods
	
	def testGainMode(self):
		self.cam.setGainMode(GainMode.Manual)
		gm = self.cam.getGainMode()
		self.assertEqual(gm,"Manual")
		
		self.cam.setGainMode(GainMode.Auto)
		gm =self.cam.getGainMode()
		self.assertEqual(gm,"Auto")
		
		self.cam.setGainMode(GainMode.AutoOnce)
		gm = self.cam.getGainMode()
		self.assertEqual(gm, "AutoOnce")		
			
	
	def testGainAutoMode(self):
		with self.assertRaises(RuntimeError):
			self.cam.setGainAutoMode(GainAutoMode.GainAutoAdjustTol,-1)
			
		with self.assertRaises(RuntimeError):
			self.cam.setGainAutoMode(GainAutoMode.GainAutoAdjustTol,101)
			
		self.cam.setGainAutoMode(GainAutoMode.GainAutoAdjustTol,45)
		gaat = self.cam.getGainAutoMode(GainAutoMode.GainAutoAdjustTol)
		self.assertEqual(gaat,45)
		
		
		
		
	
	def testGainValue(self):
		self.cam.setGainValue(5)
		gv = self.cam.getGainValue()
		self.assertTrue(gv,5)
		
		with self.assertRaises(RuntimeError):
			self.cam.setGainValue(-1)
		
		with self.assertRaises(RuntimeError):
			self.cam.setGainValue(33)
		
		
	#End Tests for Gain methods
	
	def testHue(self):
		with self.assertRaises(RuntimeError):
			self.cam.setHue(-41)
		
		with self.assertRaises(RuntimeError):
			self.cam.setHue(41)
			
		self.cam.setHue(30)
		h = self.cam.getHue()
		self.assertEqual(h,30)
		
			
	def testSaturation(self):
		with self.assertRaises(RuntimeError):
			self.cam.setSaturation(-1)
		with self.assertRaises(RuntimeError):
			self.cam.setSaturation(2.5)
		self.cam.setSaturation(0.5)
		s = self.cam.getSaturation()
		
		self.assertEqual(s,0.5)		
		
	def testWhitebalMode(self):
		self.cam.setWhitebalMode(WhitebalMode.Manual)
		wbm = self.cam.getWhitebalMode()
		self.assertEqual(wbm,"Manual")
		
		self.cam.setWhitebalMode(WhitebalMode.Auto)
		wbm = self.cam.getWhitebalMode()
		self.assertEqual(wbm,"Auto")
		
		self.cam.setWhitebalMode(WhitebalMode.AutoOnce)
		wbm = self.cam.getWhitebalMode()
		self.assertEqual(wbm,"AutoOnce")		
		
	
	#Tests for White balance methods
	def testWhitebalAutoMode(self):
		with self.assertRaises(RuntimeError):
			self.cam.setWhitebalAutoMode(WhitebalAutoMode.WhitebalAutoAdjustTol,-1)
			
		with self.assertRaises(RuntimeError):
			self.cam.setWhitebalAutoMode(WhitebalAutoMode.WhitebalAutoAdjustTol,51)
			
		with self.assertRaises(RuntimeError):
			self.cam.setWhitebalAutoMode(WhitebalAutoMode.WhitebalAutoRate,-1)
			
		with self.assertRaises(RuntimeError):
			self.cam.setWhitebalAutoMode(WhitebalAutoMode.WhitebalAutoRate,101)
			
		self.cam.setWhitebalAutoMode(WhitebalAutoMode.WhitebalAutoAdjustTol,49)
		waam = self.cam.getWhitebalAutoMode(WhitebalAutoMode.WhitebalAutoAdjustTol)
		
		self.assertEqual(waam,49)
		
		self.cam.setWhitebalAutoMode(WhitebalAutoMode.WhitebalAutoRate,51)
		waam = self.cam.getWhitebalAutoMode(WhitebalAutoMode.WhitebalAutoRate)
		
		self.assertEqual(waam,51)
		
		
	def testWhitebalValueRed(self):
		with self.assertRaises(RuntimeError):
			self.cam.setWhitebalValueRed(79)
			
		with self.assertRaises(RuntimeError):
			self.cam.setWhitebalValueRed(301)
			
		self.cam.setWhitebalValueRed(100)
		wbrv = self.cam.getWhitebalValueRed();
		self.assertEqual(wbrv,100)
		
	
	def testWhitebalValueBlue(self):
		with self.assertRaises(RuntimeError):
			self.cam.setWhitebalValueBlue(79)
			
		with self.assertRaises(RuntimeError):
			self.cam.setWhitebalValueBlue(301)
			
		self.cam.setWhitebalValueBlue(90)
		wbvb = self.cam.getWhitebalValueBlue();
		self.assertEqual(wbvb,90)
		
	
if __name__ == "__main__":
	unittest.main() 
