#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# --
import sys
import getopt
# -- lib
from lib.utils.printer import *
from lib.utils.usage import *
from lib.utils.check import *
from lib.utils.settings import *
from lib.request.ragent import *
from lib.utils.exception import *
# -- modules
from lib.handler.audit import *
from lib.handler.brute import *
from lib.handler.attacks import *
from lib.handler.crawler import *
from lib.handler.fullscan import *
from lib.handler.disclosure import *
from lib.handler.fingerprint import *

class wascan(object):
	""" WAScan """
	def main(self,a_method,a_url,a_header,a_data,a_scan,parent_app):
                kwargs = {}
                setApplication(parent_app)
		verbose = False
		# starting
		url = CUrl(a_url)
		parse = SplitURL(url)
		kwargs['data'] = a_data
		kwargs['method'] = a_method
		if 'Cookie' in a_header.keys():
			kwargs['cookie'] = a_header['Cookie']
			a_header.pop('Cookie',None)
		if 'User-Agent' in a_header.keys():
			kwargs['agent'] = a_header['User-Agent']
			a_header.pop('User-Agent',None)
		kwargs['headers'] = a_header
		
		try:
			PTIME(url)
			if a_scan == '0 : Finger Print':
				Fingerprint(kwargs,url).run()
			if a_scan == '1 : Attacks':
				Attacks(kwargs,url,kwargs['data'])
			if a_scan == '2 : Audit':
				Audit(kwargs,url,kwargs['data'])
			if a_scan == '3 : Brute Force':
				Brute(kwargs,url,kwargs['data'])
			if a_scan == '4 : Disclosure':
				Disclosure(kwargs,url,kwargs['data']).run()
			# full scan  
			if a_scan == '5 : Full Scan':
				info('Starting full scan module...')
				Fingerprint(kwargs,url).run()
				for u in Crawler().run(kwargs,url,kwargs['data']):
					test('Testing URL: %s'%(u))
					if '?' not in url:
						warn('Not found query in this URL... Skipping..')
					if type(u[0]) is tuple:
						kwargs['data'] = u[1]
						FullScan(kwargs,u[0],kwargs['data'])
					else:
						FullScan(kwargs,u,kwargs['data'])
				Audit(kwargs,parse.netloc,kwargs['data'])
				Brute(kwargs,parse.netloc,kwargs['data'])
		except WascanUnboundLocalError,e:
			pass

