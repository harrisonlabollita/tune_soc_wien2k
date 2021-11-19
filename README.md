Tuneable SOC in WIEN2k
======================

**A patch for tunable spin-orbit coupling in WIEN2k!**

In some material applications, one would like to adjust the strength of spin-orbit coupling (SOC) in a density-functional theory (DFT) calculation. In [WIEN2k](http://susi.theochem.tuwien.ac.at) this can currently only be done by changing the source code and recompiling. Specifically, one can adjust the speed of light (c), which is simply a constant factor in front of the spin-orbit coupling Hamiltonian. This parameter is defined in the file SRC\_lapwso/modules.F (CLIGHT) can be adjusted to whatever you would like (within reason). After adjusting this value, the user needs to recompile the lapwso module then they can perform their calculaiton.

However, this is _horribly_ inconvenient when one wants to do a systematic sweep of many different SOC strengths to say try to match ARPES data. This leads us to this current repository! Here, we have a small patch to the WIEN2k lapwso module that will allow a user to specify the strength of SOC without the need to recompile each time. To apply the patch simply run the script, [instalation script](patch_install.py). Furthermore, each file [SRC\_lapwso](SRC_lapwso) contains all of the files that will be changes as well comments illustrating what will be changed in each file.

Once the patch has been installed and the source code has been recompiled, the user simply creates a file ``soc.txt`` inside the calculation directory, which will contain a single number (REAL\*8), which will be multiplied by the speed of light (c). Note that in WIEN2k's implementation of SOC, changing the speed of light means you are adjusting a 1/(c\*c) constant in front of this term. Therefore, decreasing the speed of light increases the SOC strength and vice-versa. 

**Note**: The file ``soc.txt`` does not have to be present. If this file is not present the code will run no problem.

For clarity, the bulk of the patch comes from this small little function which will be written to the file ``modules.F`` in SRC\_lapwso.

```fortran
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
    end function get_clight
```

**Disclaimer: This patch is altering the source code to a commerical DFT code, which should be done with caution!**

Contact
-------
If you run into any trouble using this patch, please contact [me](mathlabolli@asu.edu)
