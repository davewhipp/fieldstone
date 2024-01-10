!==================================================================================================!
!==================================================================================================!
!                                                                                                  !
! ELEFANT                                                                        C. Thieulot       !
!                                                                                                  !
!==================================================================================================!
!==================================================================================================!

subroutine assemble_K(K_el)

use module_parameters, only: iel,K_storage,mVel 
use module_mesh 
use module_MUMPS
use module_sparse, only: csrK
use module_arrays, only: K_matrix 
use module_timing

implicit none

real(8), intent(in) :: K_el(mVel,mVel)

integer :: k,kV1,kV2,kkV1,kkV2,counter_mumps

!==================================================================================================!
!==================================================================================================!
!@@ \subsection{assemble\_K}
!@@
!==================================================================================================!

select case(K_storage)

!-------------------
case('matrix_FULL')

   do kV1=1,mVel
      kkV1=mesh(iel)%iconVel(kV1)
      do kV2=1,mVel
         kkV2=mesh(iel)%iconVel(kV2)
         K_matrix(kkV1,kkV2)=K_el(kV1,kV2)
      end do
   end do

!-------------------
case('matrix_MUMPS')

   counter_mumps=0
   do kV1=1,mVel
      kkV1=mesh(iel)%iconVel(kV1)
      do kV2=1,mVel
         kkV2=mesh(iel)%iconVel(kV2)
         if (kkV2>=kkV1) then
            counter_mumps=counter_mumps+1
            idV%A_ELT(counter_mumps)=K_el(kV1,kV2)
         end if
      end do
   end do

!-------------------
case('blocks_MUMPS')

   stop 'assemble_K: blocks_MUMPS not available yet'

!-------------------
case('matrix_CSR')

   do kV1=1,mVel
      kkV1=mesh(iel)%iconVel(kV1)
      do kV2=1,mVel
         kkV2=mesh(iel)%iconVel(kV2)
         do k=csrK%ia(kkV1),csrK%ia(kkV1+1)-1    
            if (csrK%ja(k)==kkV2) then  
               csrK%mat(k)=csrK%mat(k)+K_el(kV1,kV2)  
            end if    
         end do    
      end do
   end do

!-------------------
case('blocks_CSR')

!-----------
case default

   stop 'assemble_K: unknown K_storage'

end select


end subroutine

!==================================================================================================!
!==================================================================================================!
