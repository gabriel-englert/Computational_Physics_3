import numpy as np
import matplotlib.pyplot as plt



def verlet(x0,v0,tf,F,m,dt,dat_name):
    a = F/m
    t = 0
    x = x0
    v = v0
    t_list = [0]
    v_list = [v]
    x_list = [x]
    out = open(f'{dat_name}.dat','w')
    out.write('#t  x  v \n')
    while t<tf:
        v = v + (1/2)*a*dt
        x = x + v*dt
        F = -k*x
        a = F/m
        v = v + (1/2)*a*dt
        t += dt
        out.write(f'{t:.5f}  {x:.5f}  {v:.5f} \n')
    out.close()
    return 

v = 0
x = 10
r0 = 0
m=1
k=1
F = -k*(x)
a = F/m
tf = 100
dt = 0.01
dat_name = 'verlet_data'
verlet(x,v,30,F,m,dt,dat_name)
    

    
    