!==================================================================================================!
!==================================================================================================!
!                                                                                                  !
! ELEFANT                                                                        C. Thieulot       !
!                                                                                                  !
!==================================================================================================!
!==================================================================================================!

subroutine matrix_setup_GT

use module_parameters
use module_mesh 
use module_timing
use module_sparse, only : csrGT
use module_arrays, only: pnode_belongs_to

implicit none

integer inode,k,nz,i,ii,nsees,k2,jp,ip,imod
logical, dimension(:), allocatable :: alreadyseen
real(8) t3,t4

!==================================================================================================!
!==================================================================================================!
!@@ \subsection{matrix\_setup\_GT.f90}
!@@ This subroutine is executed if {\sl use\_penalty} is False.
!==================================================================================================!

if (iproc==0) then

call system_clock(counti,count_rate)

!==============================================================================!

if (.not.use_penalty) then

csrGT%nr=NfemP ! number of rows
csrGT%nc=NfemV ! number of columns

select case(spacePressure)

case('__Q0','__P0','_P-1') ! is pressure discontinuous
   csrGT%NZ=mV*ndofV*nel*mP

case default

   allocate(alreadyseen(NfemV))
   nz=0
   do ip=1,NP
      nsees=0
      alreadyseen=.false.
      do k=1,pnode_belongs_to(1,ip)
         iel=pnode_belongs_to(1+k,ip)  ! elt seen by p node
         do i=1,mV
            jp=mesh(iel)%iconV(i)
            if (.not.alreadyseen(jp)) then
               !print *,'pnode ',ip,'sees vnode ',jp
               do k2=1,ndofV
                  nz=nz+1
               end do
               alreadyseen(jp)=.true.
            end if
         end do
      end do    
   end do
   deallocate(alreadyseen)    
   csrGT%NZ=nz

end select

write(*,'(a,i8)') shift//'matrix GT%nr=',csrGT%nr
write(*,'(a,i8)') shift//'matrix GT%nc=',csrGT%nc
write(*,'(a,i8)') shift//'matrix GT%NZ=',csrGT%nz

allocate(csrGT%ia(csrGT%nr+1))
allocate(csrGT%ja(csrGT%NZ))  
allocate(csrGT%mat(csrGT%NZ)) 

select case(spacePressure)

case('__Q0','__P0') ! is pressure discontinuous

   nz=0
   csrGT%ia(1)=1
   do iel=1,nel      ! iel indicates the row in the matrix
      nsees=0
      do i=1,mV
         inode=mesh(iel)%iconV(i)
         do k=1,ndofV
            ii=ndofV*(inode-1) + k ! column address in the matrix
            nz=nz+1
            csrGT%ja(nz)=ii
            nsees=nsees+1
         end do
      end do
      csrGT%ia(iel+1)=csrGT%ia(iel)+nsees
   end do

case default

   imod=NP/4

   call cpu_time(t3)
   allocate(alreadyseen(NfemV))
   nz=0
   csrGT%ia(1)=1
   do ip=1,NP
      if (mod(ip,imod)==0) write(*,'(TL10, F6.1,a)',advance='no') real(ip)/real(NP)*100.,'%'
      nsees=0
      alreadyseen=.false.
      do k=1,pnode_belongs_to(1,ip)
         iel=pnode_belongs_to(1+k,ip)  ! elt seen by pdof
         do i=1,mV
            jp=mesh(iel)%iconV(i)
            if (.not.alreadyseen(jp)) then
               !print *,'pnode ',ip,'sees vnode ',jp
               do k2=1,ndofV
                  nz=nz+1
                  csrGT%ja(nz)=ndofV*(jp-1) + k2 ! address in the matrix
                  nsees=nsees+1
               end do
               alreadyseen(jp)=.true.
            end if
         end do
      end do
      csrGT%ia(ip+1)=csrGT%ia(ip)+nsees
   end do
   call cpu_time(t4) ; write(*,'(f10.3,a)') t4-t3,'s'

end select

!------------------------------------------------------------------------------

if (debug) then
write(2345,*) limit//'matrix_setup_GT'//limit
write(2345,*) 'csrGT%nz=',csrGT%nz
write(2345,*) 'csrGT%ia (m/M)',minval(csrGT%ia), maxval(csrGT%ia)
write(2345,*) 'csrGT%ja (m/M)',minval(csrGt%ja), maxval(csrGT%ja)
write(2345,*) 'csrGT%ia ',csrGT%ia
do i=1,NfemP
write(2345,*) i,'th line: csrGT%ja=',csrGT%ja(csrGT%ia(i):csrGT%ia(i+1)-1)-1
end do
end if

else
   write(*,'(a)') shift//'bypassed since use_penalty=True'

end if !use_penalty

!==============================================================================!

call system_clock(countf) ; elapsed=dble(countf-counti)/dble(count_rate)

write(*,'(a,f6.2,a)') 'matrix_setup_GT:',elapsed,' s                |'

end if ! iproc

end subroutine

!==================================================================================================!
!==================================================================================================!
