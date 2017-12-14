# -*- coding: utf-8 -*-
#from loadSRTM import *
import loadSRTM 
import os
import sys

print(sys.path)
print(os.path.abspath(os.path.dirname(__file__)))
print(sys.path)

boundingbox = [-68.0, -16.0, -10.0, 20.0]

srtmfiles = loadSRTM(boundingbox)

srtmfiles.createFileList()

