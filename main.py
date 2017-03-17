# main.py -- put your code here!

import time
import micropython
import random

import fct
#from stm_usb_port import USB_Port
#from json_pkt import JSON_Packet

micropython.alloc_emergency_exception_buf(100)

armed = False
triggerReceived = False
#skipReceivingFile = False

class TimingErr(Exception):
	pass


def callbackTrigger(line):
	global triggerReceived
	triggerReceived = True

def callbackTrigger2():
	global triggerReceived
	triggerReceived = True

def callbackRcvFile():
	global skipReceivingFile
	skipReceivingFile = True

def callbackArm():
	global armed
	armed = True

def main():

	global armed
	global triggerReceived
	global skipReceivingFile
	
	laser = pyb.Pin('Y1',pyb.Pin.OUT_PP,pull=pyb.Pin.PULL_UP)
	laser.value(1)
	laserLED = pyb.LED(4)
	
#	serial_port = USB_Port()
	armedLED = pyb.LED(3)			#indicates when the system is waiting for a trigger
	triggerLED = pyb.LED(2)
	
	
	extint = pyb.ExtInt('X1', pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_DOWN, callbackTrigger)
	print('before switch definition')
	sw = pyb.Switch()     			
#	sw.callback(callbackRcvFile)			#by pressing the switch the reception of the json file can be skiped
	print('after switch initialisations')
	seqs = None
#	jpkt = JSON_Packet(serial_port)
#	print('before while not skipReceivingFile')
#	while not skipReceivingFile:
#		print(skipReceivingFile)
#		byte = serial_port.read_byte()
#		if byte is not None:
#			seqs = jpkt.process_byte(byte)
#			if seqs is not None:
#				jpkt.send(seqs)
#				break
#		time.sleep_ms(100)
	print('before loading file')
	if seqs is  None:
		seqs = fct.load("sequences.json")
	print('before changin switch function')
	
	print('after loading json file')	

	seqName = "sequence0" # + random.randrange(len(seqs))

	sw.callback(callbackArm)
	while not armed:
		time.sleep(0.5)

	while True:
		numOfEvents = len(seqs[seqName])	
		rangeOfEvents = range(0,numOfEvents)
		eventName = ["event0"]
		T = [int(1/seqs[seqName][eventName[0]]["frequency"]*1000000)]
		onset = [seqs[seqName][eventName[0]]["onset"]*1000]
		duration = [(seqs[seqName][eventName[0]]["onset"]+seqs[seqName][eventName[0]]["duration"])*1000]
		for i in range(1,numOfEvents):
			eventName.append("event" + str(i))
			T.append(int(1/seqs[seqName][eventName[i]]["frequency"]*1000000))
			onset.append(seqs[seqName][eventName[i]]["onset"]*1000)
			duration.append((seqs[seqName][eventName[i]]["onset"]+seqs[seqName][eventName[i]]["duration"])*1000)

		armedLED.on()

		sw.callback(callbackTrigger2)			#for test purposes the switch can be used to trigger
		extint.enable()
		while not triggerReceived:
			time.sleep_us(1)

		start_ticks = time.ticks_us()
		triggerLED.on()
		armedLED.off()
		print('trigger received')
		extint.disable()
		
		for i in rangeOfEvents:
			
			scheduled_time = time.ticks_add(start_ticks,onset[i])
			end_time = time.ticks_add(start_ticks,duration[i])
			
			while time.ticks_diff(scheduled_time,end_time) < 0:
				now = time.ticks_us()
				if time.ticks_diff(now,scheduled_time) < 0:
					time.sleep_us(time.ticks_diff(scheduled_time,now))
					fct.laserPulse(laser,seqs[seqName][eventName[i]]["pulsewidth"],laserLED)
				elif time.ticks_diff(now,scheduled_time) == 0:
					fct.laserPulse(laser,seqs[seqName][eventName[i]]["pulsewidth"],laserLED)
				elif time.ticks_diff(now,scheduled_time) > 0:
					fct.laserPulse(laser,seqs[seqName][eventName[i]]["pulsewidth"],laserLED)
					try:				
						raise TimingErr("Missed scheduled onset time of {0}:{1} by {2} us ".format(seqName,
								eventName[i],time.ticks_diff(now,scheduled_time)))
					except TimingErr:
						print("Missed scheduled onset time of {0}:{1} by {2} us ".format(seqName,
							eventName[i],time.ticks_diff(now,scheduled_time)))
				scheduled_time = time.ticks_add(scheduled_time,T[i])

#		jpkt.send(seqs[seqName])

		triggerReceived = False
		triggerLED.off()

		sw.callback(callbackArm)
		armed = False
		while not armed:
			time.sleep(0.5)


main()
