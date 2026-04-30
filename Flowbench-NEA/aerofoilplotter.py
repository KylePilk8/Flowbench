from dependecies import *
x=np.linspace(0,1,1000)
z=np.linspace(-1,2,10)

NACA=list(input())

if len(NACA)==4:
    m=(int(NACA[0]))/100
    p=(int(NACA[1]))/10
    t=(int(NACA[2]+NACA[3]))/100


    yt = 5 * t * (0.2969 * np.sqrt(x)- 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1015 * x**4)
    yt[999]=0
    if m==0 and p==0:
        xu=x
        xl=x
        yu=yt
        yl=-yt
        yc=x*0
    else:
        region1=x<p
        region2=x>=p
        yc=np.zeros_like(x)
        dyc_dx=np.zeros_like(x)

        yc[region1]=(m/p**2)*(2*p*x[region1]-x[region1]**2)
        dyc_dx[region1]=(2*m/(p**2))*(p-x[region1])

        yc[region2]=(m/((1-p)**2))*((1-2*p)+2*p*x[region2]-x[region2]**2)
        dyc_dx[region2]=(2*m/((1-p)**2))*(p-x[region2])


        theta=np.arctan(dyc_dx)

        xu=x-yt*np.sin(theta)
        yu=yc+yt*np.cos(theta)

        xl=x+yt*np.sin(theta)
        yl=yc-yt*np.cos(theta)

elif len(NACA)==5:
    L=int(NACA[0])*0.15
    P=int(NACA[1])*0.05
    S=int(NACA[2])
    t=(int(NACA[3]+NACA[4]))/100

    yt = 5 * t * (0.2969 * np.sqrt(x)- 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1015 * x**4)
    f=lambda r: r*(1-((r/3)**(1/2)))-P
    r=float(mp.findroot(f,0.2))
    temp=(1-2*r)
    N=(3*r-7*(r**2)+8*(r**3)-4*(r**4))/((r-(r**2))**0.5)-(3/2)*(1-2*r)*(((np.pi)/2)-np.arcsin(temp))
    k1=(6*L)/N
    k2=k1*((3*(r-P)**2)-(r**3))/((1-r)**3)

    region1=(x<r)
    region2=(x>=r)
    yc=np.zeros_like(x)
    dyc_dx=np.zeros_like(x)

    if S==0:
        yc[region1]=(k1/6)*((x[region1]**3)-3*r*(x[region1]**2)+(r**2)*(3-r)*x[region1])
        dyc_dx[region1]=(k1/6)*(3*(x[region1]**2)-6*r*x[region1]+(r**2)*(3-r))

        yc[region2]=((k1*(r**3))/6)*(1-x[region2])
        dyc_dx[region2]=(-1*k1*(r**3))/6
    
    elif S==1:
        
        yc[region1]=(k1/6)*(((x[region1]-r)**3)-(k2/k1)*((1-r)**3)*x[region1]-(r**3)*x[region1]+(r**3))
        dyc_dx[region1]=(k1/6)*(3*((x[region1]-r)**2)-(k2/k1)*((1-r)**3)-(r**3))
        
        yc[region2]=(k1/6)*((k2/k1)*((x[region2]-r)**3)-(k2/k1)*((1-r)**3)*x[region2]-(r**3)*x[region2]+(r**3))
        dyc_dx[region2]=(k1/6)*(3*(k2/k1)*((x[region2]-r)**2)-(k2/k1)*((1-r)**3)-(r**3))
    else:
        print(0)
        breakpoint

    theta=np.arctan(dyc_dx)

    xu=x-yt*np.sin(theta)
    yu=yc+yt*np.cos(theta)

    xl=x+yt*np.sin(theta)
    yl=yc-yt*np.cos(theta)


fig, ax=plt.subplots()
ax.set_xlabel('Chord')
ax.set_ylabel('Thickness')
ax.set_title('Aerofoil Plotter')
ax.plot(xu,yu)
ax.plot(xl,yl)
ax.plot(x,yc,label="MCL")
ax.plot(z,z*0,color="black")

ax.set_ylim(-0.2-t,0.2+t)
ax.set_xlim(-0.05,1.05)
plt.show()

