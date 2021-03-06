#! python


import sys
import os
import re
from optparse import OptionParser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src')))
sys.path.append((os.path.dirname(os.path.abspath(__file__))))

import xunit.result
import xunit.suite
import xunit.case
import xunit.config
import logging
import unittest
import xunit.utils.cls

class ResultSpecError:
	pass

class FailTest(xunit.case.XUnitCase):
	def __call(self,num):
		if num > 1:
			self.__call(num-1)
		else:
			self.assertEqual(1,0)
		return
	def test_fail(self):
		self.__call(5)
		return

	def test_fail2(self):
		self.__call(3)
		return



class ErrorTest(xunit.case.XUnitCase):
	def __errcall(self,num):
		if num > 1:
			self.__errcall(num-1)
		else:
			raise ResultSpecError()
		return

	def test_error(self):
		self.__errcall(3)
		return

	def test_error2(self):
		self.__errcall(4)
		return


def Usage(opt,ec,msg=None):
	fp = sys.stderr
	if ec == 0:
		fp = sys.stdout
	if msg :
		fp.write('%s\n'%(msg))
	opt.print_help(fp)
	sys.exit(ec)

def Parse_Callback(option, opt_str, value, parser):
	#print 'option %s opt_str %s value %s parser %s'%(repr(option), repr(opt_str), repr(value), repr(parser))
	if opt_str == '-D' or opt_str == '--variable':
		if not hasattr(parser.values,'variables'):
			parser.values.variables = []
		if value :
			parser.values.variables.append(value)
	elif opt_str == '-V' or opt_str == '--debug':
		if not hasattr(parser.values,'variables'):
			parser.values.variables = []
		parser.values.variables.append('[global].xmllevel=5')
		
	else:
		Usage(parser,3,'unknown option (%s)'%(option))


def SplitVariables(v):
	#logging.info('v %s'%(v))
	p = '\[([^]]+)\]\.([^=]+)=(.*)'
	vpat = re.compile(p)
	m = vpat.match(v)
	if not m:
		raise exception.XUnitException('(%s) not match (%s)'%(v,p))
	sec = m.group(1)
	opt = m.group(2)
	val = m.group(3)
	return sec,opt,val
	

def SetOuterVariables(utcfg,variables=[]):
	# first to parse the variable
	for va in variables:
		s,o,v = SplitVariables(va)
		utcfg.SetValue(s,o,v,1)
	return


def maintest():
	args = OptionParser()
	args.add_option('-v','--verbose',action='store_true',dest='verbose',help='verbose mode')
	args.add_option('-f','--failfast',action="store_true",dest="failfast",help="failfast mode")
	args.add_option('-D','--variable',action="callback",callback=Parse_Callback,type="string",nargs=1,help='specify a variable format is [section].option=value')
	args.add_option('-V','--debug',action="callback",callback=Parse_Callback,help='debug mode ')

	options ,nargs = args.parse_args(sys.argv[1:])

	_vars = []
	utcfg = xunit.config.XUnitConfig()

	
	if options.verbose:
		_vars.append('[global].debug.mode=y')
		_vars.append('[.__main__].xmllevel=5')
		logging.basicConfig(level=logging.INFO,format="%(levelname)-8s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s")

	if options.failfast:
		_vars.append('[global].failfast=y')

	#logging.info('opt %r'%(options))
	if hasattr(options,'variables'):
		_vars.extend(options.variables)

	SetOuterVariables(utcfg,_vars)


	suites = xunit.suite.XUnitSuiteBase()
	if len(nargs) > 0:
		for cn in nargs:
			suites.LoadCase(cn)
	else:
		# now to get the module
		mm = __import__(__name__)
		for objname in dir(mm):
			obj = getattr(mm,objname)
			if isinstance(obj, type) and issubclass(obj,xunit.case.XUnitCase):
				cn = xunit.utils.cls.GetClassName(obj)
				suites.LoadCase(cn)

	# now we should set for the case verbose is none we debug our self information
	_res = xunit.result.XUnitResultBase()
	for s in suites:
		s(_res)
		if _res.shouldStop:
			break
	_ret = -1
	if _res.Fails() == 0 and _res.UnexpectFails() ==0 and _res.UnexpectSuccs() == 0:
		_ret = 0

	_res.ResultAll()

	return _ret



if __name__ == '__main__':
	maintest()
