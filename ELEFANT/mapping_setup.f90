!==================================================================================================!
!==================================================================================================!
!                                                                                                  !
! ELEFANT                                                                        C. Thieulot       !
!                                                                                                  !
!==================================================================================================!
!==================================================================================================!

subroutine mapping_setup

use module_parameters, only: iel,spaceV,mapping,nel,iproc,debug
use module_mesh 
use module_timing

implicit none


!==================================================================================================!
!==================================================================================================!
!@@ \subsubsection{template}
!@@
!==================================================================================================!

if (iproc==0) then

call system_clock(counti,count_rate)

!==============================================================================!

if (mapping==spaceV) then
   
   do iel=1,nel
      mesh(iel)%xM=mesh(iel)%xV   
      mesh(iel)%yM=mesh(iel)%yV   
      mesh(iel)%zM=mesh(iel)%zV   
      mesh(iel)%iconM=mesh(iel)%iconV 
   end do

else

   stop 'non isoparametric mapping not supported yet'

end if

!if (debug) then
!print *,'*************************'
!print *,'**********debug**********'
!print *,minval(mesh(1)%xM),maxval(mesh(1)%xM)
!print *,minval(mesh(1)%yM),maxval(mesh(1)%yM)
!print *,minval(mesh(1)%zM),maxval(mesh(1)%zM)
!print *,mesh(1)%iconM
!print *,'**********debug**********'
!print *,'*************************'
!end if

!==============================================================================!

call system_clock(countf) ; elapsed=dble(countf-counti)/dble(count_rate)

write(*,'(a,f6.2,a)') 'mapping_setup (',elapsed,' s)'

end if ! iproc

end subroutine

!==================================================================================================!
!==================================================================================================!
