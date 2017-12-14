# -*- coding: utf-8 -*-
from nose.tools import *
#from loadSRTM.loadSRTM import *
from .context import loadSRTM

def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_basic():
    print "I RAN!"

def test_boundingbox_1():
    #bbox: left, bottom, right, top
    boundingbox = [-68.0, -16.0, -10.0, 20.0]
    srtmfiles = loadSRTM(boundingbox)
    assert_equal(len(srtmfiles.createFileList()), 6)

def test_boundingbox_1_1():
    boundingbox = [-68.0, -16.0, -10.0, 20.0]
    srtmfiles = loadSRTM(boundingbox)
    assert_items_equal(srtmfiles.createFileList(), ["w100s10", "w100n40", "w60s10", "w60n40",
        "w20s10", "w20n40"])

def test_boundingbox_2():
    boundingbox = [-185.0, 20.0, -120.0, 55.0]
    srtmfiles = loadSRTM(boundingbox)
    assert_equal(len(srtmfiles.createFileList()), 4)

def test_boundingbox_2_1():
    boundingbox = [-185.0, 20.0, -120.0, 55.0]
    srtmfiles = loadSRTM(boundingbox)
    assert_items_equal(srtmfiles.createFileList(), ["w180n40", "w180n90", "w140n40", "w140n90"])
        

def test_boundingbox_3():
    boundingbox = [110.0, -26.0, 175.0, 45.0]
    srtmfiles = loadSRTM(boundingbox)
    assert_equal(len(srtmfiles.createFileList()), 6)

def test_boundingbox_3_1():
    boundingbox = [110.0, -26.0, 175.0, 45.0]
    srtmfiles = loadSRTM(boundingbox)
    assert_items_equal(srtmfiles.createFileList(), ["e100s10", "e100n40", "e100n90", "e140s10",
        "e140n40", "e140n90"])
