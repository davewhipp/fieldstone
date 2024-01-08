!==================================================================================================!
!==================================================================================================!
!                                                                                                  !
! ELEFANT                                                                        C. Thieulot       !
!                                                                                                  !
!==================================================================================================!
!==================================================================================================!

subroutine assemble_S(S_el)

!use module_parameters
!use module_mesh 
!use module_constants
!use module_swarm
!use module_materials
!use module_arrays
use module_timing

implicit none


!==================================================================================================!
!==================================================================================================!
!@@ \subsection{assemble_S}
!@@
!==================================================================================================!

   do k1=1,mP
      m1=mesh(iel)%iconP(k1) ! global coordinate of pressure dof
      do k2=1,mP
         m2=mesh(iel)%iconP(k2) ! global coordinate of pressure dof
         do k=csrMP%ia(m1),csrMP%ia(m1+1)-1    
            if (csrMP%ja(k)==m2) then  
               csrMP%mat(k)=csrMP%mat(k)+S_el(k1,k2)  
            end if    
         end do
      end do
   end do




end subroutine

!==================================================================================================!
!==================================================================================================!
