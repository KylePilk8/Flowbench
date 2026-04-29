from dependecies import *
NACA=list(input())
print(NACA)
m=(int(NACA[0]))/100
p=(int(NACA[1]))/10
t=(int(NACA[2]+NACA[3]))/100
print(m,p,t)

x=np.linspace(0,1,1000)
yt = 5 * t * (0.2969 * np.sqrt(x)- 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1015 * x**4)
if m==0 and p==0:
    xu=x
    xl=x
    yu=yt
    yl=-yt
    yc=x*0
else:
    mask1=x<p
    mask2=x>=p
    yc=np.zeros_like(x)
    dyc_dx=np.zeros_like(x)

    yc[mask1]=(m/p**2)*(2*p*x[mask1]-x[mask1]**2)
    dyc_dx[mask1]=(2*m/(p**2))*(p-x[mask1])

    yc[mask2]=(m/((1-p)**2))*((1-2*p)+2*p*x[mask2]-x[mask2]**2)
    dyc_dx[mask2]=(2*m/((1-p)**2))*(p-x[mask2])


    theta=np.arctan(dyc_dx)

    xu=x-yt*np.sin(theta)
    yu=yc+yt*np.cos(theta)

    xl=x+yt*np.sin(theta)
    yl=yc-yt*np.cos(theta)

fig, ax=plt.subplots()
ax.set_xlabel('Chord/m')
ax.set_ylabel('Thickness/m')
ax.set_title('Aerofoil Plotter')
ax.plot(xu,yu)
ax.plot(xl,yl)
ax.plot(x,yc)
plt.show()

