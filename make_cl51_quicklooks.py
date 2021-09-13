#!/usr/bin/env python
# coding: utf-8

import sys, getopt

import cl51_plotutils as cl51
import os, getpass, glob
import numpy as np


user = getpass.getuser()


def main(argv):
   inputfile = ''
   figpath = ''
   m = False
   cmap = 'jet'
   qc_thresh = 2 
   try:
      opts, args = getopt.getopt(argv,"hi:p:c:q:m",["ifile=","figpath=","qcthreshold=","montage"])
   except getopt.GetoptError:
      print ('make_cl51_quicklooks.py -i <inputfile> -p <figpath> -c <colormap> -q <qc_thresh> -m')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('make_cl51_quicklooks.py -i <inputfile> -p <figpath> -c <colormap> -q <qc_thresh> -m')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-p", "--figpath"):
         figpath = arg
      elif opt in ("-c", "--colormap"):
         cmap = arg
      elif opt in ("-q", "--qcthreshold"):
         qc_thresh = int(arg)
      elif opt in ("-m", "--montage"):
         m = True
   print ('Input file is ', inputfile)
   print ('Figure path is ', figpath)
   cl51.make_quicklook(inputfile,figpath,colormap=cmap, qc_threshold=qc_thresh,montage=m)


if __name__ == "__main__":
   main(sys.argv[1:])



