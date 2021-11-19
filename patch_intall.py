#!/usr/bin/env python
import sys, glob, os

def find_wienroot():
    wien = {}

    return wien

def install():
    
    # find WIENROOT
    root = find_wienroot() 
    print("Applying patch to WIEN2k version= {} in dir: {}".format(root["version"], root["dir"]))
    # changes to be made
    comment = "!  CLIGHT="
    function = """contains
    function get_clight() result(clight)
      ! this function checks for a file soc.txt.
      ! if the file is present it uses ctilde = prefactor*c
      ! if the file does not change anything
      implicit none
      logical :: soc_file
      real*8 :: clight
      real*8 :: prefactor
      inquire(FILE="soc.txt", EXIST=soc_file)
      if (soc_file) then
        open(69, file="soc.txt", status="old")
        read(69,*) prefactor
        CLIGHT=137.0359895D0*prefactor       ! c = prefactor*c
        close(69)
      else
        CLIGHT=137.0359895D0
      endif
    end function get_clight"""

    define = "real*8::clight\n"
    call   = "CLIGHT = get_clight()\n"

    changes = {"atpar.F":    [[40, define], [68, call]],
               "diracout.f": [[37, define], [70, call]], 
               "garadme.f" : [[37, define], [81, call]],
               "garadorb.f": [[9, define], [51, call]], 
               "hscalc.f" : [[7, define], [21, call]], 
               "outwin.F": [[24, define], [44, call]], 
               "vnsrint.f" : [[9, define], [55, call]], 
               "modules.F": [[1, comment], [10, function]]
               }

    for file in changes.keys():
        f = open(file).readlines()
        # make the changes from the dictionary
        f.close()

    print("Finished applying the patch!")





if __name__ == "__main__":
    install()
