!==================================================================================================!
!==================================================================================================!
!                                                                                                  !
! ELEFANT                                                                        C. Thieulot       !
!                                                                                                  !
!==================================================================================================!
!==================================================================================================!

subroutine output_solution

use module_constants, only: zero
use module_parameters
use module_statistics 
use module_mesh 
use module_timing

implicit none

integer i,k
real(8) uth,vth,wth,pth,dum
real(8) dNdx(mV),dNdy(mV),dNdz(mV),div_v,jcob

logical, parameter :: output_boundary_indicators=.false. ! careful with these for higher order elts
logical, parameter :: output_fixed_boundaries=.false. ! careful with these for higher order elts

!==================================================================================================!
!==================================================================================================!
!@@ \subsubsection{output\_solution}
!@@ This subroutine generates the {\filenamefont solution.vtu} in the {\foldernamefont OUTPUT}
!@@ folder. It also generates the basic ascii file {\filenamefont solution.ascii}
!@@ \begin{tabular}{lcc}
!@@ & 2D & 3D \\
!@@ $P_1$ & 5 & 10 \\
!@@ $P_2$ & 22 & 24 \\
!@@ $Q_1$ & 9 & 12 \\
!@@ $Q_2$ & 23 & 25 \\
!@@ \hline
!@@ \end{tabular}
!==================================================================================================!

if (iproc==0 .and. mod(istep,output_freq)==0) then

call system_clock(counti,count_rate)

!==============================================================================!

open(unit=123,file='OUTPUT/solution_'//cistep//'.vtu',status='replace',form='formatted')
write(123,'(a)') '<VTKFile type="UnstructuredGrid" version="0.1" byte_order="BigEndian">'
write(123,'(a)') '<UnstructuredGrid>'
write(123,'(a,i8,a,i7,a)') '<Piece NumberOfPoints="',mV*nel,'" NumberOfCells="',nel,'">'
!=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
write(123,'(a)') '<Points>'
write(123,'(a)') '<DataArray type="Float32" NumberOfComponents="3" Format="ascii">'
do iel=1,nel
   do k=1,mV
      write(123,'(3es12.4)') mesh(iel)%xV(k),mesh(iel)%yV(k),mesh(iel)%zV(k)
   end do
end do
write(123,'(a)') '</DataArray>'
write(123,'(a)') '</Points>'
!=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
write(123,'(a)') '<CellData Scalars="scalars">'
!-----
if (debug .or. output_boundary_indicators) then
write(123,*) '<DataArray type="Float32" Name="boundary: 1" Format="ascii">'
do iel=1,nel
if (mesh(iel)%bnd1_elt) then
   write(123,'(i1)') 1
else
   write(123,'(i1)') 0
end if
end do
write(123,*) '</DataArray>'
end if
!-----
if (debug .or. output_boundary_indicators) then
write(123,*) '<DataArray type="Float32" Name="boundary: 2" Format="ascii">'
do iel=1,nel
if (mesh(iel)%bnd2_elt) then
   write(123,'(i1)') 1
else
   write(123,'(i1)') 0
end if
end do
write(123,*) '</DataArray>'
end if
!-----
if (debug .or. output_boundary_indicators) then
write(123,*) '<DataArray type="Float32" Name="boundary: 3" Format="ascii">'
do iel=1,nel
if (mesh(iel)%bnd3_elt) then
   write(123,'(i1)') 1
else
   write(123,'(i1)') 0
end if
end do
write(123,*) '</DataArray>'
end if
!-----
if (debug .or. output_boundary_indicators) then
write(123,*) '<DataArray type="Float32" Name="boundary: 4" Format="ascii">'
do iel=1,nel
if (mesh(iel)%bnd4_elt) then
   write(123,'(i1)') 1
else
   write(123,'(i1)') 0
end if
end do
write(123,*) '</DataArray>'
end if
!-----
if (debug .or. output_boundary_indicators .and. ndim==3) then
write(123,*) '<DataArray type="Float32" Name="boundary: 5" Format="ascii">'
do iel=1,nel
if (mesh(iel)%bnd5_elt) then
   write(123,'(i1)') 1
else
   write(123,'(i1)') 0
end if
end do
write(123,*) '</DataArray>'
end if
!-----
if (debug .or. output_boundary_indicators .and. ndim==3) then
write(123,*) '<DataArray type="Float32" Name="boundary: 6" Format="ascii">'
do iel=1,nel
if (mesh(iel)%bnd6_elt) then
   write(123,'(i1)') 1
else
   write(123,'(i1)') 0
end if
end do
write(123,*) '</DataArray>'
end if
!-----
write(123,'(a)') '<DataArray type="Float32" NumberOfComponents="3" Name="hx,hy,hz" Format="ascii">'
do iel=1,nel
   write(123,'(3es12.4)') mesh(iel)%hx,mesh(iel)%hy,mesh(iel)%hz
end do
write(123,'(a)') '</DataArray>'
!-----
write(123,'(a)') '<DataArray type="Float32" Name="vol" Format="ascii">'
do iel=1,nel
   write(123,'(es12.4)') mesh(iel)%vol
end do
write(123,'(a)') '</DataArray>'
!-----
if (use_swarm) then
write(123,'(a)') '<DataArray type="Float32" Name="nmarker" Format="ascii">'
do iel=1,nel
   write(123,'(i4)') mesh(iel)%nmarker
end do
write(123,'(a)') '</DataArray>'
end if
!-----
if (use_swarm) then
write(123,*) '<DataArray type="Float32" Name="least squares: a_rho" Format="ascii">'
do iel=1,nel
   write(123,*) mesh(iel)%a_rho
end do
write(123,*) '</DataArray>'
end if
!-----
if (use_swarm) then
write(123,*) '<DataArray type="Float32" Name="least squares: b_rho" Format="ascii">'
do iel=1,nel
   write(123,*) mesh(iel)%b_rho
end do
write(123,*) '</DataArray>'
end if
!-----
if (use_swarm) then
write(123,*) '<DataArray type="Float32" Name="least squares: c_rho" Format="ascii">'
do iel=1,nel
   write(123,*) mesh(iel)%c_rho
end do
write(123,*) '</DataArray>'
end if
!-----
if (use_swarm) then
write(123,*) '<DataArray type="Float32" Name="least squares: a_eta" Format="ascii">'
do iel=1,nel
   write(123,*) mesh(iel)%a_eta
end do
write(123,*) '</DataArray>'
end if
!-----
if (use_swarm) then
write(123,*) '<DataArray type="Float32" Name="least squares: b_eta" Format="ascii">'
do iel=1,nel
   write(123,*) mesh(iel)%b_eta
end do
write(123,*) '</DataArray>'
end if
!-----
if (use_swarm) then
write(123,*) '<DataArray type="Float32" Name="least squares: c_eta" Format="ascii">'
do iel=1,nel
   write(123,*) mesh(iel)%c_eta
end do
write(123,*) '</DataArray>'
end if
!-----
write(123,'(a)') '<DataArray type="Float32" Name="rho (avrg)" Format="ascii">'
do iel=1,nel
   write(123,'(f12.5)') mesh(iel)%rho_avrg 
end do
write(123,'(a)') '</DataArray>'
!-----
write(123,*) '<DataArray type="Float32" Name="eta (avrg)" Format="ascii">'
do iel=1,nel
   write(123,'(es12.4)') mesh(iel)%eta_avrg 
end do
write(123,*) '</DataArray>'
!-----
if (solve_stokes_system) then
write(123,*) '<DataArray type="Float32" Name="div(v)" Format="ascii">'
do iel=1,nel
   if (ndim==2) then
      call compute_dNdx_dNdy(zero,zero,dNdx,dNdy,jcob)
      div_v=sum(dNdx(1:mV)*mesh(iel)%u(1:mV))&
           +sum(dNdy(1:mV)*mesh(iel)%v(1:mV))
   else
      call compute_dNdx_dNdy_dNdz(zero,zero,zero,dNdx,dNdy,dNdz,jcob)
      div_v=sum(dNdx(1:mV)*mesh(iel)%u(1:mV))&
           +sum(dNdy(1:mV)*mesh(iel)%v(1:mV))&
           +sum(dNdz(1:mV)*mesh(iel)%w(1:mV))
   end if
   write(123,*) div_v
end do
write(123,*) '</DataArray>'
end if
!-----
write(123,*) '</CellData>'
!=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
write(123,*) '<PointData Scalars="scalars">'
!-----
if (solve_stokes_system) then
write(123,*) '<DataArray type="Float32" NumberOfComponents="3" Name="velocity" Format="ascii">'
do iel=1,nel
   do k=1,mV
      write(123,'(3es12.4)') mesh(iel)%u(k),mesh(iel)%v(k),mesh(iel)%w(k) 
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
if (solve_stokes_system) then
write(123,*) '<DataArray type="Float32" Name="pressure (q)" Format="ascii">'
do iel=1,nel
   do k=1,mV
      write(123,'(es12.4)') mesh(iel)%q(k)
   end do
end do
write(123,*) '</DataArray>'
end if 
!-----
write(123,*) '<DataArray type="Float32" Name="rho" Format="ascii">'
do iel=1,nel
   do k=1,mV
      write(123,'(es12.4)') mesh(iel)%rho(k)
   end do
end do
write(123,*) '</DataArray>'
!-----
write(123,*) '<DataArray type="Float32" Name="eta" Format="ascii">'
do iel=1,nel
   do k=1,mV
      write(123,'(es12.4)') mesh(iel)%eta(k)
   end do
end do
write(123,*) '</DataArray>'
!-----
if (use_T) then 
write(123,*) '<DataArray type="Float32" Name="temperature (T)" Format="ascii">'
do iel=1,nel
   do k=1,mT
      write(123,'(es12.4)') mesh(iel)%T(k)
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
if (use_T) then 
write(123,*) '<DataArray type="Float32" NumberOfComponents="3" Name="heat flux" Format="ascii">'
do iel=1,nel
   do k=1,mV
      write(123,'(3es12.4)') mesh(iel)%qx(k),mesh(iel)%qy(k),mesh(iel)%qz(k)
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
if (output_boundary_indicators .and. ndim==3) then
write(123,*) '<DataArray type="Float32" Name="boundary: 5" Format="ascii">'
do iel=1,nel
   do k=1,mV
      if (mesh(iel)%bnd5_node(k)) then
         write(123,'(i1)') 1
      else
         write(123,'(i1)') 0
      end if
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
if (output_boundary_indicators .and. ndim==3) then
write(123,*) '<DataArray type="Float32" Name="boundary: 6" Format="ascii">'
do iel=1,nel
   do k=1,mV
      if (mesh(iel)%bnd6_node(k)) then
         write(123,'(i1)') 1
      else
         write(123,'(i1)') 0
      end if
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
if (output_boundary_indicators) then
write(123,*) '<DataArray type="Float32" Name="boundary: 1" Format="ascii">'
do iel=1,nel
   do k=1,mV
      if (mesh(iel)%bnd1_node(k)) then
         write(123,'(i1)') 1
      else
         write(123,'(i1)') 0
      end if
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
if (output_boundary_indicators) then
write(123,*) '<DataArray type="Float32" Name="boundary: 2" Format="ascii">'
do iel=1,nel
   do k=1,mV
      if (mesh(iel)%bnd2_node(k)) then
         write(123,'(i1)') 1
      else
         write(123,'(i1)') 0
      end if
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
if (output_boundary_indicators) then
write(123,*) '<DataArray type="Float32" Name="boundary: 3" Format="ascii">'
do iel=1,nel
   do k=1,mV
      if (mesh(iel)%bnd3_node(k)) then
         write(123,'(i1)') 1
      else
         write(123,'(i1)') 0
      end if
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
if (output_boundary_indicators) then
write(123,*) '<DataArray type="Float32" Name="boundary: 4" Format="ascii">'
do iel=1,nel
   do k=1,mV
      if (mesh(iel)%bnd4_node(k)) then
         write(123,'(i1)') 1
      else
         write(123,'(i1)') 0
      end if
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
if (output_fixed_boundaries) then
write(123,*) '<DataArray type="Float32" Name="fix_u" Format="ascii">'
do iel=1,nel
   do k=1,mV
      if (mesh(iel)%fix_u(k)) then
         write(123,'(i1)') 1
      else
         write(123,'(i1)') 0
      end if
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
if (output_fixed_boundaries) then
write(123,*) '<DataArray type="Float32" Name="fix_v" Format="ascii">'
do iel=1,nel
   do k=1,mV
      if (mesh(iel)%fix_v(k)) then
         write(123,'(i1)') 1
      else
         write(123,'(i1)') 0
      end if
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
if (output_fixed_boundaries .and. ndim==3) then
write(123,*) '<DataArray type="Float32" Name="fix_w" Format="ascii">'
do iel=1,nel
   do k=1,mV
      if (mesh(iel)%fix_w(k)) then
         write(123,'(i1)') 1
      else
         write(123,'(i1)') 0
      end if
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
write(123,*) '<DataArray type="Float32" NumberOfComponents="3" Name="velocity (analytical)" Format="ascii">'
do iel=1,nel
   do k=1,mV
      call experiment_analytical_solution(mesh(iel)%xV(k),mesh(iel)%yV(k),mesh(iel)%zV(k),&
                               uth,vth,wth,dum,dum,dum,dum,dum,dum,dum,dum)
      write(123,'(3es12.5)') uth,vth,wth
   end do
end do
write(123,*) '</DataArray>'
!-----
if (solve_stokes_system) then
write(123,*) '<DataArray type="Float32" NumberOfComponents="3" Name="velocity (error)" Format="ascii">'
do iel=1,nel
   do k=1,mV
      call experiment_analytical_solution(mesh(iel)%xV(k),mesh(iel)%yV(k),mesh(iel)%zV(k),&
                               uth,vth,wth,dum,dum,dum,dum,dum,dum,dum,dum)
      write(123,'(3es12.5)') mesh(iel)%u(k)-uth,mesh(iel)%v(k)-vth,mesh(iel)%w(k)-wth
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
write(123,*) '<DataArray type="Float32" Name="pressure q (analytical)" Format="ascii">'
do iel=1,nel
   do k=1,mV
      call experiment_analytical_solution(mesh(iel)%xV(k),mesh(iel)%yV(k),mesh(iel)%zV(k),&
                               uth,vth,wth,pth,dum,dum,dum,dum,dum,dum,dum)
      write(123,'(es12.4)') pth
   end do
end do
write(123,*) '</DataArray>'
!-----
if (solve_stokes_system) then
write(123,*) '<DataArray type="Float32" Name="pressure q (error)" Format="ascii">'
do iel=1,nel
   do k=1,mV
      call experiment_analytical_solution(mesh(iel)%xV(k),mesh(iel)%yV(k),mesh(iel)%zV(k),&
                               uth,vth,wth,pth,dum,dum,dum,dum,dum,dum,dum)
      write(123,'(es12.4)') mesh(iel)%q(k)-pth
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
if (solve_stokes_system) then
write(123,*) '<DataArray type="Float32" Name="exx" Format="ascii">'
do iel=1,nel
   do k=1,mV
      write(123,*) mesh(iel)%exx(k)
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
if (solve_stokes_system) then
write(123,*) '<DataArray type="Float32" Name="eyy" Format="ascii">'
do iel=1,nel
   do k=1,mV
      write(123,'(es12.5)') mesh(iel)%eyy(k)
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
if (solve_stokes_system .and. ndim==3) then
write(123,*) '<DataArray type="Float32" Name="ezz" Format="ascii">'
do iel=1,nel
   do k=1,mV
      write(123,'(es12.5)') mesh(iel)%ezz(k)
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
if (solve_stokes_system) then
write(123,*) '<DataArray type="Float32" Name="exy" Format="ascii">'
do iel=1,nel
   do k=1,mV
      write(123,'(es12.5)') mesh(iel)%exy(k)
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
if (solve_stokes_system .and. ndim==3) then
write(123,*) '<DataArray type="Float32" Name="exz" Format="ascii">'
do iel=1,nel
   do k=1,mV
      write(123,'(es12.5)') mesh(iel)%exz(k)
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
if (solve_stokes_system .and. ndim==3) then
write(123,*) '<DataArray type="Float32" Name="eyz" Format="ascii">'
do iel=1,nel
   do k=1,mV
      write(123,'(es12.5)') mesh(iel)%eyz(k)
   end do
end do
write(123,*) '</DataArray>'
end if
!-----
write(123,*) '</PointData>'
!=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
write(123,*) '<Cells>'
!-----
write(123,*) '<DataArray type="Int32" Name="connectivity" Format="ascii">'
do iel=1,nel
   write(123,*) ( (iel-1)*mV+i-1,i=1,mV) 
end do
write(123,*) '</DataArray>'
!-----
write(123,*) '<DataArray type="Int32" Name="offsets" Format="ascii">'
select case(spaceV)
case('__Q1')
   if (ndim==2) write(123,*) (iel*4,iel=1,nel)
   if (ndim==3) write(123,*) (iel*8,iel=1,nel)
case('__Q2')
   if (ndim==2) write(123,*) (iel*9,iel=1,nel)
   if (ndim==3) write(123,*) (iel*27,iel=1,nel)
case('__P1')
   if (ndim==2) write(123,*) (iel*3,iel=1,nel)
   if (ndim==3) write(123,*) (iel*4,iel=1,nel)
case('__P2')
   if (ndim==2) write(123,*) (iel*6,iel=1,nel)
   if (ndim==3) write(123,*) (iel*10,iel=1,nel)
case('_Q1+')
   write(123,*) (iel*4,iel=1,nel)
case('Q1++')
   write(123,*) (iel*8,iel=1,nel)
case default
   stop 'pb in output_solution: cell offset unknown'
end select
write(123,*) '</DataArray>'
!-----
write(123,*) '<DataArray type="Int32" Name="types" Format="ascii">'
select case(spaceV)
case('__Q1')
   if (ndim==2) write(123,*) (9,iel=1,nel)
   if (ndim==3) write(123,*) (12,iel=1,nel)
case('__Q2')
   if (ndim==2) write(123,*) (23,iel=1,nel)
   if (ndim==3) write(123,*) (25,iel=1,nel)
case('__P1')
   if (ndim==2) write(123,*) (5,iel=1,nel)
   if (ndim==3) write(123,*) (10,iel=1,nel)
case('__P2')
   if (ndim==2) write(123,*) (22,iel=1,nel)
   if (ndim==3) write(123,*) (24,iel=1,nel)
case('_Q1+')
   write(123,*) (9,iel=1,nel)
case('Q1++')
   write(123,*) (12,iel=1,nel)
case default
   stop 'pb in output_solution: cell type unknown'
end select
write(123,*) '</DataArray>'
!-----
write(123,*) '</Cells>'
!=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
write(123,*) '</Piece>'
write(123,*) '</UnstructuredGrid>'
write(123,*) '</VTKFile>'
close(123)

!----------------------------------------------------------
!open(unit=123,file="OUTPUT/solution.ascii",action="write")
!write(123,*) '#1,2,3  x,y,z '
!write(123,*) '#4,5,6  u,v,w '
!write(123,*) '#7      q '
!write(123,*) '#8      T '
!do iel=1,nel 
!   do k=1,mV
!      write(123,'(8es12.4)') mesh(iel)%xV(k),mesh(iel)%yV(k),mesh(iel)%zV(k),&
!                             mesh(iel)%u(k),mesh(iel)%v(k),mesh(iel)%w(k),&
!                             mesh(iel)%q(k),mesh(iel)%T(k)
!   end do
!end do
!close(123)

!==============================================================================!

call system_clock(countf) ; elapsed=dble(countf-counti)/dble(count_rate)

write(*,'(a,f6.2,a)') 'output_solution (',elapsed,' s)'

end if ! iproc

end subroutine

!==================================================================================================!
!==================================================================================================!
