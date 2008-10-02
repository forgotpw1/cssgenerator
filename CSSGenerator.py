#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# CSSGenerator <>
# Python script to extract color properties from a website and create a css file with them
#
# Copyright (C) 2008 Manrique López
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Library or Lesser General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

__author__       = 'J. Manrique López <http://www.jsmanrique.es/>'
__copyright__    = 'Copyright 2007, J. Manrique López'
__license__      = 'GNU General Public License'
__version__      = '0.0.1'

import cssutils
from cssutils.script import CSSCapture
import sys
import urllib2
from BeautifulSoup import BeautifulSoup

class FetchURL:
	def __init__(self,url):
		self.url = url		
		userAgent = 'Mozilla/5.0 (X11; U; Linux i686; es-ES; rv:1.9.0.3) Gecko/2008092510 Ubuntu/8.04 (hardy) Firefox/3.0.3'
		headers = {'User-Agent': userAgent}
		req = urllib2.Request(url, None, headers)
		response = urllib2.urlopen(req)
		self.data = response.read()

	def data(self):	
		return self.data

class CSSGenerator:
	def __init__(self, url):
		self.generatedCSS = ''
		self.url = url
		#self.fetchedCSS = cssutils.parseUrl(url)
		
	def generateCSS(self):
		c = CSSCapture(ua='Mozilla/5.0 (X11; U; Linux i686; es-ES; rv:1.9.0.3) Gecko/2008092510 Ubuntu/8.04 (hardy) Firefox/3.0.3')
		
		sheetList = c.capture(self.url)
		
		page = FetchURL(self.url).data
		soup = BeautifulSoup(page)
		styleElementList = soup.findAll('style')
		for styleElement in styleElementList:
			css = styleElement.renderContents()
			sheetList.append(cssutils.parseString(css))
				
		for sheet in sheetList:
			if not('handheld' in sheet.media.mediaText or 'print' in sheet.media.mediaText) or 'screen' in sheet.media.mediaText:
				for rule in sheet:
					if rule.type == 1:
						for property in rule.style:
							if property.name == 'color' or property.name == 'background-color':
								self.generatedCSS = self.generatedCSS + rule.selectorText + '{'+ property.name +':' + property.value +';}\n'
		return self.generatedCSS

if __name__ == '__main__':
	try:
		css = CSSGenerator(sys.argv[1]).generateCSS()
		print css
		cssFile = open(sys.argv[2],'w')
		cssFile.write(css)
		cssFile.close()
	except:
		print 'Usage:\n $python CSSGenerator.py [URL] [filename]'
