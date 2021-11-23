#!/usr/bin/env python
import sys, glob, os, shutil

def find_wienroot():
    wien = {}
    try:
        wien["dir"] = os.environ["WIENROOT"]
    except:
        print("[ERROR] environment variable WIENROOT not found!")
        sys.exit(1)
    wien["version"] = open(wien["dir"] +"/WIEN2k_VERSION").readlines()[0]
    return wien

def uninstall(root):
    print("[INFO] uninstalling...")
    for file in glob.glob(root["dir"]+"/SRC_lapwso/"+"*.F_unpatched"):
        print("[INFO] uninstalling...{}".format(file.split("unpatched")[0][:-1]))
        shutil.move(file, file.split("unpatched")[0][:-1])
    for file in glob.glob(root["dir"]+"/SRC_lapwso/"+"*.f_unpatched"):
        print("[INFO] uninstalling...{}".format(file.split("unpatched")[0][:-1]))
        shutil.move(file, file.split("unpatched")[0][:-1])
    print("[INFO] uninstall complete!")

def install():
    # find WIENROOT
    root = find_wienroot() 
    print("[INFO] Applying patch to WIEN2k version= {} in dir: {}".format(root["version"], root["dir"]))

    if len(glob.glob(root["dir"]+"/SRC_lapwso/"+"*.F_unpatched")) != 0:
            print("[INFO] previous patch detected uninstalling!")
            uninstall(root)
            sys.exit(0)

    # changes to be made
    comment = "! REAL*8,PARAMETER  :: CLIGHT=137.0359895D0\n"
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
                    end function get_clight\n"""

    define = "      real*8::clight\n"
    call   = "      CLIGHT = get_clight()\n"

    changes = {"atpar.F":    [[40, define], [64, call]],
               "diracout.f": [[37, define], [70, call]], 
               "garadme.f" : [[37, define], [77, call]],
               "garadorb.f": [[9, define], [51, call]], 
               "hscalc.f" :  [[7, define], [17, call]], 
               "outwin.F":   [[24, define], [44, call]], 
               "vnsrint.f" : [[9, define], [51, call]], 
               "modules.F":  [[22, comment], [31, function]]
               }

    for file in changes.keys():
        print("[INFO] applying patch to file: {}".format(file))
        shutil.copy2(root["dir"]+"/SRC_lapwso/"+file, root["dir"]+"/SRC_lapwso/"+file+"_unpatched")
        f = open(root["dir"]+"/SRC_lapwso/"+file).readlines()
        if file == "modules.F": f.pop(21)
        for c in changes[file]:
            f.insert(c[0]-1, c[1])
        fnew = open(root["dir"]+"/SRC_lapwso/"+file, "w")
        for (il, line) in enumerate(f):
            fnew.write(line)
        fnew.close()
    print("[INFO] Finished applying the patch!")

if __name__ == "__main__":
    install()
