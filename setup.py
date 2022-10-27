from distutils.core import setup
import py2exe
import pygubu
import tkinter
import BeautifulSoup
import lib, plugins

setup(windows=['SSCan.py'],
      options={
          'py2exe':{
              'packages':['BeautifulSoup','pygubu','tkinter','lib','plugins']}
          })
