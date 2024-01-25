!==================================================================================================!
!==================================================================================================!
!                                                                                                  !
! ELEFANT                                                                        C. Thieulot       !
!                                                                                                  !
!==================================================================================================!
!==================================================================================================!

subroutine process_inputs

use module_parameters, only: GT_storage,stokes_solve_strategy,iproc,inner_solver_type,K_storage
use module_timing

implicit none


!==================================================================================================!
!==================================================================================================!
!@@ \subsection{process\_inputs}
!@@
!==================================================================================================!

if (iproc==0) then

call system_clock(counti,count_rate)

!==============================================================================!

!assumptions are default:
!K_storage='matrix_FULL'
!GT_storage='matrix_FULL'

write(*,'(a,a)') shift//'stokes_solve_strategy=',stokes_solve_strategy

select case(stokes_solve_strategy)

!--------------
case('penalty')
   GT_storage='none'

   select case(inner_solver_type)
   case('LINPACK')
      K_storage='matrix_FULL'
   case('Y12M')
      K_storage='matrix_CSR'
   case default
      stop 'process_input: unknown inner_solver_type'
   end select


!-----------------
case('segregated')

   select case(inner_solver_type)
   case('LINPACK')
      K_storage='blocks_FULL'
   case('Y12M')
      K_storage='blocks_CSR'
   case default
      stop 'process_input: unknown inner_solver_type'
   end select

case default

   stop 'process_inputs: pb with stokes_solve_strategy'

end select

write(*,'(a,a)') shift//'K_storage=',K_storage

!----------------------------------------------------------


!==============================================================================!

call system_clock(countf) ; elapsed=dble(countf-counti)/dble(count_rate)

write(*,'(a,f6.2,a)') 'process_inputs:',elapsed,' s                 |'

end if ! iproc

end subroutine

!==================================================================================================!
!==================================================================================================!
