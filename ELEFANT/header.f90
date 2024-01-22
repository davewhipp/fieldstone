!=================================================================================================!
!=================================================================================================!
!                                                                                                 !
! ELEFANT                                                                        C. Thieulot      !
!                                                                                                 !
!=================================================================================================!
!=================================================================================================!

subroutine header

use module_parameters

implicit none

if (iproc==0) then
write(*,'(a)') '================================================================================'
write(*,'(a)') '================================================================================'
write(*,'(a)') '=============================[ E L E F A N T ]=================================='
write(*,'(a)') '================================================================================'
write(*,'(a)') '================================================================================'
end if

end subroutine

!=================================================================================================!
!=================================================================================================!

subroutine spacer

use module_parameters

implicit none

if (iproc==0) then
write(*,'(a)') '================================================================================'
write(*,'(a)') '================================================================================'
end if

end subroutine

!=================================================================================================!
!=================================================================================================!

subroutine spacer_istep

use module_parameters

implicit none

if (iproc==0) then
write(*,'(a)') '----------------------------------------------------------------------'
write(*,'(a,i6,a)') 'istep=',istep,' ---------------------------------------------------------'
write(*,'(a)') '----------------------------------------------------------------------'
end if

end subroutine

!=================================================================================================!
!=================================================================================================!

subroutine spacer_end

use module_parameters

implicit none

if (iproc==0) then
write(*,'(a)') '======================================================================'
write(*,'(a)') '======================================================================'
end if

end subroutine

!=================================================================================================!
!=================================================================================================!

subroutine footer

use module_parameters

implicit none

if (iproc==0) then
write(*,'(a)') '================================================================================'
write(*,'(a)') ' run completed. get a life. go home ... '
write(*,'(a)') '================================================================================'
end if

call flush(6)

end subroutine

!=================================================================================================!
!=================================================================================================!
