import numpy as np
import matplotlib.pyplot as plt
import random
from numba import jit
import time
start = time.time()
'''
Caixa bidimensional (L x L) contendo N partículas de raio R não interagentes
1. Inicialize N partículas em posições aleatórias
2. Inicialize N partículas em uma rede quadrada
3. Inicialize N partículas em uma rede triangular
'''
def maxwell_distribution(T):
    sigma = np.sqrt(T)
    vx = np.random.normal(0,sigma)
    vy = np.random.normal(0,sigma)
    return vx,vy

def MRU(particles,tf,dt,dat_name):
    t = 0
    N = len(particles)
    with open(f'{dat_name}.dat','w') as out:
        out.write('# t ' + ' '.join([f'x{i+1} y{i+1}' for i in range(N)]) + '\n')
        while t<tf:
            line_data = [f'{t:.5f}']  # Adiciona o tempo
            for p in particles:
                p.x += p.vx*dt
                p.y += p.vy*dt
                line_data.append(p.x)
                line_data.append(p.y)
                # Escreve a linha de dados no arquivo
            out.write(' '.join(map(str, line_data)) + '\n')
            t += dt


L = 1000000
N = 10000

def distance(p1,p2):
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def add_if_not_collision(self,new_particle):
    collision = False
    for particula in self.particles:
        if distance(particula,new_particle) < 2*new_particle.radius:
            collision = True
            break
    if not collision:
        self.particles = np.append(self.particles,new_particle)
    return

def collision_test_walls(self,particula):
    if (particula.x>self.L):
        particula.x = 2*self.L - particula.x
        particula.vx = -1*particula.vx
    elif (particula.x<0):
        particula.x = -particula.x
        particula.vx = -particula.vx
    elif (particula.y>self.L):
        particula.y = 2*self.L - particula.y
        particula.vy = -1*particula.vy
    elif (particula.y<0):
        particula.y =  -particula.y
        particula.vy = -particula.vy
    return 


class particle():
    def __init__(self,x,y,radius):
        self.radius = radius
        self.x = x
        self.y = y
        self.vx,self.vy = maxwell_distribution(500)



class box():
    def __init__(self,L):
        self.L = L
        self.particles = np.array([])
    def create_particles_random(self,radius,N):
        self.N = N
        while len(self.particles)<N:
            x = random.uniform(radius,self.L-radius)
            y = random.uniform(radius,self.L-radius)
            new_particle = particle(x,y,radius)
            add_if_not_collision(self,new_particle)
            #test if new_particle collides with the rest 
    def create_particles_square(self,radius):
        max_particles_line = int(np.floor(self.L/(2*radius)))
        self.N = max_particles_line**2
        for i in range(max_particles_line):
            for j in range(max_particles_line):
                x = (j + 0.5)* 2 * radius
                y = (i + 0.5) * 2 * radius
                new_particle = particle(x,y,radius)
                self.particles = np.append(self.particles,new_particle)
    def create_particles_triangle(self,radius):
        triangle_height = np.sqrt(3)*radius
        max_particles_line = int(np.floor(self.L/(2*radius)))
        max_particles_column = int(np.floor(self.L/triangle_height))
        self.N = max_particles_line*max_particles_column
        for i in range(max_particles_column):
            for j in range(max_particles_line):
                x = (j + 0.5)* 2 * radius
                if i%2 == 1:
                    x += radius
                y = (i + 0.5) * triangle_height
                if (x+radius < self.L) and (y + radius < self.L):
                    new_particle = particle(x,y,radius)
                    self.particles = np.append(self.particles,new_particle)
                
    def plotar(self):
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.set_xlim(0, self.L)
        ax.set_ylim(0, self.L)

        for particula in self.particles:
            circulo = plt.Circle((particula.x, particula.y), particula.radius, color='b', fill=True)
            ax.add_patch(circulo)

        plt.title(f'{self.N} Partículas em uma Caixa {self.L}x{self.L}')
        plt.show()
    
    def MRU(self,tf,dt,dat_name):
        t = 0
        N = len(self.particles)
        with open(f'{dat_name}.dat','w') as out:
            out.write('# t ' + ' '.join([f'x{i+1} y{i+1}' for i in range(N)]) + '\n')
            while t<tf:
                line_data = [f'{t:.5f}']  # Adiciona o tempo
                for p in self.particles:
                    p.x += p.vx*dt
                    p.y += p.vy*dt
                    collision_test_walls(self,p)
                    line_data.append(p.x)
                    line_data.append(p.y)
                    # Escreve a linha de dados no arquivo
                out.write(' '.join(map(str, line_data)) + '\n')
                t += dt
    

        
b = box(100)
b.create_particles_random(1,100)
print(b.particles)
#b.plotar()
p = b.MRU(30,0.01,'particle_animation')
end = time.time()
print(end-start)



        

    