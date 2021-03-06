#! python

import sys
import os
import subprocess
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src')))
sys.path.append((os.path.dirname(os.path.abspath(__file__))))

import xunit.result
import xunit.suite
import xunit.case
import xunit.config
import unittest
import logging


class XUnitTested(xunit.case.XUnitCase):
	@classmethod
	def XUnitsetUpClass(cls):
		return

	@classmethod
	def XUnittearDownClass(cls):
		return

	def XUnitsetUp(self):
		return

	def XUnittearDown(self):
		return

	
	def test_case1(self):
		pass

	def test_casefail(self):
		self.assertEqual(1,0)
		return

	@unittest.skip("must skiped")
	def test_skip(self):
		return

	@unittest.expectedFailure
	def test_succwhenexpectfail(self):
		return
	


class XUnitTestResult(xunit.case.XUnitCase):
	def test_resultnotfailfast(self):
		sbase = xunit.suite.XUnitSuiteBase()
		# now for the name of current case
		mn = self.__module__
		cn = 'XUnitTested'
		sbase.LoadCase(mn +'.'+cn)

		# to set for it is not for 
		utcfg = xunit.config.XUnitConfig()
		utcfg.SetValue('global','failfast','',1)

		_res2 = None
		try:
			_res2 = xunit.result.XUnitResultBase(0)

			for s in sbase:
				s(_res2)
				if _res2.shouldStop:
					break

			self.assertEqual(_res2.Cases(),4)
			self.assertEqual(_res2.Succs(),1)
			self.assertEqual(_res2.Fails(),1)
			self.assertEqual(_res2.Skips(),1)
			self.assertEqual(_res2.UnexpectFails(),0)
			self.assertEqual(_res2.UnexpectSuccs(),1)
		finally:
			if _res2:
				_res2.RestoreLogOutput()
				del _res2
			_res2 = None
		return


	def test_resultfailfastwithskip(self):
		sbase = xunit.suite.XUnitSuiteBase()
		# now for the name of current case
		mn = self.__module__
		cn = 'XUnitTested'
		sbase.LoadCase(mn +'.'+cn+':'+'test_case1')
		sbase.LoadCase(mn +'.'+cn+':'+'test_skip')
		sbase.LoadCase(mn +'.'+cn+':'+'test_casefail')
		sbase.LoadCase(mn +'.'+cn+':'+'test_succwhenexpectfail')
		# to set for it is not for 
		utcfg = xunit.config.XUnitConfig()
		utcfg.SetValue('global','failfast','y',1)

		_res2 = None
		try:
			_res2 = xunit.result.XUnitResultBase(0)

			for s in sbase:
				s.run(_res2)
				if _res2.shouldStop:
					break

			self.assertEqual(_res2.Cases(),3)
			self.assertEqual(_res2.Succs(),1)
			self.assertEqual(_res2.Fails(),1)
			self.assertEqual(_res2.Skips(),1)
		finally:
			if _res2:
				_res2.RestoreLogOutput()
				del _res2
			_res2 = None
		return


	def test_resultfailfastfirst(self):
		sbase = xunit.suite.XUnitSuiteBase()
		# now for the name of current case
		mn = self.__module__
		cn = 'XUnitTested'
		sbase.LoadCase(mn +'.'+cn+':'+'test_casefail')
		sbase.LoadCase(mn +'.'+cn+':'+'test_case1')
		sbase.LoadCase(mn +'.'+cn+':'+'test_skip')
		sbase.LoadCase(mn +'.'+cn+':'+'test_succwhenexpectfail')
		# to set for it is not for 
		utcfg = xunit.config.XUnitConfig()
		utcfg.SetValue('global','failfast','y',1)

		_res2 = None
		try:
			_res2 = xunit.result.XUnitResultBase(0)

			for s in sbase:
				s.run(_res2)
				if _res2.shouldStop:
					break

			self.assertEqual(_res2.Cases(),1)
			self.assertEqual(_res2.Succs(),0)
			self.assertEqual(_res2.Fails(),1)
			self.assertEqual(_res2.Skips(),0)
		finally:
			if _res2:
				_res2.RestoreLogOutput()
				del _res2
			_res2 = None
		return


	def test_resultunexpectedfail(self):
		sbase = xunit.suite.XUnitSuiteBase()
		# now for the name of current case
		mn = self.__module__
		cn = 'XUnitTested'
		sbase.LoadCase(mn +'.'+cn+':'+'test_succwhenexpectfail')
		sbase.LoadCase(mn +'.'+cn+':'+'test_case1')
		sbase.LoadCase(mn +'.'+cn+':'+'test_skip')
		sbase.LoadCase(mn +'.'+cn+':'+'test_casefail')
		# to set for it is not for 
		utcfg = xunit.config.XUnitConfig()
		utcfg.SetValue('global','failfast','y',1)

		_res2 = None
		try:
			_res2 = xunit.result.XUnitResultBase(0)

			for s in sbase:
				s.run(_res2)
				if _res2.shouldStop:
					break

			self.assertEqual(_res2.Cases(),1)
			self.assertEqual(_res2.Succs(),0)
			self.assertEqual(_res2.Fails(),0)
			self.assertEqual(_res2.Skips(),0)
			self.assertEqual(_res2.UnexpectSuccs(),1)
		finally:
			if _res2:
				_res2.RestoreLogOutput()
				del _res2
			_res2 = None
		return

	def __CallProcessReturn(self,cmd):
		sp = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		ep = sp.stderr
		op = sp.stdout
		ls = []
		ls += ep.readlines()
		ls += op.readlines()
		ol = []
		for l in ls:
			ol.append(l.rstrip('\r\n'))
		return ol

	def __FindLineIdx(self,ls,s):
		i = 0
		idx = -1
		vpat = re.compile(s)
		for l in ls:
			if vpat.search(l):
				idx = i
				break
			i += 1
		return idx

	def test_errormsgerror(self):
		curpath = os.path.dirname(os.path.abspath(__file__))
		errpy = os.path.join(curpath,'test_errres.py')
		lss = self.__CallProcessReturn('python %s -v __main__.ErrorTest:test_error'%(errpy))
		idx = self.__FindLineIdx(lss,'test_error')
		self.assertTrue(idx>=0)
		idx = self.__FindLineIdx(lss,'test_error2')
		self.assertTrue(idx == -1)
		return


	def test_errormsgfast(self):
		curpath = os.path.dirname(os.path.abspath(__file__))
		errpy = os.path.join(curpath,'test_errres.py')
		lss = self.__CallProcessReturn('python %s -v -f'%(errpy))
		idx = self.__FindLineIdx(lss,'Traceback')
		self.assertTrue(idx>=0)
		idx = self.__FindLineIdx(lss[idx+1:],'Traceback')
		self.assertTrue(idx == -1)
		return

	def test_errormsgnotfast(self):
		curpath = os.path.dirname(os.path.abspath(__file__))
		errpy = os.path.join(curpath,'test_errres.py')
		lss = self.__CallProcessReturn('python %s -v'%(errpy))
		idx = self.__FindLineIdx(lss,'Traceback')
		self.assertTrue(idx>=0)
		idx = self.__FindLineIdx(lss[idx+1:],'Traceback')
		self.assertTrue(idx >= 0)
		return


def MainTest():
	verb = 1
	ff = False
	utcfg = xunit.config.XUnitConfig()
	if '-v' in sys.argv[1:] or '--verbose' in sys.argv[1:]:
		logging.basicConfig(level=logging.INFO,format="%(levelname)-8s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s")
		verb = 2
		utcfg.SetValue('global','debug.mode','y')
	else:
		logging.basicConfig(level=logging.WARNING,format="%(levelname)-8s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s")
	if '-f' in sys.argv[1:] or '--failfast' in sys.argv[1:]:
		ff = True
		utcfg.SetValue('global','failfast','y')
	suites = xunit.suite.XUnitSuiteBase()
	suites.LoadCase('__main__.XUnitTestResult')

	unittest.TextTestRunner(sys.stderr,descriptions=True, verbosity=verb ,failfast=ff, buffer=False, resultclass=None).run(suites)
	return

if __name__ == '__main__':
	MainTest()


