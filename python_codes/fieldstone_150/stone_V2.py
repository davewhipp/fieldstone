import numpy as np
import sys as sys
import scipy.sparse as sps
from scipy.sparse.linalg import *
from scipy.sparse import lil_matrix
import time as timing

###############################################################################

def NNV(r,s):
    N_0= 0.5*r*(r-1.) * 0.5*s*(s-1.)
    N_1=    (1.-r**2) * 0.5*s*(s-1.)
    N_2= 0.5*r*(r+1.) * 0.5*s*(s-1.)
    N_3= 0.5*r*(r-1.) *    (1.-s**2)
    N_4=    (1.-r**2) *    (1.-s**2)
    N_5= 0.5*r*(r+1.) *    (1.-s**2)
    N_6= 0.5*r*(r-1.) * 0.5*s*(s+1.)
    N_7=    (1.-r**2) * 0.5*s*(s+1.)
    N_8= 0.5*r*(r+1.) * 0.5*s*(s+1.)
    return np.array([N_0,N_1,N_2,N_3,N_4,N_5,N_6,N_7,N_8],dtype=np.float64)

def dNNVdr(r,s):
    dNdr_0= 0.5*(2.*r-1.) * 0.5*s*(s-1)
    dNdr_1=       (-2.*r) * 0.5*s*(s-1)
    dNdr_2= 0.5*(2.*r+1.) * 0.5*s*(s-1)
    dNdr_3= 0.5*(2.*r-1.) *   (1.-s**2)
    dNdr_4=       (-2.*r) *   (1.-s**2)
    dNdr_5= 0.5*(2.*r+1.) *   (1.-s**2)
    dNdr_6= 0.5*(2.*r-1.) * 0.5*s*(s+1)
    dNdr_7=       (-2.*r) * 0.5*s*(s+1)
    dNdr_8= 0.5*(2.*r+1.) * 0.5*s*(s+1)
    return np.array([dNdr_0,dNdr_1,dNdr_2,dNdr_3,dNdr_4,dNdr_5,dNdr_6,dNdr_7,dNdr_8],dtype=np.float64)

def dNNVds(r,s):
    dNds_0= 0.5*r*(r-1.) * 0.5*(2.*s-1.)
    dNds_1=    (1.-r**2) * 0.5*(2.*s-1.)
    dNds_2= 0.5*r*(r+1.) * 0.5*(2.*s-1.)
    dNds_3= 0.5*r*(r-1.) *       (-2.*s)
    dNds_4=    (1.-r**2) *       (-2.*s)
    dNds_5= 0.5*r*(r+1.) *       (-2.*s)
    dNds_6= 0.5*r*(r-1.) * 0.5*(2.*s+1.)
    dNds_7=    (1.-r**2) * 0.5*(2.*s+1.)
    dNds_8= 0.5*r*(r+1.) * 0.5*(2.*s+1.)
    return np.array([dNds_0,dNds_1,dNds_2,dNds_3,dNds_4,dNds_5,dNds_6,dNds_7,dNds_8],dtype=np.float64)

def NNP(r,s):
    N_0=0.25*(1-r)*(1-s)
    N_1=0.25*(1+r)*(1-s)
    N_2=0.25*(1-r)*(1+s)
    N_3=0.25*(1+r)*(1+s)
    return np.array([N_0,N_1,N_2,N_3],dtype=np.float64)

###############################################################################

def bx(x,y):
    val=((12.-24.*y)*x**4+(-24.+48.*y)*x*x*x +
         (-48.*y+72.*y*y-48.*y*y*y+12.)*x*x +
         (-2.+24.*y-72.*y*y+48.*y*y*y)*x +
         1.-4.*y+12.*y*y-8.*y*y*y)
    return val

def by(x,y):
    val=((8.-48.*y+48.*y*y)*x*x*x+
         (-12.+72.*y-72.*y*y)*x*x+
         (4.-24.*y+48.*y*y-48.*y*y*y+24.*y**4)*x -
         12.*y*y+24.*y*y*y-12.*y**4)
    return val

def velocity_x(x,y):
    val=x*x*(1.-x)**2*(2.*y-6.*y*y+4*y*y*y)
    return val

def velocity_y(x,y):
    val=-y*y*(1.-y)**2*(2.*x-6.*x*x+4*x*x*x)
    return val

def pressure(x,y):
    val=x*(1.-x)-1./6.
    return val

###############################################################################

print("-----------------------------")
print("--------- stone 150 ---------")
print("-----------------------------")

ndim=2
ndofV=2  # number of velocity degrees of freedom per node
ndofP=1  # number of pressure degrees of freedom 

Lx=1.
Ly=1.

if int(len(sys.argv) == 2):
   nelx = int(sys.argv[1])
else:
   nelx = 16

nely=nelx

nel=nelx*nely
nnx=2*nelx+1  # number of elements, x direction
nny=2*nely+1  # number of elements, y direction
NV=nnx*nny

NP=(nelx+1)*(nely+1)
mV=9     # number of velocity nodes making up an element
mP=4     # number of pressure nodes making up an element
rVnodes=[-1,0,+1,-1,0,+1,-1,0,+1]
sVnodes=[-1,-1,-1,0,0,0,+1,+1,+1]

ndofV=2
ndofP=1

NfemV=NV*ndofV       # number of velocity dofs
NfemP=NP*ndofP       # number of pressure dofs
Nfem=NfemV+NfemP     # total nb of dofs

eps=1e-9
eta=1.

hx=Lx/nelx
hy=Ly/nely

visu = 1

###############################################################################

nqperdim=3
qcoords=[-np.sqrt(3./5.),0.,np.sqrt(3./5.)]
qweights=[5./9.,8./9.,5./9.]
nqel=nqperdim**ndim

###############################################################################

print ('nelx     =',nelx)
print ('nely     =',nely)
print ('nnx      =',nnx)
print ('nny      =',nny)
print ('NV       =',NV)
print ('NP       =',NP)
print ('nel      =',nel)
print ('NfemV    =',NfemV)
print ('NfemP    =',NfemP)
print ('Nfem     =',Nfem)
print ('nqperdim =',nqperdim)
print("-----------------------------")

###############################################################################
# build velocity nodes coordinates 
###############################################################################
start = timing.time()

xV=np.zeros(NV,dtype=np.float64)  # x coordinates
yV=np.zeros(NV,dtype=np.float64)  # y coordinates

counter=0    
for j in range(0,nny):
    for i in range(0,nnx):
        xV[counter]=i*hx/2
        yV[counter]=j*hy/2
        counter+=1

print("build V grid: %.3f s" % (timing.time() - start))

###############################################################################
# connectivity
###############################################################################
start = timing.time()

iconV=np.zeros((mV,nel),dtype=np.int32)

counter=0
for j in range(0,nely):
    for i in range(0,nelx):
        counter2=0
        for k in range(0,3):
            for l in range(0,3):
                iconV[counter2,counter]=i*2+l+j*2*nnx+nnx*k
                counter2+=1
        counter += 1

print("build iconV: %.3f s" % (timing.time() - start))

###############################################################################
# build pressure grid 
###############################################################################
start = timing.time()

xP=np.empty(NP,dtype=np.float64)     # x coordinates
yP=np.empty(NP,dtype=np.float64)     # y coordinates
      
counter=0    
for j in range(0,(2-1)*nely+1):
    for i in range(0,(2-1)*nelx+1):
        xP[counter]=i*hx/(2-1)
        yP[counter]=j*hy/(2-1)
        counter+=1

#np.savetxt('gridP.ascii',np.array([xP,yP]).T,header='# x,y')

print("build P grid: %.3f s" % (timing.time() - start))

###############################################################################
# build pressure connectivity array 
###############################################################################
start = timing.time()

iconP=np.zeros((mP,nel),dtype=np.int32)

om1=2-1
counter=0
for j in range(0,nely):
    for i in range(0,nelx):
        counter2=0
        for k in range(0,2):
            for l in range(0,2):
                iconP[counter2,counter]=i*om1+l+j*om1*(om1*nelx+1)+(om1*nelx+1)*k 
                counter2+=1
        counter += 1

#print("-------iconP--------")
#for iel in range (0,nel):
#    print ("iel=",iel)
#    for i in range(0,mP):
#        print ("node ",i,':',iconP[i,iel],"at pos.",xP[iconP[i,iel]], yP[iconP[i,iel]])

print("build iconP: %.3f s" % (timing.time() - start))

###############################################################################
# define boundary conditions
###############################################################################
start = timing.time()

bc_fix=np.zeros(NfemV,dtype=bool)  # boundary condition, yes/no
bc_val=np.zeros(NfemV,dtype=np.float64)  # boundary condition, value

for i in range(0,NV):
    if xV[i]<eps:
       bc_fix[i*ndofV]   = True ; bc_val[i*ndofV]   = 0.
       bc_fix[i*ndofV+1] = True ; bc_val[i*ndofV+1] = 0.
    if xV[i]>(Lx-eps):
       bc_fix[i*ndofV]   = True ; bc_val[i*ndofV]   = 0.
       bc_fix[i*ndofV+1] = True ; bc_val[i*ndofV+1] = 0.
    if yV[i]<eps:
       bc_fix[i*ndofV]   = True ; bc_val[i*ndofV]   = 0.
       bc_fix[i*ndofV+1] = True ; bc_val[i*ndofV+1] = 0.
    if yV[i]>(Ly-eps):
       bc_fix[i*ndofV]   = True ; bc_val[i*ndofV]   = 0.
       bc_fix[i*ndofV+1] = True ; bc_val[i*ndofV+1] = 0.

print("boundary conditions: %.3f s" % (timing.time() - start))

###############################################################################
# compute area of elements
###############################################################################
start = timing.time()

area    = np.zeros(nel,dtype=np.float64) 
dNNNVdr = np.zeros(mV,dtype=np.float64)  # shape functions derivatives
dNNNVds = np.zeros(mV,dtype=np.float64)  # shape functions derivatives

for iel in range(0,nel):
    for iq in range(0,nqperdim):
        for jq in range(0,nqperdim):
            rq=qcoords[iq]
            sq=qcoords[jq]
            weightq=qweights[iq]*qweights[jq]
            dNNNVdr[0:mV]=dNNVdr(rq,sq)
            dNNNVds[0:mV]=dNNVds(rq,sq)
            jcb=np.zeros((ndim,ndim),dtype=np.float64)
            for k in range(0,mV):
                jcb[0,0] += dNNNVdr[k]*xV[iconV[k,iel]]
                jcb[0,1] += dNNNVdr[k]*yV[iconV[k,iel]]
                jcb[1,0] += dNNNVds[k]*xV[iconV[k,iel]]
                jcb[1,1] += dNNNVds[k]*yV[iconV[k,iel]]
            jcob = np.linalg.det(jcb)
            area[iel]+=jcob*weightq

print("     -> area (m,M) %.4e %.4e " %(np.min(area),np.max(area)))
print("     -> total area %.6f " %(area.sum()))

print("compute elements areas: %.3f s" % (timing.time() - start))

###############################################################################
# precompute basis functions values at q points
###############################################################################
start = timing.time()

jcbi=np.zeros((ndim,ndim),dtype=np.float64)
jcbi[0,0]=2/hx
jcbi[1,1]=2/hy
jcob=hx*hy/4

NNNV=np.zeros((nqel,mV),dtype=np.float64) 
NNNP=np.zeros((nqel,mP),dtype=np.float64) 
dNNNVdr=np.zeros((nqel,mV),dtype=np.float64) 
dNNNVds=np.zeros((nqel,mV),dtype=np.float64) 
dNNNVdx=np.zeros((nqel,mV),dtype=np.float64) 
dNNNVdy=np.zeros((nqel,mV),dtype=np.float64) 
rq=np.zeros(nqel,dtype=np.float64) 
sq=np.zeros(nqel,dtype=np.float64) 
weightq=np.zeros(nqel,dtype=np.float64) 
   
counterq=0 
for iq in range(0,nqperdim):
    for jq in range(0,nqperdim):
        rq[counterq]=qcoords[iq]
        sq[counterq]=qcoords[jq]
        weightq[counterq]=qweights[iq]*qweights[jq]
        NNNV[counterq,0:mV]=NNV(rq[counterq],sq[counterq])
        dNNNVdr[counterq,0:mV]=dNNVdr(rq[counterq],sq[counterq])
        dNNNVds[counterq,0:mV]=dNNVds(rq[counterq],sq[counterq])
        NNNP[counterq,0:mP]=NNP(rq[counterq],sq[counterq])
        dNNNVdx[counterq,0:mV]=jcbi[0,0]*dNNNVdr[counterq,0:mV]
        dNNNVdy[counterq,0:mV]=jcbi[1,1]*dNNNVds[counterq,0:mV]
        counterq+=1

print("compute N & grad(N) at q pts: %.3f s" % (timing.time() - start))

###############################################################################
# build FE matrix
# [ K G ][u]=[f]
# [GT 0 ][p] [h]
###############################################################################
start = timing.time()

A_sparse=lil_matrix((Nfem,Nfem),dtype=np.float64)
f_rhs=np.zeros(NfemV,dtype=np.float64)        # right hand side f 
h_rhs=np.zeros(NfemP,dtype=np.float64)        # right hand side h 
b_mat=np.zeros((3,ndofV*mV),dtype=np.float64) # gradient matrix B 
N_mat=np.zeros((3,ndofP*mP),dtype=np.float64) # matrix N 
c_mat=np.array([[2,0,0],[0,2,0],[0,0,1]],dtype=np.float64) 

for iel in range(0,nel):

    f_el=np.zeros((mV*ndofV),dtype=np.float64)
    K_el=np.zeros((mV*ndofV,mV*ndofV),dtype=np.float64)
    G_el=np.zeros((mV*ndofV,mP),dtype=np.float64)
    h_el=np.zeros((mP),dtype=np.float64)

    for iq in range(0,nqel):

        xq=0.0
        yq=0.0
        for k in range(0,mV):
            xq+=NNNV[iq,k]*xV[iconV[k,iel]]
            yq+=NNNV[iq,k]*yV[iconV[k,iel]]

        for i in range(0,mV):
            b_mat[0:3, 2*i:2*i+2] = [[dNNNVdx[iq,i],0.           ],
                                     [0.           ,dNNNVdy[iq,i]],
                                     [dNNNVdy[iq,i],dNNNVdx[iq,i]]]

        K_el+=b_mat.T.dot(c_mat.dot(b_mat))*eta*weightq[iq]*jcob

        for i in range(0,mV):
            f_el[ndofV*i  ]+=NNNV[iq,i]*jcob*weightq[iq]*bx(xq,yq)
            f_el[ndofV*i+1]+=NNNV[iq,i]*jcob*weightq[iq]*by(xq,yq)

        for i in range(0,mP):
            N_mat[0,i]=NNNP[iq,i]
            N_mat[1,i]=NNNP[iq,i]
            N_mat[2,i]=0.

        G_el-=b_mat.T.dot(N_mat)*weightq[iq]*jcob

    # end for iq

    # impose b.c. 
    for k1 in range(0,mV):
        for i1 in range(0,ndofV):
            ikk=ndofV*k1          +i1
            m1 =ndofV*iconV[k1,iel]+i1
            if bc_fix[m1]:
               K_ref=K_el[ikk,ikk] 
               for jkk in range(0,mV*ndofV):
                   f_el[jkk]-=K_el[jkk,ikk]*bc_val[m1]
                   K_el[ikk,jkk]=0
                   K_el[jkk,ikk]=0
               K_el[ikk,ikk]=K_ref
               f_el[ikk]=K_ref*bc_val[m1]
               h_el[:]-=G_el[ikk,:]*bc_val[m1]
               G_el[ikk,:]=0

    # assemble matrix K_mat and right hand side rhs
    for k1 in range(0,mV):
        for i1 in range(0,ndofV):
            ikk=ndofV*k1          +i1
            m1 =ndofV*iconV[k1,iel]+i1
            for k2 in range(0,mV):
                for i2 in range(0,ndofV):
                    jkk=ndofV*k2          +i2
                    m2 =ndofV*iconV[k2,iel]+i2
                    A_sparse[m1,m2] += K_el[ikk,jkk]
            for k2 in range(0,mP):
                jkk=k2
                m2 =iconP[k2,iel]
                A_sparse[m1,NfemV+m2]+=G_el[ikk,jkk]
                A_sparse[NfemV+m2,m1]+=G_el[ikk,jkk]
            f_rhs[m1]+=f_el[ikk]
    for k2 in range(0,mP):
        m2=iconP[k2,iel]
        h_rhs[m2]+=h_el[k2]

print("build FE matrix: %.3fs - %d elts" % (timing.time()-start, nel))

###############################################################################
# solve system
###############################################################################
start = timing.time()
   
rhs = np.zeros(Nfem,dtype=np.float64)         # right hand side of Ax=b
rhs[0:NfemV]=f_rhs
rhs[NfemV:Nfem]=h_rhs

sparse_matrix=A_sparse.tocsr()

sol=sps.linalg.spsolve(sparse_matrix,rhs)

print("solve time: %.3f s - %d elts" % (timing.time() - start,nel))

###############################################################################
# put solution into separate x,y velocity arrays
###############################################################################
start = timing.time()

u,v=np.reshape(sol[0:NfemV],(NV,2)).T

p=sol[NfemV:Nfem]

print("     -> u (m,M) %.4f %.4f " %(np.min(u),np.max(u)))
print("     -> v (m,M) %.4f %.4f " %(np.min(v),np.max(v)))
print("     -> p (m,M) %.4f %.4f " %(np.min(p),np.max(p)))

#np.savetxt('velocity.ascii',np.array([xV,yV,u,v]).T,header='# x,y,u,v')
#np.savetxt('pressure.ascii',np.array([xP,yP,p]).T,header='# x,y,p')

print("split vel into u,v: %.3f s" % (timing.time() - start))

###############################################################################
# normalise pressure
###############################################################################
start = timing.time()

avrgP=0
for iel in range(0,nel):
    for iq in range(0,nqel):
        pq=0.
        for k in range(0,mP):
            pq+=NNNP[iq,k]*p[iconP[k,iel]]
        avrgP+=pq*jcob*weightq[iq]
    # end for iq
#end iel

p-=(avrgP/Lx/Ly)

print("     -> p (m,M) %.4f %.4f " %(np.min(p),np.max(p)))

print("normalise pressure: %.3f s - %d elts" % (timing.time() - start,nel))

###############################################################################
# project pressure onto velocity grid
###############################################################################
start = timing.time()

q=np.zeros(NV,dtype=np.float64)
c=np.zeros(NV,dtype=np.float64)

for iel in range(0,nel):
    for i in range(0,mV):
        #NNNP[0:mP]=NNP(rVnodes[i],sVnodes[i])
        #q[iconV[i,iel]]+=np.dot(p[iconP[0:mP,iel]],NNNP[0:mP])
        q[iconV[i,iel]]+=np.dot(p[iconP[0:mP,iel]],NNP(rVnodes[i],sVnodes[i]))
        c[iconV[i,iel]]+=1.

q=q/c

#np.savetxt('q.ascii',np.array([xV,yV,q]).T,header='# x,y,q')

print("project p onto Vnodes: %.3f s" % (timing.time() - start))

###############################################################################
# compute error fields for plotting
###############################################################################
start = timing.time()

error_u = np.empty(NV,dtype=np.float64)
error_v = np.empty(NV,dtype=np.float64)
error_p = np.empty(NP,dtype=np.float64)
error_q = np.empty(NV,dtype=np.float64)

for i in range(0,NV): 
    error_u[i]=u[i]-velocity_x(xV[i],yV[i])
    error_v[i]=v[i]-velocity_y(xV[i],yV[i])
    error_q[i]=q[i]-pressure(xV[i],yV[i])

for i in range(0,NP): 
    error_p[i]=p[i]-pressure(xP[i],yP[i])

print("     -> error_u (m,M) %.4e %.4e " %(np.min(error_u),np.max(error_u)))
print("     -> error_v (m,M) %.4e %.4e " %(np.min(error_v),np.max(error_v)))
print("     -> error_p (m,M) %.4e %.4e " %(np.min(error_p),np.max(error_p)))
print("     -> error_q (m,M) %.4e %.4e " %(np.min(error_q),np.max(error_q)))

print("compute error fields: %.3f s" % (timing.time() - start))

###############################################################################
# compute L2 errors
###############################################################################
start = timing.time()

errv=0.
errp=0.
errq=0.
for iel in range (0,nel):
    for iq in range(0,nqel):

        xq=0.
        yq=0.
        uq=0.
        vq=0.
        qq=0.
        for k in range(0,mV):
            xq+=NNNV[iq,k]*xV[iconV[k,iel]]
            yq+=NNNV[iq,k]*yV[iconV[k,iel]]
            uq+=NNNV[iq,k]*u[iconV[k,iel]]
            vq+=NNNV[iq,k]*v[iconV[k,iel]]
            qq+=NNNV[iq,k]*q[iconV[k,iel]]
        errv+=((uq-velocity_x(xq,yq))**2+(vq-velocity_y(xq,yq))**2)*weightq[iq]*jcob
        errq+=(qq-pressure(xq,yq))**2*weightq[iq]*jcob

        xq=0.
        yq=0.
        pq=0.
        for k in range(0,mP):
            xq+=NNNP[iq,k]*xP[iconP[k,iel]]
            yq+=NNNP[iq,k]*yP[iconP[k,iel]]
            pq+=NNNP[iq,k]*p[iconP[k,iel]]
        errp+=(pq-pressure(xq,yq))**2*weightq[iq]*jcob

    # end for iq
# end for iel

errv=np.sqrt(errv)
errp=np.sqrt(errp)
errq=np.sqrt(errq)

print("     -> nel= %6d ; errv= %.8e ; errp= %.8e ; errq= %.8e" %(nel,errv,errp,errq))

print("compute errors: %.3f s - %d elts" % (timing.time() - start,nel))

###############################################################################
# plot of solution
###############################################################################

if visu==1:
    vtufile=open('solution_'+str(nelx)+'.vtu',"w")
    vtufile.write("<VTKFile type='UnstructuredGrid' version='0.1' byte_order='BigEndian'> \n")
    vtufile.write("<UnstructuredGrid> \n")
    vtufile.write("<Piece NumberOfPoints=' %5d ' NumberOfCells=' %5d '> \n" %(NV,nel))
    #####
    vtufile.write("<Points> \n")
    vtufile.write("<DataArray type='Float32' NumberOfComponents='3' Format='ascii'> \n")
    for i in range(0,NV):
        vtufile.write("%10e %10e %10e \n" %(xV[i],yV[i],0.))
    vtufile.write("</DataArray>\n")
    vtufile.write("</Points> \n")
    #####
    vtufile.write("<CellData Scalars='scalars'>\n")
    #--
    vtufile.write("<DataArray type='Float32' Name='area' Format='ascii'> \n")
    for iel in range (0,nel):
        vtufile.write("%10e\n" % (area[iel]))
    vtufile.write("</DataArray>\n")
    #--
    vtufile.write("</CellData>\n")
    #####
    vtufile.write("<PointData Scalars='scalars'>\n")
    #--
    vtufile.write("<DataArray type='Float32' NumberOfComponents='3' Name='velocity' Format='ascii'> \n")
    for i in range(0,NV):
        vtufile.write("%10e %10e %10e \n" %(u[i],v[i],0.))
    vtufile.write("</DataArray>\n")
    #--
    vtufile.write("<DataArray type='Float32' Name='q' Format='ascii'> \n")
    for i in range(0,NV):
        vtufile.write("%10e \n" %q[i])
    vtufile.write("</DataArray>\n")
    #--
    vtufile.write("<DataArray type='Float32' Name='error u' Format='ascii'> \n")
    for i in range(0,NV):
        vtufile.write("%.5e \n" %error_u[i])
    vtufile.write("</DataArray>\n")
    #--
    vtufile.write("<DataArray type='Float32' Name='error v' Format='ascii'> \n")
    for i in range(0,NV):
        vtufile.write("%.5e \n" %error_v[i])
    vtufile.write("</DataArray>\n")
    #--
    vtufile.write("<DataArray type='Float32' Name='error q' Format='ascii'> \n")
    for i in range(0,NV):
        vtufile.write("%.5e \n" %error_q[i])
    vtufile.write("</DataArray>\n")
    #--
    vtufile.write("</PointData>\n")
    #####
    vtufile.write("<Cells>\n")
    #--
    vtufile.write("<DataArray type='Int32' Name='connectivity' Format='ascii'> \n")
    for iel in range (0,nel):
        vtufile.write("%d %d %d %d \n" %(iconV[0,iel],iconV[2,iel],iconV[8,iel],iconV[6,iel]))
    vtufile.write("</DataArray>\n")
    #--
    vtufile.write("<DataArray type='Int32' Name='offsets' Format='ascii'> \n")
    for iel in range (0,nel):
        vtufile.write("%d \n" %((iel+1)*4))
    vtufile.write("</DataArray>\n")
    #--
    vtufile.write("<DataArray type='Int32' Name='types' Format='ascii'>\n")
    for iel in range (0,nel):
        vtufile.write("%d \n" %9)
    vtufile.write("</DataArray>\n")
    #--
    vtufile.write("</Cells>\n")
    #####
    vtufile.write("</Piece>\n")
    vtufile.write("</UnstructuredGrid>\n")
    vtufile.write("</VTKFile>\n")
    vtufile.close()

print("-----------------------------")
print("------------the end----------")
print("-----------------------------")

###############################################################################
###############################################################################
