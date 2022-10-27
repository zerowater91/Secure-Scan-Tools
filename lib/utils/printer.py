#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from lib.utils.colors import *
from lib.utils.unicode import *
import tkinter as tk

application = None

def setApplication(arg):
        global application
        application = arg

def plus(string,flag="[+]"):
        application.response_Text.insert(tk.END,"{} {}\n".format(
		flag,
		ucode(string)
		))

def less(string,flag="[-]"):
	application.response_Text.insert(tk.END,"{} {}\n".format(
		flag,
		ucode(string)
		))

def warn(string,flag="[!]"):
	application.response_Text.insert(tk.END,"{} {}\n".format(
		flag,
		ucode(string)
		))

def test(string,flag="[*]"):
	application.response_Text.insert(tk.END,"{} {}\n".format(
		flag,
		ucode(string)
		))
def info(string,flag="[i]"):
	application.response_Text.insert(tk.END,"{} {}\n".format(
		flag,
		ucode(string)
		))

def more(string,flag="|"):
	application.response_Text.insert(tk.END,"{}  {}\n".format(
		flag,
		ucode(string)
		))

def null():
	print ""
