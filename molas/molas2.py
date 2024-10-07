import numpy as np
import matplotlib.pyplot as plt
#Duas partículas e 3 molas, uma entre as partículas, e cada partícula presa a uma parede

def verlet_2_molas(x01,x02,v01,v02,tf,r0,r02,m,dt,dat_name):
    #valores iniciais
    t = 0
    x1 = x01
    v1 = v01
    x2 = x02
    v2 = v02
    #calculando forças e  acelerações iniciais
    F21 = -k*((x2-x1)-r0) #força de 1 em 2
    F12 = -k*((x1-x2)+r0) #força de 2 em 1
    F1P = -k*(x1-r0) #força da parede em 1
    F2P = -k*(x2-r02) #força da parede em 2
    a1 = (F12 + F1P)/m #aceleração partícula 1
    a2 = (F21 + F2P)/m #aceleração partícula 2
    #criando arquivo dat e escrevendo cabeçalho e valores iniciais
    out = open(f'{dat_name}.dat','w')
    out.write('#t  x1  x2  v1  v2 \n')
    out.write(f'{t:.5f}  {x1:.5f}  {x2:.5f}  {v1:.5f}  {v2:.5f} \n')
    #loop do velocity verlet
    while t<tf:
        #atualiza velocidade para t+dt/2
        v1 = v1 + (1/2)*a1*dt
        v2 = v2 + (1/2)*a2*dt
        x1 = x1 + v1*dt
        x2 = x2 + v2*dt
        #atualiza aceleração
        F21 = -k*((x2-x1)-r0)
        F12 = -k*((x1-x2)+r0)
        F1P = -k*(x1-r0)
        F2P = -k*(x2-r02)
        a1 = (F12 + F1P)/m
        a2 = (F21 + F2P)/m
        #atualiza velocidade novamente, com a nova aceleração
        v1 = v1 + (1/2)*a1*dt
        v2 = v2 + (1/2)*a2*dt
        t += dt
        out.write(f'{t:.5f}  {x1:.5f}  {x2:.5f}  {v1:.5f}  {v2:.5f} \n')
    out.close()
    return 

v1 = -1
v2 = 5
x1 = 2
x2 = 10
r0 = 5
r02 = 9
m=1
k=1
F21 = -k*((x2-x1)-r0)
F12 = -k*((x1-x2)+r0)
F1P = -k*(x1-r0)
F2P = -k*(x2-r02)
a1 = (F12 + F1P)/m
a2 = (F21 + F2P)/m
tf = 100
dt = 0.01
dat_name = 'verlet_data_2'
verlet_2_molas(x1,x2,v1,v2,100,r0,r02,m,dt,dat_name)