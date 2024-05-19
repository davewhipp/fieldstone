import numpy as np
import FEbasis2D as FE
import matplotlib.pyplot as plt

###############################################################################

def quadrature(space,nqpts):

    if nqpts==0: exit('nqpts=0!')

    if space=='Q1' or space=='Q2' or space=='Q2s' or space=='Q3' or space=='Q4' or\
       space=='Q1+' or space=='DSSY1' or space=='DSSY2' or space=='RT1' or space=='RT2' or\
       space=='Han' or space=='Chen':
       coords=qcoords_1D(nqpts)
       weights=qweights_1D(nqpts)
       nq=nqpts**2 
       val_r = np.zeros(nq,dtype=np.float64) 
       val_s = np.zeros(nq,dtype=np.float64) 
       val_w = np.zeros(nq,dtype=np.float64) 
       counter=0
       for iq in range(0,nqpts):
           for jq in range(0,nqpts):
               val_r[counter]=coords[iq]
               val_s[counter]=coords[jq]
               val_w[counter]=weights[iq]*weights[jq]
               counter+=1

    elif space=='P1' or space=='P2' or space=='P1+' or\
         space=='P2+' or space=='P3' or space=='P4' or space=='P1NC':

       nq=nqpts
       val_r = np.zeros(nq,dtype=np.float64) 
       val_s = np.zeros(nq,dtype=np.float64) 
       val_w = np.zeros(nq,dtype=np.float64) 

       if nq==1: #linear 1st order - confirmed
          val_r[0]=1/3 ; val_s[0]=1/3 ; val_w[0]=1/2

       elif nq==3: #quadratic 2nd order - confirmed
          val_r[0]=1/6 ; val_s[0]=1/6 ; val_w[0]=1/3/2
          val_r[1]=2/3 ; val_s[1]=1/6 ; val_w[1]=1/3/2
          val_r[2]=1/6 ; val_s[2]=2/3 ; val_w[2]=1/3/2

       elif nq==4: #cubic 3rd order - confirmed 
          val_r[0]=1/3 ; val_r[0]=1/3 ; val_w[0]=-27/48/2
          val_r[1]=1/5 ; val_r[1]=3/5 ; val_w[1]= 25/48/2
          val_r[2]=1/5 ; val_r[2]=1/5 ; val_w[2]= 25/48/2
          val_r[3]=3/5 ; val_r[3]=1/5 ; val_w[3]= 25/48/2

       elif nq==6: #4th order - confirmed
          val_r[0]=0.091576213509771 ; val_s[0]=0.091576213509771 ; val_w[0]=0.109951743655322/2.0 
          val_r[1]=0.816847572980459 ; val_s[1]=0.091576213509771 ; val_w[1]=0.109951743655322/2.0 
          val_r[2]=0.091576213509771 ; val_s[2]=0.816847572980459 ; val_w[2]=0.109951743655322/2.0 
          val_r[3]=0.445948490915965 ; val_s[3]=0.445948490915965 ; val_w[3]=0.223381589678011/2.0 
          val_r[4]=0.108103018168070 ; val_s[4]=0.445948490915965 ; val_w[4]=0.223381589678011/2.0 
          val_r[5]=0.445948490915965 ; val_s[5]=0.108103018168070 ; val_w[5]=0.223381589678011/2.0 

       elif nq==7: #5th order - confirmed
          val_r[0]=0.1012865073235 ; val_s[0]=0.1012865073235 ; val_w[0]=0.0629695902724 
          val_r[1]=0.7974269853531 ; val_s[1]=0.1012865073235 ; val_w[1]=0.0629695902724 
          val_r[2]=0.1012865073235 ; val_s[2]=0.7974269853531 ; val_w[2]=0.0629695902724 
          val_r[3]=0.4701420641051 ; val_s[3]=0.0597158717898 ; val_w[3]=0.0661970763942 
          val_r[4]=0.4701420641051 ; val_s[4]=0.4701420641051 ; val_w[4]=0.0661970763942 
          val_r[5]=0.0597158717898 ; val_s[5]=0.4701420641051 ; val_w[5]=0.0661970763942 
          val_r[6]=0.3333333333333 ; val_s[6]=0.3333333333333 ; val_w[6]=0.1125000000000 

       elif nq==12: #6th order - confirmed
          val_r[ 0]=0.24928674517091 ; val_s[ 0]=0.24928674517091 ; val_w[ 0]=0.11678627572638/2
          val_r[ 1]=0.24928674517091 ; val_s[ 1]=0.50142650965818 ; val_w[ 1]=0.11678627572638/2
          val_r[ 2]=0.50142650965818 ; val_s[ 2]=0.24928674517091 ; val_w[ 2]=0.11678627572638/2
          val_r[ 3]=0.06308901449150 ; val_s[ 3]=0.06308901449150 ; val_w[ 3]=0.05084490637021/2
          val_r[ 4]=0.06308901449150 ; val_s[ 4]=0.87382197101700 ; val_w[ 4]=0.05084490637021/2
          val_r[ 5]=0.87382197101700 ; val_s[ 5]=0.06308901449150 ; val_w[ 5]=0.05084490637021/2
          val_r[ 6]=0.31035245103378 ; val_s[ 6]=0.63650249912140 ; val_w[ 6]=0.08285107561837/2
          val_r[ 7]=0.63650249912140 ; val_s[ 7]=0.05314504984482 ; val_w[ 7]=0.08285107561837/2
          val_r[ 8]=0.05314504984482 ; val_s[ 8]=0.31035245103378 ; val_w[ 8]=0.08285107561837/2
          val_r[ 9]=0.63650249912140 ; val_s[ 9]=0.31035245103378 ; val_w[ 9]=0.08285107561837/2
          val_r[10]=0.31035245103378 ; val_s[10]=0.05314504984482 ; val_w[10]=0.08285107561837/2
          val_r[11]=0.05314504984482 ; val_s[11]=0.63650249912140 ; val_w[11]=0.08285107561837/2

       elif nq==13: #7th order - confirmed

          val_r[ 0]=0.33333333333333 ; val_s[ 0]=0.33333333333333 ; val_w[ 0]=-0.14957004446768/2
          val_r[ 1]=0.26034596607904 ; val_s[ 1]=0.26034596607904 ; val_w[ 1]=0.17561525743321/2
          val_r[ 2]=0.26034596607904 ; val_s[ 2]=0.47930806784192 ; val_w[ 2]=0.17561525743321/2
          val_r[ 3]=0.47930806784192 ; val_s[ 3]=0.26034596607904 ; val_w[ 3]=0.17561525743321/2
          val_r[ 4]=0.06513010290222 ; val_s[ 4]=0.06513010290222 ; val_w[ 4]=0.05334723560884/2
          val_r[ 5]=0.06513010290222 ; val_s[ 5]=0.86973979419557 ; val_w[ 5]=0.05334723560884/2
          val_r[ 6]=0.86973979419557 ; val_s[ 6]=0.06513010290222 ; val_w[ 6]=0.05334723560884/2
          val_r[ 7]=0.31286549600487 ; val_s[ 7]=0.63844418856981 ; val_w[ 7]=0.07711376089026/2
          val_r[ 8]=0.63844418856981 ; val_s[ 8]=0.04869031542532 ; val_w[ 8]=0.07711376089026/2
          val_r[ 9]=0.04869031542532 ; val_s[ 9]=0.31286549600487 ; val_w[ 9]=0.07711376089026/2
          val_r[10]=0.63844418856981 ; val_s[10]=0.31286549600487 ; val_w[10]=0.07711376089026/2
          val_r[11]=0.31286549600487 ; val_s[11]=0.04869031542532 ; val_w[11]=0.07711376089026/2
          val_r[12]=0.04869031542532 ; val_s[12]=0.63844418856981 ; val_w[12]=0.07711376089026/2

       elif nq==16: #8th order - confirmed

          val_r[ 0]=0.33333333333333 ; val_s[ 0]=0.33333333333333 ; val_w[ 0]=0.14431560767779/2
          val_r[ 1]=0.45929258829272 ; val_s[ 1]=0.45929258829272 ; val_w[ 1]=0.09509163426728/2
          val_r[ 2]=0.45929258829272 ; val_s[ 2]=0.08141482341455 ; val_w[ 2]=0.09509163426728/2
          val_r[ 3]=0.08141482341455 ; val_s[ 3]=0.45929258829272 ; val_w[ 3]=0.09509163426728/2
          val_r[ 4]=0.17056930775176 ; val_s[ 4]=0.17056930775176 ; val_w[ 4]=0.10321737053472/2
          val_r[ 5]=0.17056930775176 ; val_s[ 5]=0.65886138449648 ; val_w[ 5]=0.10321737053472/2
          val_r[ 6]=0.65886138449648 ; val_s[ 6]=0.17056930775176 ; val_w[ 6]=0.10321737053472/2
          val_r[ 7]=0.05054722831703 ; val_s[ 7]=0.05054722831703 ; val_w[ 7]=0.03245849762320/2
          val_r[ 8]=0.05054722831703 ; val_s[ 8]=0.89890554336594 ; val_w[ 8]=0.03245849762320/2
          val_r[ 9]=0.89890554336594 ; val_s[ 9]=0.05054722831703 ; val_w[ 9]=0.03245849762320/2
          val_r[10]=0.26311282963464 ; val_s[10]=0.72849239295540 ; val_w[10]=0.02723031417443/2
          val_r[11]=0.72849239295540 ; val_s[11]=0.00839477740996 ; val_w[11]=0.02723031417443/2
          val_r[12]=0.00839477740996 ; val_s[12]=0.26311282963464 ; val_w[12]=0.02723031417443/2
          val_r[13]=0.72849239295540 ; val_s[13]=0.26311282963464 ; val_w[13]=0.02723031417443/2
          val_r[14]=0.26311282963464 ; val_s[14]=0.00839477740996 ; val_w[14]=0.02723031417443/2
          val_r[15]=0.00839477740996 ; val_s[15]=0.72849239295540 ; val_w[15]=0.02723031417443/2

       elif nq==19: #9th order - duna85
           #https://mathsfromnothing.au/triangle-quadrature-rules/?i=1

           val_r[ 1]=0. ; val_s[ 1]=0. ; val_w[ 1]=0.097135796282799 /2
           val_r[ 2]=0. ; val_s[ 2]=0. ; val_w[ 2]=0.031334700227139 /2
           val_r[ 3]=0. ; val_s[ 3]=0. ; val_w[ 3]=0.031334700227139 /2
           val_r[ 4]=0. ; val_s[ 4]=0. ; val_w[ 4]=0.031334700227139 /2
           val_r[ 5]=0. ; val_s[ 5]=0. ; val_w[ 5]=0.077827541004774 /2
           val_r[ 6]=0. ; val_s[ 6]=0. ; val_w[ 6]=0.077827541004774/2
           val_r[ 7]=0. ; val_s[ 7]=0. ; val_w[ 7]=0.077827541004774 /2
           val_r[ 8]=0. ; val_s[ 8]=0. ; val_w[ 8]=0.079647738927210 /2
           val_r[ 9]=0. ; val_s[ 9]=0. ; val_w[ 9]=0.079647738927210 /2
           val_r[10]=0. ; val_s[10]=0. ; val_w[10]=0.079647738927210 /2
           val_r[11]=0. ; val_s[11]=0. ; val_w[11]=0.043283539377289 /2
           val_r[12]=0. ; val_s[12]=0. ; val_w[12]=0.043283539377289 /2
           val_r[13]=0. ; val_s[13]=0. ; val_w[13]=0.043283539377289 /2
           val_r[14]=0. ; val_s[14]=0. ; val_w[14]=0.043283539377289 /2
           val_r[15]=0. ; val_s[15]=0. ; val_w[15]=0.043283539377289 /2
           val_r[16]=0. ; val_s[16]=0. ; val_w[16]=0.043283539377289 /2
           val_r[17]=0. ; val_s[17]=0. ; val_w[17]=0.025577675658698 /2
           val_r[18]=0. ; val_s[18]=0. ; val_w[18]=0.025577675658698 /2
           val_r[19]=0. ; val_s[19]=0. ; val_w[19]=0.025577675658698 /2


       else:
          exit('quadrature: nqpts not available')

    else:
       exit('quadrature: unknown space')

    return nq,val_r,val_s,val_w

###############################################################################

def qcoords_1D(nqpts):

    val = np.zeros(nqpts,dtype=np.float64) 

    if nqpts==1: 
       val[0]=0

    if nqpts==2: 
       val=[-1./np.sqrt(3.),1./np.sqrt(3.)]

    if nqpts==3: 
       val=[-np.sqrt(3/5),0.,np.sqrt(3/5)]

    if nqpts==4: 
       qc4a=np.sqrt(3./7.+2./7.*np.sqrt(6./5.))
       qc4b=np.sqrt(3./7.-2./7.*np.sqrt(6./5.))
       val=[-qc4a,-qc4b,qc4b,qc4a]

    if nqpts==5: 
       qc5a=np.sqrt(5.+2.*np.sqrt(10./7.))/3.
       qc5b=np.sqrt(5.-2.*np.sqrt(10./7.))/3.
       qc5c=0.
       val=[-qc5a,-qc5b,qc5c,qc5b,qc5a]

    if nqpts==6:
       val=[-0.932469514203152,\
            -0.661209386466265,\
            -0.238619186083197,\
            +0.238619186083197,\
            +0.661209386466265,\
            +0.932469514203152]

    if nqpts==7:
       val=[-0.9491079123427585,\
            -0.7415311855993945,\
            -0.4058451513773972,\
             0.0000000000000000,\
             0.4058451513773972,\
             0.7415311855993945,\
             0.9491079123427585]

    if nqpts==8:
       val=[-0.9602898564975363,\
            -0.7966664774136267,\
            -0.5255324099163290,\
            -0.1834346424956498,\
             0.1834346424956498,\
             0.5255324099163290,\
             0.7966664774136267,\
             0.9602898564975363]

    if nqpts==9:
       val=[-0.9681602395076261,\
            -0.8360311073266358,\
            -0.6133714327005904,\
            -0.3242534234038089,\
             0.0000000000000000,\
             0.3242534234038089,\
             0.6133714327005904,\
             0.8360311073266358,\
             0.9681602395076261]

    if nqpts==10:
       val=[-0.973906528517172,\
            -0.865063366688985,\
            -0.679409568299024,\
            -0.433395394129247,\
            -0.148874338981631,\
             0.148874338981631,\
             0.433395394129247,\
             0.679409568299024,\
             0.865063366688985,\
             0.973906528517172]

    return val

###############################################################################

def qweights_1D(nqpts):

    val = np.zeros(nqpts,dtype=np.float64) 

    if nqpts==1:
       val[0]=2

    if nqpts==2:
       val=[1.,1.]

    if nqpts==3:
       val=[5/9,8/9,5/9]

    if nqpts==4:
       qw4a=(18-np.sqrt(30.))/36.
       qw4b=(18+np.sqrt(30.))/36
       val=[qw4a,qw4b,qw4b,qw4a]

    if nqpts==5: 
       qw5a=(322.-13.*np.sqrt(70.))/900.
       qw5b=(322.+13.*np.sqrt(70.))/900.
       qw5c=128./225.
       val=[qw5a,qw5b,qw5c,qw5b,qw5a]

    if nqpts==6:
       val=[0.171324492379170,\
            0.360761573048139,\
            0.467913934572691,\
            0.467913934572691,\
            0.360761573048139,\
            0.171324492379170]

    if nqpts==7:
       val=[0.1294849661688697,\
            0.2797053914892766,\
            0.3818300505051189,\
            0.4179591836734694,\
            0.3818300505051189,\
            0.2797053914892766,\
            0.1294849661688697]

    if nqpts==8:
       val=[0.1012285362903763,\
            0.2223810344533745,\
            0.3137066458778873,\
            0.3626837833783620,\
            0.3626837833783620,\
            0.3137066458778873,\
            0.2223810344533745,\
            0.1012285362903763]

    if nqpts==9:
       val=[0.0812743883615744,\
            0.1806481606948574,\
            0.2606106964029354,\
            0.3123470770400029,\
            0.3302393550012598,\
            0.3123470770400029,\
            0.2606106964029354,\
            0.1806481606948574,\
            0.0812743883615744]

    if nqpts==10:
       val=[0.066671344308688,\
            0.149451349150581,\
            0.219086362515982,\
            0.269266719309996,\
            0.295524224714753,\
            0.295524224714753,\
            0.269266719309996,\
            0.219086362515982,\
            0.149451349150581,\
            0.066671344308688]

    return val

###############################################################################

def visualise_quadrature_points(space,nqpts):
    r=FE.NNN_r(space)
    s=FE.NNN_s(space)

    nq,rq,sq,wq=quadrature(space,nqpts)
    plt.figure()
    plt.scatter(rq,sq,s=50,color='orange',marker='+')
    plt.scatter(r,s,color='teal',s=10)
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.25)
    plt.xlabel('r')
    plt.ylabel('s')
    plt.title(space)

    if space=='Q1' or space=='Q2' or space=='Q3' or space=='Q4' or space=='Q1+' or\
       space=='DSSY1' or space=='DSSY2' or space=='RT1' or space=='RT2' or space=='Q2s':
       plt.xlim([-1.1,+1.1])
       plt.ylim([-1.1,+1.1])
       plt.plot([-1,1,1,-1,-1],[-1,-1,1,1,-1],color='teal',linewidth=2)
    elif space=='P1' or space=='P2' or space=='P1+' or space=='P2+' or space=='P3' or space=='P4':
       plt.xlim([-0.1,+1.1])
       plt.ylim([-0.1,+1.1])
       plt.plot([0,0,1,0],[0,1,0,0],color='teal',linewidth=2)
    else:
       exit('visualise_quadrature_points: unknown space')
    plt.savefig(space+'_quadrature_points'+str(nqpts)+'.pdf',bbox_inches='tight')
    print('     -> generated '+space+'_quadrature_points'+str(nqpts)+'.pdf')
    plt.close()

###############################################################################

def nqpts_default(space):
    if space=='Q1':      
       nqpts=2
    elif space=='Q2':    
       nqpts=3
    elif space=='Q3':    
       nqpts=4
    elif space=='Q4':    
       nqpts=5
    elif space=='Q1+':   
       nqpts=3
    elif space=='Q2+':   
       nqpts=3
    elif space=='Han':   
       nqpts=4
    elif space=='Chen':  
       nqpts=3
    elif space=='DSSY1': 
       nqpts=3
    elif space=='DSSY2': 
       nqpts=3
    elif space=='RT1':   
       nqpts=3
    elif space=='RT2':   
       nqpts=3
    elif space=='P1':    
       nqpts=3
    elif space=='P2':    
       nqpts=7 #6
    elif space=='P3':    
       nqpts=6
    elif space=='P4':    
       nqpts=12
    elif space=='P1+':   
       nqpts=7 #6
    elif space=='P2+':   
       nqpts=7
    elif space=='P1NC':  
       nqpts=3
    else:
       exit('nqpts_default: space unknown')
    return nqpts

###############################################################################
