MODULE param
! comment line defining CLIGHT

! Insert the following snippet of code below at the end of the param module

  contains
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
END MODULE param
! continue with the rest of the file
