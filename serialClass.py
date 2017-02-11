# -*- coding: cp1252 -*-
import serial
from fileFunctions import logTEXT
from accessClass import accessHANDLER
from time import sleep

#serconn = serial.Serial('/dev/ttyACM0',9600,timeout=1)


class Singleton(object):
  _instance = None
  def __new__(class_, *args, **kwargs):
    if not isinstance(class_._instance, class_):
        class_._instance = object.__new__(class_, *args, **kwargs)
    return class_._instance
	
class serialCOMM(Singleton):
	serconn = serial.Serial('/dev/ttyACM0',9600,timeout=1) #,timeout=30
	acH = accessHANDLER()
	

	def openCONN(self):
		if not self.serconn.isOpen():
			try:
				print("avattu portti uusiksi")
				self.serconn.open()
			except serial.SerialException:
				file.logTEXT("Error: Serial connection could not be established")

	def closeCONN(self):
		self.serconn.close()
		
##########################################################################################
################################# Sarjaportin viestihaku #################################
##########################################################################################
	def getDATA(self):
		s = ""
		try:
			s = self.serconn.readline()
			s = s[:-1]
		except serial.SerialTimeoutException:
			file.logTEXT("Error: Serial connection timeout")
			s = "EX"
		except serial.SerialException:
			file.logTEXT("Error: Serial connection terminated")
			s = "EX"
		finally:
			return s
			
##########################################################################################
################################ Sarjaportin viestifunktio ###############################
############ Volume 0-255, on_time int ms, amount = int määrä, off_time int ms ###########
##########################################################################################
			
	def writeDATA(self, COMMAND, VOLUME = 255, ON_TIME = 500, AMOUNT = 1, OFF_TIME = 0):
		if not self.acH.accessSER():	# Odottaa vuoroa (timeout 30sec)
			return
		self.openCONN()
		#sleep(0.2) # viive jotta edelliset viestit ovat varmasti loppuneet
		
		if COMMAND == 'T':
			self.serconn.write("T")
			
		if COMMAND == 'G':
			self.serconn.write("G")

		if COMMAND == 'B':
			for i in range(0, AMOUNT):
				self.serconn.write("B" + str(VOLUME) + ":" + str((ON_TIME)) + "X")
				sleep((float(OFF_TIME) + float(ON_TIME)) / 1000)
		
		self.acH.exitSER()