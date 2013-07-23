#! python

'''
	this is the file for the ptz get and set
'''

import struct

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..')))
import xunit.utils.exception
import xunit.extlib.sdkproto.syscp as syscp

class SdkPtzInvalidError(xunit.utils.exception.XUnitException):
	pass

class SdkPtzOutRangeError(xunit.utils.exception.XUnitException):
	pass

SYSCODE_CTL_PTZ_REQ=1077
SYSCODE_CTL_PTZ_RESP=1078

SYS_PTZCMD_STOP=0
SYS_PTZCMD_ZOOM_TELE=1
SYS_PTZCMD_ZOOM_WIDE=2
SYS_PTZCMD_FOCUS_NEAR=3
SYS_PTZCMD_IRIS_LARGE=4
SYS_PTZCMD_IRIS_SMALL=5
SYS_PTZCMD_AUXON=6
SYS_PTZCMD_AUXOFF=7
SYS_PTZCMD_AUTOPANON=8
SYS_PTZCMD_AUTOPANOFF=9
SYS_PTZCMD_UP=10
SYS_PTZCMD_DOWN=11
SYS_PTZCMD_LEFT=12
SYS_PTZCMD_RIGHT=13
SYS_PTZCMD_RIGHTUP=14
SYS_PTZCMD_LEFTUP=15
SYS_PTZCMD_RIGHTDOWN=16
SYS_PTZCMD_LEFTDOWN=17
SYS_PTZCMD_GOTOPRESET=18
SYS_PTZCMD_SETPRESET=19
SYS_PTZCMD_CLEARPRESET=20
SYS_PTZCMD_LIGHT_ON=21
SYS_PTZCMD_LIGHT_OFF=22
SYS_PTZCMD_STARTTOUR=23
SYS_PTZCMD_STOPTOUR=24
SYS_PTZCMD_3DCONTROL=200
SYS_PTZCMD_NR=255

class SdkPtz(syscp.SysCP):
	def __init__(self):
		syscp.SysCP.__init__(self)
		return
	def __del__(self):
		syscp.SysCP.__del__(self)
		return

	def __FormatPtzCommand(self,ptzid,cmd,param1=0,param2=0,param3=0,param4=0):
		rbuf = ''
		rbuf += struct.pack('>II',ptzid,cmd)
		rbuf += struct.pack('>IIII',param1,param2,param3,param4)
		return rbuf

	def UpPtz(self,ptzid,speed):
		seqbuf = self.__FormatPtzCommand(ptzid,SYS_PTZCMD_UP,speed)
		return self.FormatSysCp(SYSCODE_CTL_PTZ_REQ,seqbuf)

	def DownPtz(self,ptzid,speed):
		seqbuf = self.__FormatPtzCommand(ptzid,SYS_PTZCMD_DOWN,speed)
		return self.FormatSysCp(SYSCODE_CTL_PTZ_REQ,seqbuf)

	def RightPtz(self,ptzid,speed):
		seqbuf = self.__FormatPtzCommand(ptzid,SYS_PTZCMD_RIGHT,speed)
		return self.FormatSysCp(SYSCODE_CTL_PTZ_REQ,seqbuf)
		
	def LeftPtz(self,ptzid,speed):
		seqbuf = self.__FormatPtzCommand(ptzid,SYS_PTZCMD_LEFT,speed)
		return self.FormatSysCp(SYSCODE_CTL_PTZ_REQ,seqbuf)
	
