!==================================================================================================!
!==================================================================================================!
!                                                                                                  !
! ELEFANT                                                                        C. Thieulot       !
!                                                                                                  !
!==================================================================================================!
!==================================================================================================!

subroutine print_parameters

use module_parameters

implicit none


!==================================================================================================!
!==================================================================================================!
!@@ \subsubsection{print\_parameters}
!@@
!==================================================================================================!

if (iproc==0) then

                 write(*,'(a,i10)')    '        ndim        =',ndim
                 write(*,'(a,a11)')    '        geometry    =',geometry
                 write(*,'(a,a10)')    '        spaceV      =',spaceV
                 write(*,'(a,a10)')    '        spaceP      =',spaceP
if (use_T)       write(*,'(a,a10)')    '        spaceT      =',spaceT
                 write(*,'(a,a10)')    '        mapping     =',mapping
                 write(*,'(a,f10.3)')  '        Lx          =',Lx
                 write(*,'(a,f10.3)')  '        Ly          =',Ly
if (ndim==3)     write(*,'(a,f10.3)')  '        Lz          =',Lz

select case(geometry)
case('cartesian2D')
                 write(*,'(a,i10)')    '        nelx        =',nelx
                 write(*,'(a,i10)')    '        nely        =',nely
case('cartesian3D')
                 write(*,'(a,i10)')    '        nelx        =',nelx
                 write(*,'(a,i10)')    '        nely        =',nely
                 write(*,'(a,i10)')    '        nelz        =',nelz
case('spherical')
                 write(*,'(a,i10)')    '        nelr        =',nelr
                 write(*,'(a,i10)')    '        neltheta    =',neltheta
                 write(*,'(a,i10)')    '        nelphi      =',nelphi
end select

                 write(*,'(a,i10)')    '        nel         =',nel
                 write(*,'(a,i10)')    '        nqel        =',nqel
                 write(*,'(a,i10)')    '        mV          =',mV
                 write(*,'(a,i10)')    '        mP          =',mP
                 write(*,'(a,i10)')    '        mT          =',mT
                 write(*,'(a,i10)')    '        NV          =',NV
                 write(*,'(a,i10)')    '        NP          =',NP
if (use_T)       write(*,'(a,i10)')    '        NT          =',NT
                 write(*,'(a,i10)')    '        NfemV       =',NfemV
                 write(*,'(a,i10)')    '        NfemP       =',NfemP
if (use_T)       write(*,'(a,i10)')    '        NfemT       =',NfemT
                 write(*,'(a,i10)')    '        Nq          =',Nq
                 write(*,'(a,l10)')    '        inner_solver_type=',inner_solver_type
                 write(*,'(a,i10)')    '        nmat        =',nmat
                 write(*,'(a,l10)')    '        use_penalty =',use_penalty
if (use_penalty) write(*,'(a,es10.3)') '        penalty     =',penalty
if (use_ALE)     write(*,'(a,l10)')    '        use_ALE     =',penalty

end if ! iproc

end subroutine

!==================================================================================================!
!==================================================================================================!
