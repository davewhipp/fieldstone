!==================================================================================================!
!==================================================================================================!
!                                                                                                  !
! ELEFANT                                                                        C. Thieulot       !
!                                                                                                  !
!==================================================================================================!
!==================================================================================================!

subroutine impose_boundary_conditions(K_el,G_el,f_el,h_el)

use global_parameters
use structures
!use constants

implicit none

real(8),intent(inout) :: K_el(mV*ndofV,mV*ndofV)
real(8),intent(inout) :: f_el(mV*ndofV)
real(8),intent(inout) :: G_el(mV*ndofV,mP)
real(8),intent(inout) :: h_el(mP)

integer k,i,j
real(8) bcvalue,Kref

!==================================================================================================!
!==================================================================================================!
!@@ \subsubsection{impose\_boundary\_conditions}
!@@
!==================================================================================================!

do k=1,mV    

   !x component
   if (mesh(iel)%fix_u(k)) then
      bcvalue=mesh(iel)%u(k)
      i=(k-1)*ndofV+1    
      Kref=K_el(i,i)    
      do j=1,mV*ndofV
         f_el(j)=f_el(j)-K_el(j,i)*bcvalue    
         K_el(i,j)=0d0 
         K_el(j,i)=0d0  
      enddo  
      do j=1,mP
         h_el(j)=h_el(j)-G_el(i,j)*bcvalue
         G_el(i,j)=0d0
      enddo  
      K_el(i,i)=Kref    
      f_el(i)=Kref*bcvalue   
   end if

   !y component
   if (mesh(iel)%fix_v(k)) then
      bcvalue=mesh(iel)%v(k)
      i=(k-1)*ndofV+2    
      Kref=K_el(i,i)    
      do j=1,mV*ndofV
         f_el(j)=f_el(j)-K_el(j,i)*bcvalue    
         K_el(i,j)=0d0 
         K_el(j,i)=0d0  
      enddo  
      do j=1,mP
         h_el(j)=h_el(j)-G_el(i,j)*bcvalue
         G_el(i,j)=0d0
      enddo  
      K_el(i,i)=Kref    
      f_el(i)=Kref*bcvalue   
   end if

   !z component
   if (mesh(iel)%fix_w(k)) then
      bcvalue=mesh(iel)%w(k)
      i=(k-1)*ndofV+3    
      Kref=K_el(i,i)    
      do j=1,mV*ndofV
         f_el(j)=f_el(j)-K_el(j,i)*bcvalue    
         K_el(i,j)=0d0 
         K_el(j,i)=0d0  
      enddo  
      do j=1,mP
         h_el(j)=h_el(j)-G_el(i,j)*bcvalue
         G_el(i,j)=0d0
      enddo  
      K_el(i,i)=Kref    
      f_el(i)=Kref*bcvalue   
   end if

enddo

end subroutine

!==================================================================================================!
!==================================================================================================!
